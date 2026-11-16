from fastapi import APIRouter
from schemas import TaskBase, TaskCreate, TaskResponse, TaskUpdate
from database import tasks_db

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
    responses={404: {"description": "Stats not found"}}
)

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