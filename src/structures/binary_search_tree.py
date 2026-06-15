class BSTNode:
    """Узел бинарного дерева поиска."""

    def __init__(self, task):
        self.task = task
        self.left = None
        self.right = None


class BinarySearchTree:
    """
    Бинарное дерево поиска.

    Ключ сортировки — дедлайн задачи; при равных дедлайнах — идентификатор.
    """

    def __init__(self):
        self._root = None
        self._size = 0

    def get_size(self):
        return self._size

    def is_empty(self):
        return self._root is None

    def _compare(self, task_a, task_b):
        if task_a.deadline < task_b.deadline:
            return -1
        if task_a.deadline > task_b.deadline:
            return 1
        if task_a.task_id < task_b.task_id:
            return -1
        if task_a.task_id > task_b.task_id:
            return 1
        return 0

    def insert(self, task):
        """Вставляет задачу в дерево."""
        if self._root is None:
            self._root = BSTNode(task)
            self._size += 1
            return

        current = self._root
        while True:
            comparison = self._compare(task, current.task)
            if comparison < 0:
                if current.left is None:
                    current.left = BSTNode(task)
                    self._size += 1
                    return
                current = current.left
            elif comparison > 0:
                if current.right is None:
                    current.right = BSTNode(task)
                    self._size += 1
                    return
                current = current.right
            else:
                current.task = task
                return

    def delete(self, task):
        """Удаляет задачу из дерева. Возвращает True, если задача найдена."""
        self._root, deleted = self._delete_node(self._root, task)
        if deleted:
            self._size -= 1
        return deleted

    def _delete_node(self, node, task):
        if node is None:
            return None, False

        comparison = self._compare(task, node.task)
        if comparison < 0:
            node.left, deleted = self._delete_node(node.left, task)
            return node, deleted
        if comparison > 0:
            node.right, deleted = self._delete_node(node.right, task)
            return node, deleted

        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True

        successor = self._find_min_node(node.right)
        node.task = successor.task
        node.right, _ = self._delete_node(node.right, successor.task)
        return node, True

    def find(self, task_id):
        """Находит задачу по идентификатору."""
        return self._find_by_id(self._root, task_id)

    def _find_by_id(self, node, task_id):
        if node is None:
            return None
        if node.task.task_id == task_id:
            return node.task
        found = self._find_by_id(node.left, task_id)
        if found is not None:
            return found
        return self._find_by_id(node.right, task_id)

    def find_earliest(self):
        """Возвращает задачу с самым ранним дедлайном."""
        if self._root is None:
            return None
        return self._find_min_node(self._root).task

    def find_latest(self):
        """Возвращает задачу с самым поздним дедлайном."""
        if self._root is None:
            return None
        return self._find_max_node(self._root).task

    def _find_min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def _find_max_node(self, node):
        while node.right is not None:
            node = node.right
        return node

    def inorder_traversal(self):
        """Рекурсивный симметричный обход — задачи по возрастанию дедлайна."""
        result = []
        self._inorder_recursive(self._root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node is None:
            return
        self._inorder_recursive(node.left, result)
        result.append(node.task)
        self._inorder_recursive(node.right, result)

    def filter_by_deadline_before(self, deadline):
        """Возвращает задачи с дедлайном не позже указанной даты."""
        result = []
        self._filter_recursive(self._root, deadline, result)
        return result

    def _filter_recursive(self, node, deadline, result):
        if node is None:
            return

        if node.task.deadline <= deadline:
            self._filter_recursive(node.left, deadline, result)
            result.append(node.task)
            self._filter_recursive(node.right, deadline, result)
        else:
            self._filter_recursive(node.left, deadline, result)
