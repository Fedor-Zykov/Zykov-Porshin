from app.domain.limits import LimitCheckContext
from app.support.types import CheckResult, money


class LimitsService:
    def __init__(self):
        self._transaction_maximum = money("500")
        self._daily_maximum = money("1000")

    def check(self, context: LimitCheckContext) -> CheckResult:
        context.amount.same_currency(self._transaction_maximum)
        context.amount.same_currency(self._daily_maximum)
        if context.amount.amount > self._transaction_maximum.amount:
            return CheckResult(False, "TRANSACTION_LIMIT_EXCEEDED")
        if context.projected_today().amount > self._daily_maximum.amount:
            return CheckResult(False, "DAILY_LIMIT_EXCEEDED")
        return CheckResult(True)


def new_service():
    return LimitsService()


def check_values(service, amount, spent_today, spent_month, contactless=False):
    context = LimitCheckContext(amount, spent_today, spent_month, contactless)
    return service.check(context)


def projected_values(amount, spent_today, spent_month, contactless=False):
    return LimitCheckContext(amount, spent_today, spent_month, contactless).projected_today()
