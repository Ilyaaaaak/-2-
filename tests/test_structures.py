import unittest

from src.structures.queue import Queue
from src.structures.stack import Stack


class TestStack(unittest.TestCase):
    def test_push_and_pop(self):
        stack = Stack()

        stack.push("first")
        stack.push("second")

        self.assertEqual(stack.pop(), "second")
        self.assertEqual(stack.pop(), "first")
        self.assertTrue(stack.is_empty())

    def test_pop_empty_stack_raises_error(self):
        stack = Stack()

        with self.assertRaises(IndexError):
            stack.pop()

    def test_peek_returns_last_item_without_removing_it(self):
        stack = Stack()

        stack.push("first")
        stack.push("second")

        self.assertEqual(stack.peek(), "second")
        self.assertEqual(len(stack), 2)


class TestQueue(unittest.TestCase):
    def test_enqueue_and_dequeue(self):
        queue = Queue()

        queue.enqueue("first")
        queue.enqueue("second")

        self.assertEqual(queue.dequeue(), "first")
        self.assertEqual(queue.dequeue(), "second")
        self.assertTrue(queue.is_empty())

    def test_dequeue_empty_queue_raises_error(self):
        queue = Queue()

        with self.assertRaises(IndexError):
            queue.dequeue()

    def test_peek_returns_first_item_without_removing_it(self):
        queue = Queue()

        queue.enqueue("first")
        queue.enqueue("second")

        self.assertEqual(queue.peek(), "first")
        self.assertEqual(len(queue), 2)


if __name__ == "__main__":
    unittest.main()
