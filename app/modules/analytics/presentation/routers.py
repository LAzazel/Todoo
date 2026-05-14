from fastapi import APIRouter
from app.modules.analytics.domain.models import SystemStats

router = APIRouter(prefix="/analytics", tags=["analytics"])

global_stats_db = SystemStats()

@router.get("/stats")
def get_system_stats():
    return {
        "total_created": global_stats_db.total_todos_created,
        "total_completed": global_stats_db.total_todos_completed,
        "high_priority": global_stats_db.high_priority_todos,
        "total_users": global_stats_db.total_users_registered
    }