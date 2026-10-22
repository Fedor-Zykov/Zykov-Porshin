from app.support.errors import DomainError
from app.support.types import Money, CheckResult
from app.domain.limits import LimitCheckContext


class LimitRule:
    def __init__(self, maximum: Money):
        if not isinstance(maximum, Money):
            raise DomainError("INVALID_CONFIG")
        self._maximum = maximum

    @property
    def maximum(self):
        return self._maximum

    # ЛР3: оформить ABC и общий контракт результата.
    def check(self, context: LimitCheckContext) -> CheckResult:
        return None


class TransactionLimit(LimitRule):
    # Перенести существующее транзакционное ограничение.
    pass


class DailyLimit(LimitRule):
    # Перенести существующее дневное ограничение.
    pass
