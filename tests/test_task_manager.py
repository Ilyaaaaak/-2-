import unittest
from datetime import datetime

from src.services.task_manager import TaskManager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()

    def test_add_task(self):
        deadline = datetime(2026, 6, 15, 18, 0)

        task = self.manager.add_task("Сделать отчёт", 5, 60, deadline)

        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.name, "Сделать отчёт")
        self.assertEqual(self.manager.get_task_count(), 1)
        self.assertEqual(self.manager.get_task(1), task)

    def test_list_tasks_by_deadline(self):
        late = datetime(2026, 6, 20, 12, 0)
        early = datetime(2026, 6, 15, 12, 0)

        self.manager.add_task("Поздняя задача", 1, 20, late)
        self.manager.add_task("Ранняя задача", 2, 30, early)

        tasks = self.manager.list_tasks_by_deadline()

        self.assertEqual(tasks[0].name, "Ранняя задача")
        self.assertEqual(tasks[1].name, "Поздняя задача")

    def test_find_earliest_and_latest_deadline(self):
        self.manager.add_task("Средняя", 3, 30, datetime(2026, 6, 16, 12, 0))
        self.manager.add_task("Ранняя", 1, 10, datetime(2026, 6, 14, 12, 0))
        self.manager.add_task("Поздняя", 5, 50, datetime(2026, 6, 20, 12, 0))

        earliest = self.manager.find_earliest_deadline_task()
        latest = self.manager.find_latest_deadline_task()

        self.assertEqual(earliest.name, "Ранняя")
        self.assertEqual(latest.name, "Поздняя")

    def test_delete_task(self):
        task = self.manager.add_task(
            "Удалить меня",
            2,
            15,
            datetime(2026, 6, 15, 10, 0),
        )

        result = self.manager.delete_task(task.task_id)

        self.assertTrue(result)
        self.assertIsNone(self.manager.get_task(task.task_id))
        self.assertEqual(self.manager.get_task_count(), 0)

    def test_delete_unknown_task_returns_false(self):
        result = self.manager.delete_task(999)

        self.assertFalse(result)
        self.assertEqual(self.manager.get_task_count(), 0)

    def test_modify_task_updates_queue(self):
        task = self.manager.add_task(
            "Старое название",
            2,
            15,
            datetime(2026, 6, 15, 10, 0),
        )
        self.manager.enqueue_for_execution(task.task_id)

        updated = self.manager.modify_task(task.task_id, name="Новое название")
        queue = self.manager.get_execution_queue()

        self.assertEqual(updated.name, "Новое название")
        self.assertEqual(queue[0].name, "Новое название")

    def test_modify_unknown_task_returns_none(self):
        result = self.manager.modify_task(999, name="Новое название")

        self.assertIsNone(result)

    def test_delete_task_removes_it_from_queue(self):
        first = self.manager.add_task("Первая", 1, 10, datetime(2026, 6, 15, 10, 0))
        second = self.manager.add_task("Вторая", 2, 20, datetime(2026, 6, 16, 10, 0))

        self.manager.enqueue_for_execution(first.task_id)
        self.manager.enqueue_for_execution(second.task_id)
        self.manager.delete_task(first.task_id)

        queue = self.manager.get_execution_queue()

        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0].name, "Вторая")

    def test_execution_queue(self):
        first = self.manager.add_task("Первая", 1, 10, datetime(2026, 6, 15, 10, 0))
        second = self.manager.add_task("Вторая", 2, 20, datetime(2026, 6, 16, 10, 0))

        self.assertTrue(self.manager.enqueue_for_execution(first.task_id))
        self.assertTrue(self.manager.enqueue_for_execution(second.task_id))

        self.assertEqual(self.manager.dequeue_execution().name, "Первая")
        self.assertEqual(self.manager.dequeue_execution().name, "Вторая")
        self.assertIsNone(self.manager.dequeue_execution())

    def test_undo_add(self):
        task = self.manager.add_task(
            "Новая задача",
            1,
            10,
            datetime(2026, 6, 15, 10, 0),
        )

        message = self.manager.undo()

        self.assertEqual(message, "Отменено добавление: Новая задача")
        self.assertIsNone(self.manager.get_task(task.task_id))

    def test_undo_delete(self):
        task = self.manager.add_task(
            "Восстановить",
            1,
            10,
            datetime(2026, 6, 15, 10, 0),
        )
        self.manager.delete_task(task.task_id)

        message = self.manager.undo()

        self.assertEqual(message, "Отменено удаление: Восстановить")
        self.assertIsNotNone(self.manager.get_task(task.task_id))

    def test_undo_modify(self):
        task = self.manager.add_task(
            "Старое",
            1,
            10,
            datetime(2026, 6, 15, 10, 0),
        )

        self.manager.modify_task(task.task_id, name="Новое")
        message = self.manager.undo()

        self.assertEqual(message, "Отменено изменение: Старое")
        self.assertEqual(self.manager.get_task(task.task_id).name, "Старое")


if __name__ == "__main__":
    unittest.main()
