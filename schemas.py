
from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    date_of_birth: date
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    course: str | None = Field(default=None, max_length=100)
    address: str | None = Field(default=None, max_length=250)
    enrollment_date: date | None = None

    @model_validator(mode="after")
    def check_contact(self):
        if not self.email and not self.phone:
            raise ValueError("Provide an email address or phone number")
        return self


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    date_of_birth: date | None = None
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    course: str | None = Field(default=None, max_length=100)
    address: str | None = Field(default=None, max_length=250)
    enrollment_date: date | None = None

    model_config = ConfigDict(extra="forbid")


class StudentResponse(BaseModel):
    student_id: int
    name: str
    date_of_birth: date
    email: EmailStr | None
    phone: str | None
    course: str | None
    address: str | None
    enrollment_date: date | None

    model_config = ConfigDict(from_attributes=True)
