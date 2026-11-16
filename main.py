# Главный файл приложения
from fastapi import FastAPI
from routers import tasks, stats

app = FastAPI(
    title="ToDo лист API",
    description="API для управления задачами с использованием матрицы Эйзенхауэра",
    version="1.0.0",
    contact={ 
        "name": "Захваткин Кирилл Андреевич",
    }

)

routers = [tasks.router, stats.router]

for router in routers:
    app.include_router(router, prefix="/api/v1")
    
    
@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Привет, студент!",
        **app.openapi()["info"],
    }
