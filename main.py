from fastapi import FastAPI, HTTPException, UploadFile, File
# import motor.motor_asyncio
from pymongo import MongoClient
# import gridfs
# import shutil
from model import (Alumni, Event, Student, AuthData,
                   Chat, PasswordData, ReviewList, BugReport)
# from database import (
# authenticate_alumni,
# authenticate_student,
# fetch_student,
# fetch_alumni,
# fetch_events_history,
# fetch_ongoing_event,
# fetch_event_details,
# remove_event,
# update_event_details,
# fetch_all_students,
# update_alumni_details,
# schedule_event,
# update_alumni_details,
# update_student_details
# )
import os
from fastapi.middleware.cors import CORSMiddleware
import socketio
DYNAMIC_API_URL = "https://ams-chat-api.onrender.com/"

app = FastAPI()
origins = ["http://localhost:3000", "https://alumni-mapping-system.vercel.app",
           "https://ams-chat-api.onrender.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# uri = os.getenv("MONGODB")
uri = "mongodb+srv://chirag1292003:12092003Duan@alumni-mapping-system-d.iryfq1v.mongodb.net/?retryWrites=true&w=majority"
# client = motor.motor_asyncio.AsyncIOMotorClient(uri)
client = MongoClient(uri)
database = client.alumni_mapping_system
alumni_collection = database.alumni
student_collection = database.student
bugs_collection = database.bugs
chat_collection = database.chat


@app.get("/")
async def home_route():
    return {"application": "alumni-mapping-system"}


@app.post("/auth")
async def auth_user(post_data: AuthData):
    '''
    used for the login page \n
    send the email and the password hash in the following format \n
        email: string
        password: string
    if autherised you will recieve the following response \n
        type: alumni or student
        email: string
        alumni: if type == student
        login: "first time" if logging in for the first time
    else you will get the following response \n
        null
    '''
    post_data = post_data.model_dump()
    data = alumni_collection.find_one({
        "email": post_data["email"],
        "password": post_data["password"]
    })
    if (data and post_data["password"] == ""):
        return {
            "type": "alumni",
            "email": data["email"],
            "login": "first time"
        }
    elif (data and post_data["password"] != ""):
        return {
            "type": "alumni",
            "email": data["email"]
        }

    data = student_collection.find_one({
        "email": post_data["email"],
        "password": post_data["password"]
    })
    if (data and post_data["password"] == ""):
        return {
            "type": "student",
            "email": data["email"],
            "alumni": data["alumni"],
            "login": "first time"
        }
    elif (data and post_data["password"] != ""):
        return {
            "type": "student",
            "email": data["email"],
            "alumni": data["alumni"]
        }


@app.get("/data/{email}")
async def get_data(email):
    '''
    get some data about a user \n
    the request should have a email in the url \n
    if the email is of a student it will return \n
        roll_no: str
        name: str
        email: str
        stream: str
        student_coordinator: str
        alumni: str
        desc: str
        course: str
        image: str
    if the email is of a alumni it will return \n
        name: str
        batch: str
        company: str
        position: str
        email: str
        desc: str
        image: str
        expertise: list
    '''
    data = alumni_collection.find_one({
        "email": email
    })
    if (data):
        return Alumni(**data)

    data = student_collection.find_one({
        "email": email
    })
    if (data):
        return Student(**data)


@app.get("/data/students/{email}")
async def students_data(email):
    '''
    get all the details of students under a alumni \n
    the request should have a email in url \n
    it will return a array with the following details \n
        [
            roll_no: str
            name: str
            email: str
            stream: str
            student_coordinator: str
            alumni: str
            desc: str
            course: str
            image: str
        ]
    '''
    data = []
    cursor = student_collection.find({"alumni": email})
    if (cursor):
        for document in cursor:
            data.append(Student(**document))
        return data


@app.get("/event/history/{email}")
async def event_history(email):
    '''
    get all the events that have happended or are happening under a alumni  \n
    it takes a alumni email in the url and returns the list of events as below \n
        pending: []
        done: []
    each event is described by the following attributes \n
        title: str
        start_time: str
        end_time: str
        day: str
        date: str
        desc: str
        link: str
        type: str
        docs: list
    '''
    data = {
        "pending": [],
        "done": [],
    }
    cursor = alumni_collection.find_one({"email": email})
    if cursor and cursor['event_history']:
        for val in cursor['event_history']:
            if val['type'] == 'pending':
                data["pending"].append(val)
            else:
                data["done"].append(val)
    return data


@app.put("/update/student/{email}")
async def update_student(email, put_data: Student):
    '''
    change the student details in the database \n
    the request should have the following parameters \n
        desc: str
        image: str
        interest: str TODO
    returns \n
        success: true | false
    '''
    details = put_data.model_dump()
    try:
        data = student_collection.find_one({"email": email})
        for key in data.keys():
            if key in details.keys() and data[key] != details[key]:
                student_collection.update_one(
                    {"email": email}, {"$set": {f"{key}": details[key]}})
        return {"success": True}
    except:
        return {"success": False}


@app.put("/update/alumni/{email}")
async def update_alumni(email, put_data: Alumni):
    '''
    change the alumni details in the database \n
    the request should have the following parameters \n
        company: str
        position: str
        desc: str
        image: str
        expertise: list
    returns \n
        success: true | false
    '''
    details = put_data.model_dump()
    try:
        data = alumni_collection.find_one({"email": email})
        for key in data.keys():
            if key in details.keys() and data[key] != details[key]:
                alumni_collection.update_one(
                    {"email": email}, {"$set": {f"{key}": details[key]}})
        return {"success": True}
    except:
        return {"success": False}


@app.put("/set/password/{email}")
async def set_password(email, data: PasswordData):
    '''
    set the password of a user in the database \n
    the request url must contain the email and the request body must contain the password and the type of the user \n
    returns \n
        success: true | false

    '''
    type = data.type
    password = data.password

    if type == "alumni":
        try:
            alumni_collection.update_one(
                {"email": email}, {"$set": {"password": password}})
            return {
                "success": True,
            }
        except:
            return {
                "success": False
            }
    if type == "student":
        try:
            student_collection.update_one(
                {"email": email}, {"$set": {"password": password}})
            return {
                "success": True,
            }
        except:
            return {
                "success": False
            }


@app.put("/update/event/{email}/{title}")
async def update_event(email, title, details: Event):
    '''
    change the event details without canceling the event \n
    supply the email of the alumni and the title of the event in the url = \n
    also give the new event details in the put request with the following parameters \n
        title: str 
        start_time: str
        end_time: str
        day: str 
        date: str
        desc: str
        talking_points: str
        link: str
        type: str
        docs: list
    if the event is updated you will get the following response \n
        success: true
    if the event is not updated you will get the following response \n
        success: false
    '''
    details = details.model_dump()
    try:
        data = alumni_collection.find_one({"email": email})
        data = data['event_history']
        for i in range(len(data)):
            if data[i]['title'] == title:
                data[i] = details

        re = alumni_collection.update_one(
            {"email": email}, {"$set": {"event_history": data}})
        with socketio.SimpleClient() as sio:
            sio.connect(f'{DYNAMIC_API_URL}')
            sio.emit("event_updates", email)
        return {"success": True}
    except:
        return {"success": False}


@app.delete("/delete/event/{email}/{title}")
async def delete_event(email, title):
    '''
    cancel a scheduled event \n
    supply the email of the alumni under which the event is hosted and the title of the event in the url \n 
    if the event is successfully deleted, you will recieve the following response \n
        success: true
    if it is not deleted, you will recieve the following response \n
        success: false
    '''
    try:
        data = alumni_collection.update_one(
            {"email": email},
            {"$pull": {"event_history": {"title": title}}})
        with socketio.SimpleClient() as sio:
            sio.connect(f'{DYNAMIC_API_URL}')
            sio.emit("event_updates", email)
        return {"success": True}
    except:
        return {"success": "False"}


@app.post("/schedule/event/{email}")
async def post_event(email, event: Event):
    '''
    schedule a event \n
    supply the email of the alumni under which the event needs to be held in the url \n
    also send the following details about the event in the post request \n
        title: str
        start_time: str
        end_time: str
        day: str
        date: str
        desc: str
        link: str
        talking_points: str
        type: str
        docs: list
    if the event is scheduled you will get the following response \n
        success: true
    if the event is not schedules you will get the following response \n
        success: false
    '''
    event = event.model_dump()
    try:
        alumni_collection.update_one(
            {"email": email}, {"$push": {"event_history": event}})
        with socketio.SimpleClient() as sio:
            sio.connect(f'{DYNAMIC_API_URL}')
            sio.emit("event_updates", email)
        return {"success": True}
    except:
        return {"success": False}


@app.post("/review/students/{email}")
async def review_students(email, event: Event, reviews: ReviewList):
    '''
    review the students after the alumni is done with the event \n
    the data must be recieved in the following format \n
        student_name(str): review(str)
    if the review is successfully stored you will get the following response \n
        success: true
    else you will get the following response \n
        success: false
    '''
    event = event.model_dump()
    reviews = reviews.model_dump()
    try:
        data = alumni_collection.find_one({"email": email})
        data = data['event_history']
        for i in range(len(data)):
            if data[i]['title'] == event['title'] and data[i]['date'] == event['date']:
                data[i]['reviews'] = reviews['data']
        re = alumni_collection.update_one(
            {"email": email}, {"$set": {"event_history": data}})
        with socketio.SimpleClient() as sio:
            sio.connect(f'{DYNAMIC_API_URL}')
            sio.emit("event_updates", email)
        return {"success": True}
    except:
        return {"success": False}


@app.post("/bugreport/{email}")
async def post_bug_report(email, report: BugReport):
    '''
    file a bug report for ams, the format of the bug report is as following \n
        email: str
        message: str
    if the report is filed sucessfully
        success: true
    else
        sucess: false
    '''
    message = report.model_dump()['message']
    try:
        bugs_collection.insert_one({"email": email, "message": message})
        return {"success": True}
    except:
        return {"success": False}


@app.get("/chat/{alumni}")
async def get_chat(alumni, skip: int = 0, limit: int = 20):
    '''
    get the intial chat done by a group under a alumni
    '''
    data = []
    cursor = chat_collection.aggregate([
        {
            "$match": {"alumni": alumni}
        },
        {
            "$project":
            {
                "_id": 0,
                "result":
                {
                    "$sortArray": {"input": "$chat", "sortBy": {"time": -1}},
                }
            },
        },
        {
            "$project": {
                "result": {
                    "$slice": ["$result", skip, limit],
                }
            }
        }
    ])
    if cursor:
        for i in cursor:
            for c in i['result']:
                data.append(c)
        return data[::-1]


# @app.post("/upload/{email}")
# async def upload_document(email, uploaded_file: UploadFile = File(...)):
#     content =   uploaded_file.read()
#     return content

    # path = f"files/{uploaded_file.filename}"
    # with open(path, 'w+b') as file:
    #     shutil.copyfileobj(uploaded_file.file, file)

    # with open(path, "rb") as file:
    #     data = file.read()
    # return data
