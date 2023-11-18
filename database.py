import motor.motor_asyncio
from model import Student
import os
# from model import Todo

uri = os.getenv("MONGODB")
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
database = client.alumni_mapping_system
alumni_collection = database.alumni
student_collection = database.student


async def authenticate_alumni(email, password):
    data = await alumni_collection.find_one({"email": email, "password": password})
    return data


async def authenticate_student(email, password):
    data = await student_collection.find_one({"email": email, "password": password})
    return data


async def fetch_student(email):
    data = await student_collection.find_one({"email": email})
    return data


async def fetch_alumni(email):
    data = await alumni_collection.find_one({"email": email})
    return data


async def fetch_ongoing_event(email):
    data = await alumni_collection.find_one({"email": email}, {"event_history": {"$elemMatch": {"type": "pending"}}})
    return data['event_history'][0]


async def fetch_events_history(email):
    data = await alumni_collection.find_one({"email": email})
    return data["event_history"]

async def fetch_event_details(email, title):
    data = await alumni_collection.find_one({"email": email}, {"event_history": {"$elemMatch": {"title": title}}})
    return data['event_history'][0]


async def fetch_all_students(email):
    data = []
    cursor = student_collection.find({"alumni": email})
    async for document in cursor:
        data.append(Student(**document))
    return data


# async def schedule_event(email, event):
#     alumni_collection.update_one(
#         {"email": email}, {"$push": {"event_history": event}})
#     return event


# async def update_alumni_details(email, alumni):
#     try:
#         data = await alumni_collection.find_one({"email": email})
#         for key in data.keys():
#             if key in alumni.keys() and data[key] != alumni[key]:
#                 alumni_collection.update_one(
#                     {"email": email}, {"$set": {f"{key}": alumni[key]}})
#         return alumni
#     except AttributeError:
#         return {"error": "invalid email id"}


# async def update_student_details(email, student):
#     try:
#         data = await student_collection.find_one({"email": email})
#         for key in data.keys():
#             if key in student.keys() and data[key] != student[key]:
#                 student_collection.update_one(
#                     {"email": email}, {"$set": {f"{key}": student[key]}})
#         return student
#     except AttributeError:
#         return {"error": "invalid email id"}


# async def fetch_one_todo(title):
#     document = await collection.find_one({"title": title})
#     return document

# async def fetch_all_todos():
#     todos = []
#     cursor = collection.find({})
#     async for document in cursor:
#         todos.append(Todo(**document))
#     return todos

# async def create_todo(todo):
#     document = todo
#     result = await collection.insert_one(document)
#     return document


# async def update_todo(title, desc):
#     await collection.update_one({"title": title}, {"$set": {"description": desc}})
#     document = await collection.find_one({"title": title})
#     return document

# async def remove_todo(title):
#     await collection.delete_one({"title": title})
#     return True
