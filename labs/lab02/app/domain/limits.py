from app.support.errors import DomainError
from app.support.types import Money


class LimitCheckContext:
    def __init__(self, amount: Money, spent_today: Money, spent_month: Money,
                 contactless: bool = False):
        if not all(isinstance(value, Money) for value in (amount, spent_today, spent_month)):
            raise DomainError("INVALID_CONTEXT")
        if type(contactless) is not bool:
            raise DomainError("INVALID_CONTEXT")
        if amount.amount <= 0:
                raise DomainError("INVALID_AMOUNT")
        for spent in (spent_today, spent_month):
            amount.same_currency(spent)
        if spent_today.amount > spent_month.amount:
            raise DomainError("INVALID_CONTEXT")
        self._amount = amount
        self._spent_today = spent_today
        self._spent_month = spent_month
        self._contactless = contactless

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

    def projected_today(self) -> Money:
        return self.spent_today.add(self.amount)
