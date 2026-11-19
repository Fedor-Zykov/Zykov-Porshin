from app.domain.rules import TransactionLimit, DailyLimit
from app.support.types import money

_DEFAULT_RULES = [TransactionLimit(money("500")), DailyLimit(money("1000"))]

from collections.abc import Iterable
from app.domain.limits import LimitCheckContext
from app.domain.rules import LimitRule
from app.support.errors import DomainError
from app.support.types import CheckResult


class LimitsService:
    def __init__(self, rules: Iterable[LimitRule]):
        self._rules = _DEFAULT_RULES  # ЛР5: переданные rules игнорируются

    def check(self, context: LimitCheckContext) -> CheckResult:
        raise NotImplementedError("ЛР5: реализуйте LimitsService.check по TASK.md")

    def check_many(self, contexts):
        raise NotImplementedError("ЛР5: реализуйте LimitsService.check_many по TASK.md")

    def first_denial(self, contexts):
        raise NotImplementedError("ЛР5: реализуйте LimitsService.first_denial по TASK.md")


def check_values(service, amount, spent_today, spent_month, contactless=False):
    context = LimitCheckContext(amount, spent_today, spent_month, contactless)
    return service.check(context)


def projected_values(amount, spent_today, spent_month, contactless=False):
    return LimitCheckContext(amount, spent_today, spent_month, contactless).projected_today()
