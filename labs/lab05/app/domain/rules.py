from abc import ABC, abstractmethod
from app.domain.limits import LimitCheckContext
from app.support.errors import DomainError
from app.support.types import Money, CheckResult


class LimitRule(ABC):
    def __init__(self, maximum: Money):
        if not isinstance(maximum, Money):
            raise DomainError("INVALID_CONFIG")
        self._maximum = maximum

    @property
    def maximum(self) -> Money:
        return self._maximum

    @abstractmethod
    def check(self, context: LimitCheckContext) -> CheckResult:
        raise NotImplementedError


class TransactionLimit(LimitRule):
    def check(self, context: LimitCheckContext) -> CheckResult:
        context.amount.same_currency(self.maximum)
        if context.amount.amount > self.maximum.amount:
            return CheckResult(False, "TRANSACTION_LIMIT_EXCEEDED")
        return CheckResult(True)


class DailyLimit(LimitRule):
    def check(self, context: LimitCheckContext) -> CheckResult:
        context.amount.same_currency(self.maximum)
        if context.projected_today().amount > self.maximum.amount:
            return CheckResult(False, "DAILY_LIMIT_EXCEEDED")
        return CheckResult(True)
