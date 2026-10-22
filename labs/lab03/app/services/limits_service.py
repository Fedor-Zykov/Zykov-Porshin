from app.domain.limits import LimitCheckContext
from app.domain.rules import TransactionLimit, DailyLimit
from app.support.errors import DomainError
from app.support.types import CheckResult, money


class LimitsService:
    def __init__(self):
        self._transaction_maximum = money("500")
        self._daily_maximum = money("1000")

        # Сначала проверяем одну покупку, затем расходы за день.
        self._rules = [
            TransactionLimit(self._transaction_maximum),
            DailyLimit(self._daily_maximum),
        ]

    def check(self, context: LimitCheckContext) -> CheckResult:
        # Принимаем только объект контекста проверки.
        if not isinstance(context, LimitCheckContext):
            raise DomainError("INVALID_CONTEXT")

        # Все правила вызываются через общий метод check().
        for rule in self._rules:
            result = rule.check(context)

            # Каждое правило обязано вернуть CheckResult.
            if not isinstance(result, CheckResult):
                raise DomainError("INVALID_RESULT")

            # При первом отказе завершаем проверку.
            if not result.allowed:
                return result

        # Все правила разрешили покупку.
        return CheckResult(True)


def new_service():
    return LimitsService()


def check_values(service, amount, spent_today, spent_month, contactless=False):
    context = LimitCheckContext(amount, spent_today, spent_month, contactless)
    return service.check(context)


def projected_values(amount, spent_today, spent_month, contactless=False):
    return LimitCheckContext(
        amount, spent_today, spent_month, contactless
    ).projected_today()