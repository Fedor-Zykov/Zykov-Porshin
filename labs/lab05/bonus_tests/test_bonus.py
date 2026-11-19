import pytest
from app import api
from app.support.errors import DomainError


def assert_code(code, operation):
    with pytest.raises(DomainError) as error:
        operation()
    assert error.value.code == code

from decimal import Decimal
from app.support.types import Money, money, CheckResult

def test_legacy_limit_adapter():
    from app.domain.limits import LimitCheckContext
    from app.domain.rules import LimitRule
    from app.domain.adapters import LegacyLimitAdapter
    from app.support.types import LegacyAmountLimit
    adapter = LegacyLimitAdapter(LegacyAmountLimit(Decimal("50")))
    assert isinstance(adapter, LimitRule)
    assert adapter.maximum == money("50")
    for amount, allowed in [("50", True), ("50.01", False)]:
        item = LimitCheckContext(money(amount), money("0"), money("0"))
        assert adapter.check(item) == CheckResult(allowed, None if allowed else "TRANSACTION_LIMIT_EXCEEDED")
    item = LimitCheckContext(money("1", "USD"), money("0", "USD"), money("0", "USD"))
    assert_code("CURRENCY_MISMATCH", lambda: adapter.check(item))
