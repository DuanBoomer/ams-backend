from pydantic import BaseModel

class Alumni(BaseModel):
    name: str
    email: str
    company: str
    expertise: list
    desc: str
    image: str

class Student(BaseModel):
    alumni: str
    name: str
    email: str
    desc: str
    course: str
    stream: str
    year: str
    rollno: str

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

