"""Модуль с собственными декораторами: hello, timer, retry."""

import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)


def hello(func):
    """Печатает «Начинаем...» перед вызовом функции и «Готово!» после."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Начинаем...")
        result = func(*args, **kwargs)
        print("Готово!")
        return result

    return wrapper


def timer(func):
    """Измеряет и печатает время выполнения функции в секундах (4 знака)."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            print(f"Функция {func.__name__} выполнена за {elapsed:.4f} с")

    return wrapper


def retry(attempts=3, delay=0):
    """Повторяет вызов функции при исключении.

    Args:
        attempts: максимальное число попыток (не меньше 1).
        delay: пауза между попытками в секундах.

    Raises:
        RuntimeError: если все попытки закончились исключением.
    """
    if attempts < 1:
        raise ValueError("attempts должно быть не меньше 1")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    last_error = error
                    logger.warning(
                        "Попытка %d/%d функции %s не удалась: %r",
                        attempt, attempts, func.__name__, error,
                    )
                    if attempt < attempts and delay > 0:
                        time.sleep(delay)
            raise RuntimeError(
                f"Функция {func.__name__} не выполнена за {attempts} попыток"
            ) from last_error

        return wrapper

    return decorator
