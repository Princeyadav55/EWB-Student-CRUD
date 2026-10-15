

# Students Database CRUD Application

## Project Overview
A Python backend application developed for the EWB Edu Tech Pvt. Ltd. internship assignment.

This application manages student records using FastAPI and SQLite.

## Features
- Create student records
- List and filter students
- Retrieve an individual student
- Update student details
- Delete student records
- Input validation and error handling
- Persistent SQLite storage

## Technologies Used
- Python
- FastAPI
- SQLite
- Uvicorn
- Pydantic

## Prerequisites
- Python 3.13 or compatible version
- pip
- Git

## Installation

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run the Application

```powershell
python -m uvicorn main:app --reload
```

## API Documentation

Open this URL in your browser:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /students | Create a student |
| GET | /students | List or filter students |
| GET | /students/{student_id} | Retrieve a student |
| PUT | /students/{student_id} | Update student details |
| DELETE | /students/{student_id} | Delete a student |

## Database
SQLite stores student records in `students.db`.
The application initializes the students table automatically.

## Testing
Use the interactive Swagger UI at `/docs` to test the endpoints.

Use dummy student information for testing.
