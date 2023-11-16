from fastapi import FastAPI, HTTPException

from model import (Alumni, Event, Student)

from database import (
    fetch_alumni,
    fetch_student,
    fetch_events_history,
    fetch_all_students,
    schedule_event,
    update_alumni_details,
    update_student_details
)

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/alumni/{email}", response_model=Alumni)
async def get_alumni(email):
    data = await fetch_alumni(email)
    if (data):
        return data
    return HTTPException(404, f"There is no alumni with the email {email}")


@app.get("/student/{email}", response_model=Student)
async def get_student(email):
    data = await fetch_student(email)
    if (data):
        return data
    return HTTPException(404, f"There is no student with the email {email}")


@app.get("/alumni/{email}/events")
async def get_events(email):
    data = await fetch_events_history(email)
    if (data):
        return {"history": data}
    return HTTPException(404, "No events")


@app.get("/alumni/{email}/students")
async def get_students(email):
    data = await fetch_all_students(email)
    if (data):
        return data
    return HTTPException(404, "Couldn't find")


@app.post("/alumni/{email}/schedule_event", response_model=Event)
async def post_event(email, event: Event):
    event = await schedule_event(email, event.dict())
    if (event):
        return event
    return HTTPException(404, "Schedule Failed")


@app.post("/alumni/{email}", response_model=Alumni)
async def update_alumni(email, data: Alumni):
    data = await update_alumni_details(email, data.dict())
    if (data):
        return data
    return HTTPException(404, "Updation failed for alumni {email}")


@app.post("student/{email}", response_model=Student)
async def update_student(email, data: Student):
    data = await update_student_details(email, data.dict())
    if (data):
        return data
    return HTTPException(404, "Updation failed for studet {email}")


# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}

# @app.get("/api/todo")
# async def get_todo():
#     response = await fetch_all_todos()
#     return response

# @app.get("/api/todo/{title}", response_model=Todo)
# async def get_todo_by_title(title):
#     response = await fetch_one_todo(title)
#     if response:
#         return response
#     raise HTTPException(404, f"There is no todo with the title {title}")

# @app.post("/api/todo/", response_model=Todo)
# async def post_todo(todo: Todo):
#     response = await create_todo(todo.dict())
#     if response:
#         return response
#     raise HTTPException(400, "Something went wrong")

# @app.put("/api/todo/{title}/", response_model=Todo)
# async def put_todo(title: str, desc: str):
#     response = await update_todo(title, desc)
#     if response:
#         return response
#     raise HTTPException(404, f"There is no todo with the title {title}")

# @app.delete("/api/todo/{title}")
# async def delete_todo(title):
#     response = await remove_todo(title)
#     if response:
#         return "Successfully deleted todo"
#     raise HTTPException(404, f"There is no todo with the title {title}")
