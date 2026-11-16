from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import List, Dict, Any

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Task not found"}}
)

# Временное хранилище (позже будет заменено на PostgreSQL)
tasks_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "title": "Сдать проект по FastAPI",
        "description": "Завершить разработку API и написать документацию",
        "is_important": True,
        "is_urgent": True,
        "quadrant": "Q1",
        "completed": False,
        "created_at": datetime.now()
    },
    {
        "id": 2,
        "title": "Изучить SQLAlchemy",
        "description": "Прочитать документацию и попробовать примеры",
        "is_important": True,
        "is_urgent": False,
        "quadrant": "Q2",
        "completed": False,
        "created_at": datetime.now()
    },
    {
        "id": 3,
        "title": "Сходить на лекцию",
        "description": None,
        "is_important": False,
        "is_urgent": True,
        "quadrant": "Q3",
        "completed": False,
        "created_at": datetime.now()
    },
    {
        "id": 4,
        "title": "Посмотреть сериал",
        "description": "Новый сезон любимого сериала",
        "is_important": False,
        "is_urgent": False,
        "quadrant": "Q4",
        "completed": True,
        "created_at": datetime.now()
    },
]

@router.get("")
async def get_all_tasks() -> dict:
    return {
        "count": len(tasks_db), # считает количество записей в хранилище
        "tasks": tasks_db # выводит всё, чта есть в хранилище
    }
    
@router.get("/quadrant/{quadrant}")
async def get_tasks_by_quadrant(quadrant: str) -> dict:
    if quadrant not in ["Q1", "Q2", "Q3", "Q4"]:
        raise HTTPException( 
            status_code=400,
            detail="Неверный квадрант. Используйте: Q1, Q2, Q3, Q4" 
        )
    filtered_tasks = [task for task in tasks_db if task["quadrant"] == quadrant]
    return {
        "quadrant": quadrant,
        "count": len(filtered_tasks),
        "tasks": filtered_tasks
    }
    
@router.get("/stats")
async def get_tasks_stats() -> dict:
    by_quadrant = {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0}
    for task in tasks_db:
        by_quadrant[task["quadrant"]] += 1

    completed = sum(1 for task in tasks_db if task["completed"])

    return {
        "total_tasks": len(tasks_db),
        "by_quadrant": by_quadrant,
        "by_status": {
            "completed": completed,
            "pending": len(tasks_db) - completed,
        },
    }


@router.get("/search")
async def search_tasks(q: str) -> dict:
    keyword = q.lower()
    found = [
        t for t in tasks_db
        if keyword in t["title"].lower()
        or keyword in (t["description"] or "").lower()
    ]

    return {
        "query": q,
        "count": len(found),
        "tasks": found
    }


@router.get("/status/{status}")
async def get_tasks_by_status(status: str) -> dict:
    if status not in ("completed", "pending"):
        raise HTTPException(
            status_code=404,
            detail="Статус не найден. Используйте: completed, pending"
        )

    is_completed = status == "completed"
    filtered_tasks = [t for t in tasks_db if t["completed"] == is_completed]

    return {
        "status": status,
        "count": len(filtered_tasks),
        "tasks": filtered_tasks
    }


@router.get("/{task_id}")
async def get_tasks_by_id(task_id: int) -> dict:
    for task in tasks_db:
        if task_id==task['id']:
            return task
    raise HTTPException(
        status_code=404,
        detail="Задача не найдена"
    )