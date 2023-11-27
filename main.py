from fastapi import FastAPI, HTTPException

from model import (Alumni, Event, Student)
# import socketio
from database import (
    authenticate_alumni,
    authenticate_student,
    fetch_student,
    fetch_alumni,
    fetch_events_history,
    fetch_ongoing_event,
    fetch_event_details,
    remove_event,
    update_event_details,
    fetch_all_students,
    update_alumni_details,
    schedule_event,
    # update_alumni_details,
    # update_student_details
)

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:3000", "https://alumni-mapping-system.vercel.app"
]

# sio=socketio.AsyncServer(cors_allowed_origins=origins,async_mode='asgi')
# socket_app = socketio.ASGIApp(sio)
# app.mount("/", socket_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home_route():
    return {"application": "alumni-mapping-system"}


@app.get("/alumni/{email}/{password}", response_model=Alumni)
async def auth_alumni(email, password):
    data = await authenticate_alumni(email, password)
    if (data):
        return data
    return HTTPException(404, f"Authentication failed for {email}")


@app.get("/student/{email}/{password}", response_model=Student)
async def auth_student(email, password):
    data = await authenticate_student(email, password)
    if (data):
        return data
    return HTTPException(404, f"Authentication failed for {email}")


@app.get("/alumni/{email}", response_model=Alumni)
async def get_alumni_details(email):
    data = await fetch_alumni(email)
    if (data):
        return data
    return HTTPException(404, f"No alumni with email: {email} exists")


@app.get("/student/{email}", response_model=Student)
async def get_student_details(email):
    data = await fetch_student(email)
    if (data):
        return data
    return HTTPException(404, f"No student with email: {email} exists")


@app.get("/events/alumni/{email}")
async def get_events_history(email):
    data = await fetch_events_history(email)
    if (data):
        return data
    return HTTPException(404, f"No events for alumni with email: {email}")


@app.get("/students/alumni/{email}")
async def get_students_under_alumni(email):
    data = await fetch_all_students(email)
    if (data):
        return data
    return HTTPException(404, f"No students under alumni with email: {email}")


@app.get("/ongoing_event/alumni/{email}")
async def get_ongoing_event(email):
    data = await fetch_ongoing_event(email)
    if (data):
        return data
    return HTTPException(404, f"No ongoing events for alumni with email: {email}")


@app.get("/eventdetails/alumni/{email}/{title}")
async def get_event_details(email, title):
    data = await fetch_event_details(email, title)
    if (data):
        return data
    return HTTPException(404, f"No event under alumni email: {email} with title: {title}")


@app.delete("/delete/events/{email}/{title}")
async def delete_event(email, title):
    data = await remove_event(email, title)
    if (data):
        return data
    return HTTPException(404, f"No event under alumni email: {email}")


@app.put("/update/alumni/{email}", response_model=Alumni)
async def put_alumni_details(email, details: Alumni):
    data = await update_alumni_details(email, details.dict())
    if "error" in data.keys():
        return HTTPException(405, f"Unable to update alumni with email: {email}")
    elif data:
        return data
    return HTTPException(404, f"No alumni with email: {email} found")


@app.post("/schedule_event/alumni/{email}", response_model=Event)
async def post_event(email, event: Event):
    data = await schedule_event(email, event.dict())
    if "error" in data.keys():
        return HTTPException(405, f"Unable to schedule meet for alumni with email: {email}")
    elif (data):
        return data
    return HTTPException(404, "Schedule Failed")

@app.put("/update/event/{email}/{title}")
async def put_event_details(email, title, details: Event):
    data = await update_event_details(email, title, details.dict())
    if (data):
        return data
    return HTTPException(404, f"some shit went really wrong")


# @app.post("/alumni/{email}", response_model=Alumni)
# async def update_alumni(email, data: Alumni):
#     # data = await update_alumni_details(email, data.dict())
#     # if (data):
#     #     return data
#     # return HTTPException(404, "Updation failed for alumni {email}")
#     return {"response": f"update alumni {email}"}


# @app.post("student/{email}", response_model=Student)
# async def update_student(email, data: Student):
#     # data = await update_student_details(email, data.dict())
#     # if (data):
#     #     return data
#     # return HTTPException(404, "Updation failed for studet {email}")
#     return {"response": f"update student {email}"}


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
