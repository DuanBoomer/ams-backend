import motor.motor_asyncio
from model import (Student, Event)
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
    returnVal = []
    data = await alumni_collection.find_one({"email": email})

    for val in data['event_history']:
        if val['type'] == 'pending':
            returnVal.append(val)

    return returnVal


async def fetch_events_history(email):
    returnVal = {
        "pending": [],
        "done": [],
    }
    data = await alumni_collection.find_one({"email": email})
    for val in data['event_history']:
        if val['type'] == 'pending':
            returnVal["pending"].append(val)
        else:
            returnVal["done"].append(val)

    return returnVal


async def fetch_event_details(email, title):
    data = await alumni_collection.find_one({"email": email}, {"event_history": {"$elemMatch": {"title": title}}})
    return data['event_history'][0]


async def remove_event(email, title):
    data = await alumni_collection.update_one({"email": email}, {"$pull": {"event_history": {"title": title}}})
    print(data)
    return {"success": True}

async def update_event_details(email, title, details):
    try:
        data = await alumni_collection.find_one({"email": email})
        data = data['event_history']
        for i in range(len(data)):
            if data[i]['title'] == title:
                data[i] = details

        alumni_collection.update_one({"email": email}, {"$set": {f"event_history": data}})
        return details
    except:
        return {"error": "invalid email id"}


async def fetch_all_students(email):
    data = []
    cursor = student_collection.find({"alumni": email})
    async for document in cursor:
        data.append(Student(**document))
    return data


async def update_alumni_details(email, details):
    try:
        data = await alumni_collection.find_one({"email": email})
        for key in data.keys():
            if key in details.keys() and data[key] != details[key]:
                alumni_collection.update_one(
                    {"email": email}, {"$set": {f"{key}": details[key]}})
        return details
    except:
        return {"error": "invalid email id"}


async def schedule_event(email, event):
    try:
        alumni_collection.update_one(
            {"email": email}, {"$push": {"event_history": event}})
        return event
    except:
        return {"error": "some error occured"}


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
