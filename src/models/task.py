"""Модель задачи для системы управления."""


class Task:
    """Задача с названием, приоритетом, временем выполнения и дедлайном."""

    def __init__(self, task_id, name, priority, execution_time, deadline):
        self.task_id = task_id
        self.name = name
        self.priority = priority
        self.execution_time = execution_time
        self.deadline = deadline

    def __str__(self):
        return (
            f"[{self.task_id}] {self.name} | "
            f"приоритет: {self.priority} | "
            f"время: {self.execution_time} мин | "
            f"дедлайн: {self.deadline.strftime('%d.%m.%Y %H:%M')}"
        )
