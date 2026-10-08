import pytest
from app import api
from app.support.errors import DomainError


def assert_code(code, operation):
    with pytest.raises(DomainError) as error:
        operation()
    assert error.value.code == code

from decimal import Decimal
from app.support.types import Money, CheckResult, money


@pytest.mark.parametrize("amount,today,code", [
    ("50", "100", None),
    ("500", "0", None),
    ("500.01", "0", "TRANSACTION_LIMIT_EXCEEDED"),
    ("100", "900", None),
    ("100.01", "900", "DAILY_LIMIT_EXCEEDED"),
    ("600", "900", "TRANSACTION_LIMIT_EXCEEDED"),
])
def test_existing_boundaries(amount, today, code):
    result = api.check(api.create(), money(amount), money(today), money(today))
    assert result == CheckResult(code is None, code)


def test_projected_total_counts_purchase_once():
    today = money("100")
    assert api.projected_today(money("50"), today, money("200")) == money("150")
    assert today == money("100")


def test_checks_do_not_write_history():
    service = api.create()
    amount, today, month = money("50"), money("100"), money("200")
    first = api.check(service, amount, today, month)
    second = api.check(service, amount, today, month)
    assert first == second == CheckResult(True)
    assert (amount, today, month) == (money("50"), money("100"), money("200"))


def test_contexts_do_not_share_data():
    first = api.projected_today(money("50"), money("100"), money("200"))
    second = api.projected_today(money("20"), money("0"), money("0"))
    assert (first, second) == (money("150"), money("20"))


@pytest.mark.parametrize("invalid", [Decimal("-1"), Decimal("NaN"), Decimal("Infinity"), Decimal("1.001"), 1.0])
def test_provided_money_rejects_invalid_amounts(invalid):
    assert_code("INVALID_AMOUNT", lambda: Money(invalid, "EUR"))


def test_provided_money_is_an_immutable_value():
    assert money("1.000") == money("1.00")
    assert str(money("-0")) == "0.00 EUR"
    amount = money("1.00")
    with pytest.raises((AttributeError, TypeError)):
        amount.amount = Decimal("9")
    assert_code("CURRENCY_MISMATCH", lambda: amount.add(money("1", "USD")))
