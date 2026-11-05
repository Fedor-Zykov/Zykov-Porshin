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
    def _check_amount(self, amount: Money, error_code: str) -> CheckResult:
        if amount.amount > self.maximum.amount:
            return CheckResult(False, error_code)
        return CheckResult(True)
    @abstractmethod
    def check(self, context: LimitCheckContext) -> CheckResult:
        raise NotImplementedError


class TransactionLimit(LimitRule):
    def check(self, context: LimitCheckContext) -> CheckResult:
        context.amount.same_currency(self.maximum)
        return self._check_amount(context.amount, "TRANSACTION_LIMIT_EXCEEDED")


class DailyLimit(LimitRule):
    def check(self, context: LimitCheckContext) -> CheckResult:
        context.amount.same_currency(self.maximum)
        return self._check_amount(context.projected_today(), "DAILY_LIMIT_EXCEEDED")
