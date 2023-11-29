from pydantic import BaseModel

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
    student_coordinator: str
    alumni: str
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

