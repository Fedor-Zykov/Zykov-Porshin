from app.domain.limits import LimitCheckContext
from app.support.types import CheckResult, money


class LimitsService:
    def __init__(self):
        self._transaction_maximum = money("500")
        self._daily_maximum = money("1000")

    def check(self, context: LimitCheckContext) -> CheckResult:
        raise NotImplementedError("ЛР3: реализуйте LimitsService.check по TASK.md")


def new_service():
    return LimitsService()


def check_values(service, amount, spent_today, spent_month, contactless=False):
    context = LimitCheckContext(amount, spent_today, spent_month, contactless)
    return service.check(context)


def projected_values(amount, spent_today, spent_month, contactless=False):
    return LimitCheckContext(amount, spent_today, spent_month, contactless).projected_today()
