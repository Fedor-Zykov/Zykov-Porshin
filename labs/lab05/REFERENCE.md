# Limits: справка для ЛР5

Контекст содержит сумму покупки и накопленные расходы за день и месяц. Правила проверяют ограничения, но не обновляют расходы.

Здесь перечислены типы текущей работы. Что требуется реализовать и какие файлы можно менять, указано в [TASK.md](TASK.md).

## Предметные объекты и исполнители

| Тип и конструктор | Публичные действия и свойства | Файл |
|---|---|---|
| `LegacyLimitAdapter(legacy, currency='EUR')` | `check(context)` | `app/domain/adapters.py` |
| `LimitCheckContext(amount: Money, spent_today: Money, spent_month: Money, contactless: bool=False)` | `amount`, `spent_today`, `spent_month`, `contactless`, `projected_today()`, `projected_month()` | `app/domain/limits.py` |
| `LimitRule(maximum: Money)` | `maximum`, `check(context: LimitCheckContext)` | `app/domain/rules.py` |
| `TransactionLimit(maximum: Money)` | `check(context: LimitCheckContext)` | `app/domain/rules.py` |
| `DailyLimit(maximum: Money)` | `check(context: LimitCheckContext)` | `app/domain/rules.py` |

Свойства читаются без скобок. Поля объекта-значения не меняются присваиванием; результат операции создаётся отдельно. Для наследника без собственного конструктора показаны аргументы конструктора базового класса.

## Вызов сервиса

| Метод | Сигнатура |
|---|---|
| `__init__` | `LimitsService(rules: Iterable[LimitRule])` |
| `check` | `check(context: LimitCheckContext)` |
| `check_many` | `check_many(contexts)` |
| `first_denial` | `first_denial(contexts)` |

`app/api.py` — готовая внешняя граница; не изменяйте её. Вызов попадает в сервис из указанного модуля. Подробные примеры создания входных объектов находятся в открытых тестах текущей папки.

В `app/services/assembly.py` находятся стандартные конфигурации. Переданный объект сохраняется, а отсутствие обозначается `None`. Пустой список или словарь не равен отсутствию настройки. Копия контейнера не означает копирования исполнителей.

Сигнатура сборки: `build_service()`.

## Готовые результаты и ошибки

`DomainError` находится в `app/support/errors.py`; код доступен через `error.code`. В разрешённых методах используйте готовые проверки, а не новую иерархию исключений.

`CheckResult(True)` означает разрешение. `CheckResult(False, code)` означает отказ, а не изменение статуса объекта. Некорректный тип результата правила вызывает `INVALID_RESULT`. При записи или списании сервис преобразует предусмотренный отказ в `DomainError` до изменения данных.

`Money` хранит `Decimal` и валюту. Для учебных данных используются EUR и USD. Заданная сумма создаётся готовой `money("10", "EUR")`; арифметика выполняется готовыми методами Money. Курс и коэффициент не округляются как денежная сумма. В Account денежный модуль — `app/domain/money.py`, в остальных вариантах он предоставлен в `app/support/`.

## Проверка поведения

`tests/test_contract.py` и `tests/test_review_contract.py` проверяют предметные правила. `tests/test_progression.py` проверяет последовательности обращений и настройки текущей работы. Ни один результат теста не является командой менять защищённый API или тесты.

Ожидаемый стартовый результат — в [STARTER-STATE.md](STARTER-STATE.md). Проверка из корня проекта: `python check.py lab05`.
