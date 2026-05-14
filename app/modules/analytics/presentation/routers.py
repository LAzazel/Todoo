from fastapi import APIRouter
from app.modules.analytics.public_contract import get_stats_store

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/stats")
def get_system_stats():
    stats = get_stats_store()
    return {
        "total_created": stats.total_todos_created,
        "total_completed": stats.total_todos_completed,
        "high_priority": stats.high_priority_todos,
        "total_users": stats.total_users_registered
    }