from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, localcontext
from app.support.errors import DomainError


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "EUR"

    def __post_init__(self):
        value = self.amount
        if not isinstance(value, Decimal) or not value.is_finite() or value < 0:
            raise DomainError("INVALID_AMOUNT")
        if self.currency not in ("EUR", "USD"):
            raise DomainError("INVALID_CURRENCY")
        try:
            with localcontext() as ctx:
                ctx.prec = 28
                rounded = value.quantize(Decimal("0.01"))
        except InvalidOperation as exc:
            raise DomainError("INVALID_AMOUNT") from exc
        if rounded != value:
            raise DomainError("INVALID_AMOUNT")
        if rounded == 0:
            rounded = Decimal("0.00")
        object.__setattr__(self, "amount", rounded)

    def same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise DomainError("CURRENCY_MISMATCH")

    def add(self, other: "Money") -> "Money":
        self.same_currency(other)
        with localcontext() as ctx:
            ctx.prec = 28
            return Money(self.amount + other.amount, self.currency)

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"


def money(amount: str, currency: str = "EUR") -> Money:
    try:
        return Money(Decimal(amount), currency)
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise DomainError("INVALID_AMOUNT") from exc


@dataclass(frozen=True)
class CheckResult:
    allowed: bool
    code: str | None = None

    def __post_init__(self):
        if type(self.allowed) is not bool:
            raise DomainError("INVALID_RESULT")
        if self.allowed and self.code is not None:
            raise DomainError("INVALID_RESULT")
        if not self.allowed and (not isinstance(self.code, str) or not self.code.strip()):
            raise DomainError("INVALID_RESULT")


class LegacyAmountLimit:
    """Локальная зависимость для бонуса; не хранит историю."""

    def __init__(self, maximum: Decimal):
        self.maximum = maximum

    def accepts(self, amount_decimal: Decimal) -> bool:
        return amount_decimal <= self.maximum
