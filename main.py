from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from dotenv import load_dotenv
from typing import List
import psycopg2
import aiosql
import os
import csv
from model import Project, Projects
from pydantic import BaseModel


app = FastAPI()
templates = Jinja2Templates(directory='templates/')

# hard coded this for testing purpose
users = {
    "admin": {"password": "adminpass", "is_admin": True},
    "user": {"password": "userpass", "is_admin": False},
}

# A global variable to track the current logged-in user
current_user = None

# new code to parse csv file and add into model
def parse_csv():
    file_path = "sample_data/projects.csv" 
    models = [] 
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            model = Project(**row)
            models.append(model)
            
    return models

@app.get("/companies")
async def get_companies(request: Request):
    projects = parse_csv()
    accept = request.headers.get("accept")

    if accept.split("/")[1] == 'json':
        return projects

    if len(accept.split(",")) > 1 or accept.split("/")[1] == 'html':
        response = templates.TemplateResponse("test_templates/companies.html", {"request": request, "payload1": projects}) 
        return response

@app.get("/")
async def get_index(request: Request):
    global current_user
    response = templates.TemplateResponse("base.html", {"request": request, "username": current_user}) 
    return response

@app.get("/list")
async def get_companies(request: Request):
    load_dotenv()
    conn = psycopg2.connect(f"dbname={os.getenv('DB_NAME')} user={os.getenv('DB_USER')} password={os.getenv('DB_PASSWORD')} host={os.getenv('DB_HOST')}")
    queries = aiosql.from_path("queries.sql", "psycopg2")

    proj = sorted([v for v in queries.get_all_projects(conn)], key=lambda x: x[1], reverse=True)
    years_dict = dict()
    years_dict[2023] = ['TestA', 'TestB']
    for line in proj:
        if line[1] in years_dict:
            # append the new number to the existing array at this slot
            years_dict[int(line[1])].append(line[0])
        else:
            # create a new array in this slot
            years_dict[int(line[1])] = [line[0]]
    print(years_dict)
    response = templates.TemplateResponse("test_templates/list.html", {"request": request, "payload1": years_dict}) 
    return response

@app.get("/login", response_class=HTMLResponse)
def admin_interface(request: Request):
    return templates.TemplateResponse("test_account/login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    global current_user

    if username in users and users[username]["password"] == password:
        current_user = username
        return templates.TemplateResponse("test_account/user.html", {"request": request, "username": username})
    else:
        return templates.TemplateResponse("test_account/login.html", {"request": request, "error": "Invalid username or password."})
    
@app.get("/logout")
def logout(request: Request):
    global current_user
    current_user = None
    return templates.TemplateResponse("test_account/login.html", {"request": request})


@app.get("/dashboard")
def dashboard(request: Request):
    if current_user and users[current_user]["is_admin"]:
        return templates.TemplateResponse("test_account/dashboard.html", {"request": request, "username": current_user})
    else:
        return templates.TemplateResponse("test_account/unauthorized.html", {"request": request})