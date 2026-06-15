"""Менеджер задач: BST, очередь исполнения и стек отмены."""

from src.models.task import Task
from src.services.undo_action import ActionType, UndoAction
from src.structures.binary_search_tree import BinarySearchTree
from src.structures.queue import Queue
from src.structures.stack import Stack


class TaskManager:
    """Управление списком задач и связанными структурами данных."""

    def __init__(self):
        self._tasks_by_id = {}
        self._deadline_tree = BinarySearchTree()
        self._execution_queue = Queue()
        self._undo_stack = Stack()
        self._next_id = 1

    def get_task_count(self):
        return len(self._tasks_by_id)

    def add_task(
        self,
        name,
        priority,
        execution_time,
        deadline,
        record_undo=True,
    ):
        """Добавляет новую задачу."""
        task = Task(
            task_id=self._next_id,
            name=name.strip(),
            priority=priority,
            execution_time=execution_time,
            deadline=deadline,
        )
        self._next_id += 1
        self._tasks_by_id[task.task_id] = task
        self._deadline_tree.insert(task)

        if record_undo:
            self._undo_stack.push(UndoAction(ActionType.ADD, task))

        return task

    def delete_task(self, task_id, record_undo=True):
        """Удаляет задачу по идентификатору."""
        task = self._tasks_by_id.get(task_id)
        if task is None:
            return False

        self._deadline_tree.delete(task)
        del self._tasks_by_id[task_id]
        self._remove_from_queue(task_id)

        if record_undo:
            self._undo_stack.push(UndoAction(ActionType.DELETE, task))

        return True

    def modify_task(
        self,
        task_id,
        name=None,
        priority=None,
        execution_time=None,
        deadline=None,
        record_undo=True,
    ):
        """Изменяет поля существующей задачи."""
        old_task = self._tasks_by_id.get(task_id)
        if old_task is None:
            return None

        if record_undo:
            self._undo_stack.push(
                UndoAction(
                    ActionType.MODIFY,
                    task=old_task,
                    previous_task=Task(
                        task_id=old_task.task_id,
                        name=old_task.name,
                        priority=old_task.priority,
                        execution_time=old_task.execution_time,
                        deadline=old_task.deadline,
                    ),
                )
            )

        self._deadline_tree.delete(old_task)

        updated_task = Task(
            task_id=old_task.task_id,
            name=name.strip() if name is not None else old_task.name,
            priority=priority if priority is not None else old_task.priority,
            execution_time=(
                execution_time
                if execution_time is not None
                else old_task.execution_time
            ),
            deadline=deadline if deadline is not None else old_task.deadline,
        )

        self._tasks_by_id[task_id] = updated_task
        self._deadline_tree.insert(updated_task)
        self._update_task_in_queue(updated_task)
        return updated_task

    def get_task(self, task_id):
        return self._tasks_by_id.get(task_id)

    def list_tasks_by_deadline(self):
        """Возвращает задачи в порядке возрастания дедлайна (рекурсивный обход)."""
        return self._deadline_tree.inorder_traversal()

    def find_earliest_deadline_task(self):
        return self._deadline_tree.find_earliest()

    def find_latest_deadline_task(self):
        return self._deadline_tree.find_latest()

    def enqueue_for_execution(self, task_id):
        """Добавляет задачу в очередь на исполнение."""
        task = self._tasks_by_id.get(task_id)
        if task is None:
            return False
        self._execution_queue.enqueue(task)
        return True

    def dequeue_execution(self):
        """Извлекает следующую задачу из очереди исполнения."""
        if self._execution_queue.is_empty():
            return None
        return self._execution_queue.dequeue()

    def get_execution_queue(self):
        return self._execution_queue.to_list()

    def can_undo(self):
        return not self._undo_stack.is_empty()

    def undo(self):
        """Отменяет последнее действие. Возвращает описание отменённого действия."""
        if self._undo_stack.is_empty():
            return None

        action = self._undo_stack.pop()

        if action.action_type == ActionType.ADD:
            self.delete_task(action.task.task_id, record_undo=False)
            return f"Отменено добавление: {action.task.name}"

        if action.action_type == ActionType.DELETE:
            self._restore_deleted_task(action.task)
            return f"Отменено удаление: {action.task.name}"

        if action.action_type == ActionType.MODIFY and action.previous_task:
            self.modify_task(
                action.previous_task.task_id,
                name=action.previous_task.name,
                priority=action.previous_task.priority,
                execution_time=action.previous_task.execution_time,
                deadline=action.previous_task.deadline,
                record_undo=False,
            )
            return f"Отменено изменение: {action.previous_task.name}"

        return None

    def _restore_deleted_task(self, task):
        self._tasks_by_id[task.task_id] = task
        self._deadline_tree.insert(task)
        if task.task_id >= self._next_id:
            self._next_id = task.task_id + 1

    def _remove_from_queue(self, task_id):
        remaining = []
        for task in self._execution_queue.to_list():
            if task.task_id != task_id:
                remaining.append(task)

        self._execution_queue = Queue()
        for task in remaining:
            self._execution_queue.enqueue(task)

    def _update_task_in_queue(self, updated_task):
        new_queue = Queue()
        for task in self._execution_queue.to_list():
            if task.task_id == updated_task.task_id:
                new_queue.enqueue(updated_task)
            else:
                new_queue.enqueue(task)

        self._execution_queue = new_queue
