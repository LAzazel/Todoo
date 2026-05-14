from app.modules.analytics.domain.models import SystemStats

_stats_store = SystemStats()

def get_stats_store() -> SystemStats:
    return _stats_store