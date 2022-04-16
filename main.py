from doctest import FAIL_FAST
import imp
from urllib import response
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import Todo

app = FastAPI()

from database import (
    fetch_all_todo,
    create_todo,
    update_todo,
    remove_todo,
    fetch_one_todo
)

origins = ['https://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def read_root():
    return {"Status": "Working"}


@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todo()
    return response


@app.get("/api/todo{title}", response_model=Todo)
async def get_todo_id(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, "No Found")


@app.post("/api/todo", response_model=Todo)
async def add_todo(todo:Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Error")


@app.put("/api/todo{id}", response_model=Todo)
async def put_todo(title:str, description:str):
    response = await update_todo(title, description)
    if response:
        return response
    raise HTTPException(400, "Error")


@app.delete("/api/todo{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return response
    raise HTTPException(400, "Error")