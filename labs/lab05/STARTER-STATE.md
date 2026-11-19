# Исходные проверки ЛР5

Успешных проверок: **27**. Ожидаемых падений: **19**.

Не завершены использование переданных зависимостей, сборка и основной путь операции. Проверки вызывают разные конфигурации и ошибающегося исполнителя; ошибка не должна превращаться в успешный результат или повторную операцию.

Падения ниже связаны с конкретными требованиями [TASK.md](TASK.md). После обязательной части все они должны пройти. Бонус проверяется отдельно и не входит в эти числа.

## Новые последовательности и конфигурации

- `tests.test_progression::test_progression_extra_lab05`
- `tests.test_progression::test_progression_limit_control_called_once_per_request`
- `tests.test_progression::test_progression_limit_denial_is_not_cached`

## Предметный контракт и общий интерфейс

- `tests.test_contract::test_checks_do_not_write_history`
- `tests.test_contract::test_container_is_copied_not_the_rules`
- `tests.test_contract::test_dependency_error_propagates_without_changing_context`
- `tests.test_contract::test_empty_rules_do_not_remove_context_validation`
- `tests.test_contract::test_existing_boundaries[100-900-None]`
- `tests.test_contract::test_existing_boundaries[100.01-900-DAILY_LIMIT_EXCEEDED]`
- `tests.test_contract::test_existing_boundaries[50-100-None]`
- `tests.test_contract::test_existing_boundaries[500-0-None]`
- `tests.test_contract::test_existing_boundaries[500.01-0-TRANSACTION_LIMIT_EXCEEDED]`
- `tests.test_contract::test_existing_boundaries[600-900-TRANSACTION_LIMIT_EXCEEDED]`
- `tests.test_contract::test_failure_short_circuits_following_rule`
- `tests.test_contract::test_first_refusal_wins_in_configured_order`
- `tests.test_contract::test_rule_is_called_in_real_path`
- `tests.test_contract::test_two_injected_configurations_differ`
- `tests.test_contract::test_wrong_result_is_not_permission`
- `tests.test_review_contract::test_review_injected_rules_run_in_order_and_only_once`

## Порядок проверки

Из корня проекта: `python check.py lab05`. Сначала прочитайте первый traceback и ожидаемый результат сценария. Не отключайте тесты, которые пока не проходят.

Ошибка импорта или установки не относится к заданию. Если исходный набор результатов отличается, сохраните вывод и сообщите преподавателю; не удаляйте решения и служебные файлы.
