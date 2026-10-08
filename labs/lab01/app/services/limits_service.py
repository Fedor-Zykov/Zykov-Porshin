"""Purchase and daily limits with adapters for the existing API."""
from app.domain.limits import LimitCheckContext
from app.support.types import CheckResult, money


class LimitsService:
    def __init__(self):
        self.transaction_maximum = money("500")
        self.daily_maximum = money("1000")

    def check(self, context: LimitCheckContext) -> CheckResult:
        context.amount.same_currency(self.transaction_maximum)
        context.amount.same_currency(self.daily_maximum)
        if context.amount.amount > self.transaction_maximum.amount:
            return CheckResult(False, "TRANSACTION_LIMIT_EXCEEDED")
        if context.projected_today().amount > self.daily_maximum.amount:
            return CheckResult(False, "DAILY_LIMIT_EXCEEDED")
        return CheckResult(True)


def new_service() -> LimitsService:
    return LimitsService()


def check_values(service, amount, spent_today, spent_month, contactless=False):
    context = LimitCheckContext(amount, spent_today, spent_month, contactless)
    return service.check(context)


def projected_values(amount, spent_today, spent_month, contactless=False):
    context = LimitCheckContext(amount, spent_today, spent_month, contactless)
    return context.projected_today()
