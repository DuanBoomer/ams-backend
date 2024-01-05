from pydantic import BaseModel
from typing import Optional

class PasswordData(BaseModel):
    password: str
    type: str

class AuthData(BaseModel):
    email: str
    password: str

class Alumni(BaseModel):
    name: str
    batch: str
    company: str
    position: str
    email: str
    desc: str
    image: str
    expertise: list

class Student(BaseModel):
    roll_no: str
    name: str
    email: str
    stream: str
    student_coordinator: Optional[str] = None
    alumni: Optional[str] = None
    desc: str
    course: str
    image: str

class Event(BaseModel):
    title: str
    start_time: str
    end_time: str
    day: str
    date: str
    desc: str
    link: str
    type: str
    docs: list

class Chat(BaseModel):
    text: str
    sender: str

