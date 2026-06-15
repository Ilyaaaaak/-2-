"""Типы действий для стека отмены."""

from src.models.task import Task


class ActionType:
    """Виды изменений, которые можно отменить."""

    ADD = "Добавление"
    DELETE = "Удаление"
    MODIFY = "Изменение"


class UndoAction:
    """Запись об изменении для отмены."""

    def __init__(self, action_type, task, previous_task=None):
        self.action_type = action_type
        self.task = task
        self.previous_task = previous_task
