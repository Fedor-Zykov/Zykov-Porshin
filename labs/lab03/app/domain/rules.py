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
    def maximum(self) -> Money:
        return self._maximum

    # Общая проверка валюты и превышения максимальной суммы.
    def _check_amount(self, amount: Money, code: str) -> CheckResult:
        amount.same_currency(self.maximum)

        if amount.amount > self.maximum.amount:
            return CheckResult(False, code)

        return CheckResult(True)

    # Каждый наследник обязан реализовать собственную проверку.
    @abstractmethod
    def check(self, context: LimitCheckContext) -> CheckResult:
        pass


# Проверка максимальной суммы одной покупки.
class TransactionLimit(LimitRule):
    def check(self, context: LimitCheckContext) -> CheckResult:
        return self._check_amount(
            context.amount,
            "TRANSACTION_LIMIT_EXCEEDED",
        )


# Проверка расходов за день с учётом текущей покупки.
class DailyLimit(LimitRule):
    def check(self, context: LimitCheckContext) -> CheckResult:
        return self._check_amount(
            context.projected_today(),
            "DAILY_LIMIT_EXCEEDED",
        )
# Проверка расходов за неделю с учётом текущей покупки.
class WeeklyLimit(LimitRule):
    def check(self, context: LimitCheckContext) -> CheckResult:
        # Если недельные расходы не переданы, пропускаем это правило.
        if context.spent_week is None:
            return CheckResult(True)

        return self._check_amount(
            context.projected_week(),
            "WEEKLY_LIMIT_EXCEEDED",
        )