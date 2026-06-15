"""Консольный интерфейс системы управления задачами."""

from datetime import datetime
from src.services.task_manager import TaskManager


class TaskCLI:
    """Меню для работы с задачами."""

    DATE_FORMAT = "%d.%m.%Y %H:%M"

    def __init__(self):
        self._manager = TaskManager()

    def run(self):
        """Запускает главный цикл программы."""
        print("=== Система управления задачами с приоритетами ===")

        while True:
            self._print_menu()
            choice = input("Выберите пункт меню: ").strip()

            result = True
            if choice == "1":

            elif choice == "2":
                self._handle_delete_task()
            elif choice == "3":
                self._handle_modify_task()
            elif choice == "4":
                self._handle_list_by_deadline()
            elif choice == "5":
                self._handle_find_earliest()
            elif choice == "6":
                self._handle_find_latest()
            elif choice == "7":
                self._handle_enqueue()
            elif choice == "8":
                self._handle_dequeue()
            elif choice == "9":
                self._handle_show_queue()
            elif choice == "10":
                self._handle_undo()
            elif choice == "0":
                result = self._handle_exit()
            else:
                print("Неверный пункт меню. Попробуйте снова.")
                continue

            if result is False:
                break

            print()

    def _print_menu(self):
        print("\n--- Меню ---")
        print("1. Добавить задачу")
        print("2. Удалить задачу")
        print("3. Изменить задачу")
        print("4. Список задач по дедлайну")
        print("5. Задача с самым ранним дедлайном")
        print("6. Задача с самым поздним дедлайном")
        print("7. Добавить задачу в очередь исполнения")
        print("8. Взять задачу из очереди исполнения")
        print("9. Показать очередь исполнения")
        print("10. Отменить последнее действие")
        print("0. Выход")

    def _read_int(self, prompt, min_value, max_value):
        while True:
            raw = input(prompt).strip()
            try:
                value = int(raw)
            except ValueError:
                print("Введите целое число.")
                continue
            if value < min_value or value > max_value:
                print(f"Значение должно быть от {min_value} до {max_value}.")
                continue
            return value

    def _read_deadline(self):
        while True:
            raw = input(
                f"Дедлайн ({self.DATE_FORMAT}, например 15.06.2026 18:00): "
            ).strip()
            try:
                return datetime.strptime(raw, self.DATE_FORMAT)
            except ValueError:
                print("Неверный формат даты. Используйте DD.MM.YYYY HH:MM.")

    def _read_task_id(self):
        return self._read_int("ID задачи: ", 1, 10**9)

    def _handle_add_task(self):
        name = input("Название задачи: ").strip()
        if not name:
            print("Название не может быть пустым.")
            return

        priority = self._read_int("Приоритет (1 — низкий, 5 — высокий): ", 1, 5)
        execution_time = self._read_int("Время выполнения (мин): ", 1, 10**6)
        deadline = self._read_deadline()

        task = self._manager.add_task(name, priority, execution_time, deadline)
        print(f"Задача добавлена: {task}")

    def _handle_delete_task(self):
        task_id = self._read_task_id()
        if self._manager.delete_task(task_id):
            print(f"Задача {task_id} удалена.")
        else:
            print(f"Задача с ID {task_id} не найдена.")

    def _handle_modify_task(self):
        task_id = self._read_task_id()
        task = self._manager.get_task(task_id)
        if task is None:
            print(f"Задача с ID {task_id} не найдена.")
            return

        print(f"Текущая задача: {task}")
        print("Оставьте поле пустым, чтобы не менять его.")

        name = input(f"Новое название [{task.name}]: ").strip()
        priority_raw = input(f"Новый приоритет [{task.priority}]: ").strip()
        time_raw = input(
            f"Новое время выполнения [{task.execution_time}]: "
        ).strip()
        deadline_raw = input(
            f"Новый дедлайн [{task.deadline.strftime(self.DATE_FORMAT)}]: "
        ).strip()

        priority = None
        if priority_raw:
            try:
                priority = int(priority_raw)
            except ValueError:
                print("Приоритет должен быть целым числом.")
                return
            if priority < 1 or priority > 5:
                print("Приоритет должен быть от 1 до 5.")
                return

        execution_time = None
        if time_raw:
            try:
                execution_time = int(time_raw)
            except ValueError:
                print("Время выполнения должно быть целым числом.")
                return
            if execution_time < 1:
                print("Время выполнения должно быть больше 0.")
                return

        deadline = None
        if deadline_raw:
            try:
                deadline = datetime.strptime(deadline_raw, self.DATE_FORMAT)
            except ValueError:
                print("Неверный формат даты. Используйте DD.MM.YYYY HH:MM.")
                return

        updated = self._manager.modify_task(
            task_id,
            name=name or None,
            priority=priority,
            execution_time=execution_time,
            deadline=deadline,
        )
        if updated:
            print(f"Задача обновлена: {updated}")

    def _handle_list_by_deadline(self):
        tasks = self._manager.list_tasks_by_deadline()
        if not tasks:
            print("Список задач пуст.")
            return

        print("Задачи по возрастанию дедлайна:")
        for index, task in enumerate(tasks, start=1):
            print(f"{index}. {task}")

    def _handle_find_earliest(self):
        task = self._manager.find_earliest_deadline_task()
        if task is None:
            print("Список задач пуст.")
            return
        print(f"Самый ранний дедлайн: {task}")

    def _handle_find_latest(self):
        task = self._manager.find_latest_deadline_task()
        if task is None:
            print("Список задач пуст.")
            return
        print(f"Самый поздний дедлайн: {task}")

    def _handle_enqueue(self):
        task_id = self._read_task_id()
        if self._manager.enqueue_for_execution(task_id):
            print(f"Задача {task_id} добавлена в очередь исполнения.")
        else:
            print(f"Задача с ID {task_id} не найдена.")

    def _handle_dequeue(self):
        task = self._manager.dequeue_execution()
        if task is None:
            print("Очередь исполнения пуста.")
            return
        print(f"Следующая задача к исполнению: {task}")

    def _handle_show_queue(self):
        queue = self._manager.get_execution_queue()
        if not queue:
            print("Очередь исполнения пуста.")
            return

        print("Очередь исполнения:")
        for index, task in enumerate(queue, start=1):
            print(f"{index}. {task}")

    def _handle_undo(self):
        if not self._manager.can_undo():
            print("Нет действий для отмены.")
            return

        message = self._manager.undo()
        if message:
            print(message)
        else:
            print("Не удалось отменить последнее действие.")

    def _handle_exit(self):
        print("Завершение работы.")
        return False


def run():
    """Точка входа консольного интерфейса."""
    TaskCLI().run()
