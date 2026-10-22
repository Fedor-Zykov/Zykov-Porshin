# Исходные проверки ЛР3

Успешных проверок: **18**. Ожидаемых падений: **18**.

Не завершены общий интерфейс, алгоритмы исполнителей и основной метод сервиса. Поэтому один незаполненный метод может вызвать несколько падений — это не несколько независимых задач.

Падения ниже связаны с конкретными требованиями [TASK.md](TASK.md). После обязательной части все они должны пройти. Бонус проверяется отдельно и не входит в эти числа.

## Новые последовательности и конфигурации

- `tests.test_progression::test_progression_limit_denial_is_not_cached`

## Предметный контракт и общий интерфейс

- `tests.test_contract::test_abstract_limit_cannot_be_instantiated`
- `tests.test_contract::test_both_rules_obey_boundaries[DailyLimit-0-0.01-0-DAILY_LIMIT_EXCEEDED]`
- `tests.test_contract::test_both_rules_obey_boundaries[DailyLimit-1000-100-900-None]`
- `tests.test_contract::test_both_rules_obey_boundaries[DailyLimit-1000-100.01-900-DAILY_LIMIT_EXCEEDED]`
- `tests.test_contract::test_both_rules_obey_boundaries[TransactionLimit-0-0.01-0-TRANSACTION_LIMIT_EXCEEDED]`
- `tests.test_contract::test_both_rules_obey_boundaries[TransactionLimit-500-500-0-None]`
- `tests.test_contract::test_both_rules_obey_boundaries[TransactionLimit-500-500.01-0-TRANSACTION_LIMIT_EXCEEDED]`
- `tests.test_contract::test_checks_do_not_write_history`
- `tests.test_contract::test_existing_boundaries[100-900-None]`
- `tests.test_contract::test_existing_boundaries[100.01-900-DAILY_LIMIT_EXCEEDED]`
- `tests.test_contract::test_existing_boundaries[50-100-None]`
- `tests.test_contract::test_existing_boundaries[500-0-None]`
- `tests.test_contract::test_existing_boundaries[500.01-0-TRANSACTION_LIMIT_EXCEEDED]`
- `tests.test_contract::test_existing_boundaries[600-900-TRANSACTION_LIMIT_EXCEEDED]`
- `tests.test_contract::test_rule_configuration_currency_must_match[DailyLimit]`
- `tests.test_contract::test_rule_configuration_currency_must_match[TransactionLimit]`
- `tests.test_contract::test_rule_is_called_in_real_path`

## Порядок проверки

Из корня проекта: `python check.py lab03`. Сначала прочитайте первый traceback и ожидаемый результат сценария. Не отключайте тесты, которые пока не проходят.

Ошибка импорта или установки не относится к заданию. Если исходный набор результатов отличается, сохраните вывод и сообщите преподавателю; не удаляйте решения и служебные файлы.
