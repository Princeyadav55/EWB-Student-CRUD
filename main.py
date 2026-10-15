
from contextlib import asynccontextmanager
import sqlite3
from datetime import date

from fastapi import FastAPI, HTTPException, Query, Response, status

from database import get_connection, init_db
from schemas import StudentCreate, StudentUpdate, StudentResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Students Database CRUD API",
    description="EWB Edu Tech internship project",
    version="1.0.0",
    lifespan=lifespan,
)


def student_to_dict(row):
    return dict(row)


@app.get("/")
def home():
    return {"message": "Students Database CRUD API is running"}


@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(student: StudentCreate):
    data = student.model_dump(mode="json")

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO students
                (name, date_of_birth, email, phone, course, address, enrollment_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data["name"].strip(),
                    data["date_of_birth"],
                    data["email"],
                    data["phone"],
                    data["course"],
                    data["address"],
                    data["enrollment_date"],
                ),
            )
            row = connection.execute(
                "SELECT * FROM students WHERE student_id = ?",
                (cursor.lastrowid,),
            ).fetchone()
            return student_to_dict(row)

    except sqlite3.IntegrityError as exc:
        raise HTTPException(
            status_code=409,
            detail="This email is already registered",
        ) from exc


@app.get("/students", response_model=list[StudentResponse])
def list_students(
    name: str | None = None,
    course: str | None = None,
    born_after: date | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    query = "SELECT * FROM students WHERE 1=1"
    parameters = []

    if name:
        query += " AND name LIKE ?"
        parameters.append(f"%{name}%")

    if course:
        query += " AND course LIKE ?"
        parameters.append(f"%{course}%")

    if born_after:
        query += " AND date_of_birth > ?"
        parameters.append(born_after.isoformat())

    query += " ORDER BY student_id LIMIT ? OFFSET ?"
    parameters.extend([limit, offset])

    with get_connection() as connection:
        rows = connection.execute(query, parameters).fetchall()
        return [student_to_dict(row) for row in rows]


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (student_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student_to_dict(row)


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentUpdate):
    changes = student.model_dump(exclude_unset=True, mode="json")

    if not changes:
        raise HTTPException(status_code=400, detail="No fields provided")

    if "name" in changes and changes["name"] is not None:
        changes["name"] = changes["name"].strip()

    with get_connection() as connection:
        existing = connection.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (student_id,),
        ).fetchone()

        if existing is None:
            raise HTTPException(status_code=404, detail="Student not found")

        merged = dict(existing)
        merged.update(changes)

        if not merged["email"] and not merged["phone"]:
            raise HTTPException(
                status_code=422,
                detail="A student must have an email address or phone number",
            )

        columns = list(changes.keys())
        assignments = ", ".join(f"{column} = ?" for column in columns)
        values = [changes[column] for column in columns]

        try:
            connection.execute(
                f"UPDATE students SET {assignments} WHERE student_id = ?",
                (*values, student_id),
            )
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=409,
                detail="This email is already registered",
            ) from exc

        row = connection.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (student_id,),
        ).fetchone()

        return student_to_dict(row)


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,),
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
