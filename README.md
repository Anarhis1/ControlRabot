# Декораторы в Python

Модуль `decorators.py` с тремя декораторами и тесты `test_decorators.py`.

## Структура

```
decorators_project/
├── decorators.py        # модуль с декораторами
├── test_decorators.py   # тесты
└── README.md
```

## Запуск

```
python -m unittest -v
```

## Использование

```python
from decorators import hello, timer, retry

@hello
def greet():
    print("Привет")

@timer
def calc():
    return sum(range(1_000_000))

@retry(attempts=3, delay=0.1)
def unstable():
    ...
```

## Результаты

| Декоратор | Что делает | Проверено |
|---|---|---|
| `hello` | Печатает «Начинаем...» до и «Готово!» после | ✅ |
| `timer` | Печатает время выполнения с точностью 4 знака | ✅ |
| `retry` | Повторяет вызов при исключении, при исчерпании — `RuntimeError` | ✅ |

## Вывод

В ходе работы были изучены и реализованы три собственных декоратора. `hello` демонстрирует базовый принцип обёртки функции. `timer` измеряет время через `time.perf_counter()` и форматирует вывод f-строкой с 4 знаками. `retry` — декоратор с параметрами: повторяет вызов при исключении, логирует неудачные попытки, поддерживает паузу `delay` и после исчерпания попыток возбуждает `RuntimeError` через `raise ... from ...`. Все декораторы лежат в `decorators.py`, снабжены docstring, сохраняют метаданные через `functools.wraps` и проверены тестами `unittest`.
