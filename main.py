# Главный файл приложения
from fastapi import FastAPI
from routers import tasks

app = FastAPI(
    title="ToDo лист API",
    description="API для управления задачами с использованием матрицы Эйзенхауэра",
    version="1.0.0",
    contact={ 
        "name": "Захваткин Кирилл Андреевич",
    }

)

app.include_router(tasks.router)

@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Привет, студент!",
        **app.openapi()["info"],
    }

@app.post("/tasks")
async def create_task(task: dict):
    return {"message": "Запись успешно создана", "task": task}