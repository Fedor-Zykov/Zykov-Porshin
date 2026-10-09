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

def context(amount="50", today="100", month="200", contactless=False):
    from app.domain.limits import LimitCheckContext
    return LimitCheckContext(money(amount), money(today), money(month), contactless)


def test_zero_purchase_is_rejected():
    assert_code("INVALID_AMOUNT", lambda: context("0", "0", "0"))


@pytest.mark.parametrize("different", ["today", "month"])
def test_context_rejects_mixed_currencies(different):
    from app.domain.limits import LimitCheckContext
    today = money("0", "USD" if different == "today" else "EUR")
    month = money("0", "USD" if different == "month" else "EUR")
    assert_code("CURRENCY_MISMATCH", lambda: LimitCheckContext(money("1"), today, month))


def test_today_cannot_exceed_month():
    assert_code("INVALID_CONTEXT", lambda: context("1", "100", "99.99"))


def test_equal_and_zero_counters_are_valid():
    assert context("1", "100", "100").projected_today() == money("101")
    assert context("1", "0", "0").projected_today() == money("1")


@pytest.mark.parametrize("attribute,value", [
    ("amount", money("0")), ("spent_today", money("999")),
    ("spent_month", money("0")), ("contactless", True),
])
def test_context_public_fields_are_read_only(attribute, value):
    item = context()
    with pytest.raises(AttributeError):
        setattr(item, attribute, value)
    assert item.amount == money("50")
    assert item.spent_today == money("100")


def test_false_result_requires_reason():
    assert_code("INVALID_RESULT", lambda: CheckResult(False))
    assert_code("INVALID_RESULT", lambda: CheckResult(True, "UNEXPECTED"))
