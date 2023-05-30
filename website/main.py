from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from dotenv import load_dotenv
import psycopg2
import aiosql
import os
import csv
from pydantic import BaseModel


app = FastAPI()
templates = Jinja2Templates(directory='templates/')

class Company(BaseModel):
    name: str
    address: str

def read_csv(file_path):
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        data = list(reader)
    return data    

# @app.get("/hello/{name}")
# async def root(request: Request, name: str):
#     accept = request.headers.get("accept")
#     hello_world = {"message": f"hello {name}"}

#     if accept.split("/")[1] == 'json':
#         return hello_world

#     if len(accept.split(",")) > 1 or accept.split("/")[1] == 'html':
#         response = templates.TemplateResponse("index.html", {"request": request, "payload1": hello_world}) 
#         return response

@app.get("/companies")
async def get_companies(request: Request):
    file_path = "sample-data/project.csv"  
    data = read_csv(file_path)
    load_dotenv()

    # conn = psycopg2.connect(f"dbname=tdm_main user=iyengar1 password=FOLD-gumption-aqualung-slurry-weary host=lpvtdmdb01.itap.purdue.edu")
    # queries = aiosql.from_path("queries.sql", "psycopg2")

    companies = [v['company'] for v in data]
    #companies = [Company(name=v) for v in companies]

    print(f"{companies=}")

    accept = request.headers.get("accept")

    if accept.split("/")[1] == 'json':
        return companies

    if len(accept.split(",")) > 1 or accept.split("/")[1] == 'html':
        response = templates.TemplateResponse("test_templates/companies.html", {"request": request, "payload1": companies}) 
        return response

