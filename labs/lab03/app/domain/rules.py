from abc import ABC, abstractmethod

from app.support.errors import DomainError
from app.support.types import Money, CheckResult
from app.domain.limits import LimitCheckContext


# Общий абстрактный класс для правил проверки лимитов.
class LimitRule(ABC):
    def __init__(self, maximum: Money):
        if not isinstance(maximum, Money):
            raise DomainError("INVALID_CONFIG")
        self._maximum = maximum

    @property
    def maximum(self):
        return self._maximum

    # Каждый наследник обязан реализовать собственную проверку.
    @abstractmethod
    def check(self, context: LimitCheckContext) -> CheckResult:
        pass


# Проверка максимальной суммы одной покупки.
class TransactionLimit(LimitRule):
    def check(self, context: LimitCheckContext) -> CheckResult:
        context.amount.same_currency(self.maximum)

        if context.amount.amount > self.maximum.amount:
            return CheckResult(False, "TRANSACTION_LIMIT_EXCEEDED")

        return CheckResult(True)


# Проверка расходов за день с учётом текущей покупки.
class DailyLimit(LimitRule):
    def check(self, context: LimitCheckContext) -> CheckResult:
        projected = context.projected_today()
        projected.same_currency(self.maximum)

        if projected.amount > self.maximum.amount:
            return CheckResult(False, "DAILY_LIMIT_EXCEEDED")

        return CheckResult(True)