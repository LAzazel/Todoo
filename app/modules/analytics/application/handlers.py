from app.modules.analytics.domain.models import SystemStats, TodoActivityRecorded

class AnalyticsHandlers:
    def __init__(self, stats_store: SystemStats):
        self.stats = stats_store

    def handle_new_todo_activity(self, internal_event: TodoActivityRecorded):
        self.stats.total_todos_created += 1
        if internal_event.is_high_priority:
            self.stats.high_priority_todos += 1

    def handle_todo_completed(self):
        self.stats.total_todos_completed += 1

    def handle_user_registered(self):
        self.stats.total_users_registered += 1