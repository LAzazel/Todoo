from app.modules.analytics.domain.models import SystemStats, TodoActivityRecorded
from app.modules.analytics.application.handlers import AnalyticsHandlers
from app.modules.analytics.infrastructure.acl import AnalyticsACL
from app.modules.core.public_contract import (
    TodoCreatedIntegrationEvent,
    TodoCompletedIntegrationEvent,
    UserRegisteredIntegrationEvent,
)
from app.modules.core.infrastructure.event_bus.in_memory_bus import InMemoryEventBus

def make_acl() -> tuple[AnalyticsACL, SystemStats]:
    stats = SystemStats()
    handlers = AnalyticsHandlers(stats)
    acl = AnalyticsACL(handlers)
    return acl, stats

class TestAnalyticsModule:
    def test_acl_does_not_pass_external_model_to_handlers(self):
        received_types = []

        class SpyHandlers(AnalyticsHandlers):
            def handle_new_todo_activity(self, internal_event):
                received_types.append(type(internal_event))

        acl = AnalyticsACL(SpyHandlers(SystemStats()))
        acl.translate_and_handle_created(
            TodoCreatedIntegrationEvent(todo_id=1, owner_id=1, priority=4)
        )
        assert received_types == [TodoActivityRecorded]

    def test_analytics_failure_does_not_affect_core(self):
        bus = InMemoryEventBus()
        acl, stats = make_acl()
        side_results = []

        def broken_analytics(event):
            raise RuntimeError("analytics is down")

        bus.subscribe(TodoCreatedIntegrationEvent, broken_analytics)
        bus.subscribe(TodoCreatedIntegrationEvent, lambda e: side_results.append(e))

        bus.publish(TodoCreatedIntegrationEvent(todo_id=1, owner_id=1, priority=1))
        assert len(side_results) == 1

    def test_end_to_end_analytics_flow(self):
        bus = InMemoryEventBus()
        acl, stats = make_acl()

        bus.subscribe(TodoCreatedIntegrationEvent, acl.translate_and_handle_created)
        bus.subscribe(TodoCompletedIntegrationEvent, acl.translate_and_handle_completed)
        bus.subscribe(UserRegisteredIntegrationEvent, acl.translate_and_handle_user_registered)

        bus.publish(TodoCreatedIntegrationEvent(todo_id=1, owner_id=1, priority=1))
        bus.publish(TodoCreatedIntegrationEvent(todo_id=2, owner_id=1, priority=4))
        bus.publish(TodoCompletedIntegrationEvent(todo_id=1, owner_id=1))
        
        bus.publish(UserRegisteredIntegrationEvent(user_id=1, email="bob@example.com"))

        assert stats.total_todos_created == 2
        assert stats.total_todos_completed == 1
        assert stats.high_priority_todos == 1
        assert stats.total_users_registered == 1