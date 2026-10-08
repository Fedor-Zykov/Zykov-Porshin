"""Data belonging to one independent limit check."""
from dataclasses import dataclass

from app.support.types import Money


@dataclass(frozen=True)
class LimitCheckContext:
    amount: Money
    spent_today: Money
    spent_month: Money
    contactless: bool = False

    def projected_today(self) -> Money:
        return self.spent_today.add(self.amount)

    def describe(self) -> str:
        return f"{self.amount}; today={self.spent_today}"
