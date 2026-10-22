"""Тесты для модуля decorators."""

import io
import re
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from decorators import hello, retry, timer


class TestHello(unittest.TestCase):
    def test_prints_before_and_after(self):
        @hello
        def work():
            print("работа")
            return 42

        buf = io.StringIO()
        with redirect_stdout(buf):
            result = work()
        self.assertEqual(buf.getvalue().splitlines(), ["Начинаем...", "работа", "Готово!"])
        self.assertEqual(result, 42)

    def test_keeps_metadata(self):
        @hello
        def work():
            """Док."""

        self.assertEqual(work.__name__, "work")
        self.assertEqual(work.__doc__, "Док.")


class TestTimer(unittest.TestCase):
    def test_prints_time_with_4_digits(self):
        @timer
        def add(a, b):
            return a + b

        buf = io.StringIO()
        with redirect_stdout(buf):
            result = add(2, b=3)
        self.assertEqual(result, 5)
        self.assertRegex(buf.getvalue(), r"\d+\.\d{4} с")

    def test_measures_time(self):
        with patch("decorators.time.perf_counter", side_effect=[10.0, 10.12345]):
            @timer
            def f():
                pass

            buf = io.StringIO()
            with redirect_stdout(buf):
                f()
        self.assertIn("0.1235", buf.getvalue())


class TestRetry(unittest.TestCase):
    def test_success_after_failures(self):
        calls = []

        @retry(attempts=3)
        def flaky():
            calls.append(1)
            if len(calls) < 3:
                raise ValueError("сбой")
            return "ok"

        self.assertEqual(flaky(), "ok")
        self.assertEqual(len(calls), 3)

    def test_runtime_error_when_exhausted(self):
        calls = []

        @retry(attempts=3)
        def broken():
            calls.append(1)
            raise ValueError("сбой")

        with self.assertRaises(RuntimeError) as ctx:
            broken()
        self.assertEqual(len(calls), 3)
        self.assertIsInstance(ctx.exception.__cause__, ValueError)

    def test_delay_between_attempts(self):
        @retry(attempts=3, delay=0.5)
        def broken():
            raise ValueError

        with patch("decorators.time.sleep") as sleep:
            with self.assertRaises(RuntimeError):
                broken()
        self.assertEqual(sleep.call_count, 2)
        sleep.assert_called_with(0.5)

    def test_invalid_attempts(self):
        with self.assertRaises(ValueError):
            retry(attempts=0)

    def test_keeps_metadata(self):
        @retry()
        def f():
            """Док."""

        self.assertEqual(f.__name__, "f")


if __name__ == "__main__":
    unittest.main()
