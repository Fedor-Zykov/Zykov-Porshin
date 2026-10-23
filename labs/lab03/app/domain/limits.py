from app.support.errors import DomainError
from app.support.types import Money


class LimitCheckContext:
    def __init__(
        self,
        amount: Money,
        spent_today: Money,
        spent_month: Money,
        contactless: bool = False,
        spent_week: Money | None = None,
    ):
        if not all(
            isinstance(value, Money)
            for value in (amount, spent_today, spent_month)
        ):
            raise DomainError("INVALID_CONTEXT")

        if type(contactless) is not bool:
            raise DomainError("INVALID_CONTEXT")

        if amount.amount <= 0:
            raise DomainError("INVALID_AMOUNT")

        amount.same_currency(spent_today)
        amount.same_currency(spent_month)

        if spent_today.amount > spent_month.amount:
            raise DomainError("INVALID_CONTEXT")

        # Проверяем недельные расходы, если они переданы.
        if spent_week is not None:
            if not isinstance(spent_week, Money):
                raise DomainError("INVALID_CONTEXT")

            amount.same_currency(spent_week)

            if spent_today.amount > spent_week.amount:
                raise DomainError("INVALID_CONTEXT")

        self._amount = amount
        self._spent_today = spent_today
        self._spent_month = spent_month
        self._contactless = contactless
        self._spent_week = spent_week

    @property
    def amount(self) -> Money:
        return self._amount

    @property
    def spent_today(self) -> Money:
        return self._spent_today

    @property
    def spent_month(self) -> Money:
        return self._spent_month

    @property
    def contactless(self) -> bool:
        return self._contactless

    @property
    def spent_week(self) -> Money | None:
        return self._spent_week

    def projected_today(self) -> Money:
        return self.spent_today.add(self.amount)

    # Расходы за неделю с учётом новой покупки.
    def projected_week(self) -> Money:
        if self.spent_week is None:
            raise DomainError("INVALID_CONTEXT")

        return self.spent_week.add(self.amount)