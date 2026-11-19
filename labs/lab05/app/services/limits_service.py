
from collections.abc import Iterable
from app.domain.limits import LimitCheckContext
from app.domain.rules import LimitRule
from app.support.errors import DomainError
from app.support.types import CheckResult


class LimitsService:
    def __init__(self, rules: Iterable[LimitRule]):
        self._rules = tuple(rules)  # Сохраняем переданные правила

    def check(self, context: LimitCheckContext) -> CheckResult:
        if not isinstance(context, LimitCheckContext):  # Проверяем тип данных покупки
            raise DomainError("INVALID_CONTEXT")  # Сообщаем о неправильном типе
        for rule in self._rules:  # Перебираем переданные правила по порядку
            result = rule.check(context)  # Вызываем проверку текущего правила
            if not isinstance(result, CheckResult):  # Проверяем тип результата
                raise DomainError("INVALID_RESULT")  # Правило вернуло неправильный результат
            if not result.allowed:  # Если правило запретило покупку
                return result  # Возвращаем первый отказ и прекращаем проверки
        return CheckResult(True)  # Все правила пройдены — покупка разрешена

    def check_many(self, contexts):
        return tuple(self.check(context) for context in contexts)  # Проверяем каждую покупку и возвращаем кортеж результатов

    def first_denial(self, contexts):
        for index, context in enumerate(contexts):  # Перебираем покупки с номерами от нуля
            result = self.check(context)  # Проверяем текущую покупку
            if not result.allowed:  # Если покупка запрещена
                return index, result  # Возвращаем номер и результат первого отказа
        return None  # Отказов нет


def check_values(service, amount, spent_today, spent_month, contactless=False):
    context = LimitCheckContext(amount, spent_today, spent_month, contactless)
    return service.check(context)


def projected_values(amount, spent_today, spent_month, contactless=False):
    return LimitCheckContext(amount, spent_today, spent_month, contactless).projected_today()
