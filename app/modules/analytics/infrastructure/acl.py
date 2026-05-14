from app.modules.analytics.application.handlers import AnalyticsHandlers
from app.modules.analytics.domain.models import TodoActivityRecorded
from app.modules.core.public_contract import TodoCompletedIntegrationEvent, TodoCreatedIntegrationEvent, UserRegisteredIntegrationEvent


class AnalyticsACL:
    def __init__(self, handlers: AnalyticsHandlers):
        self.handlers = handlers

    def translate_and_handle_created(self, external_event: TodoCreatedIntegrationEvent):
        is_high = external_event.priority >= 3
        internal_event = TodoActivityRecorded(is_high_priority=is_high)
        
        self.handlers.handle_new_todo_activity(internal_event)

    def translate_and_handle_completed(self, external_event: TodoCompletedIntegrationEvent):
        self.handlers.handle_todo_completed()

    def translate_and_handle_user_registered(self, external_event: UserRegisteredIntegrationEvent):
        self.handlers.handle_user_registered()