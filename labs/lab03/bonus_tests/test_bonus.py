import pytest
from app import api
from app.support.errors import DomainError


def assert_code(code, operation):
    with pytest.raises(DomainError) as error:
        operation()
    assert error.value.code == code

from decimal import Decimal
from app.support.types import Money, money, CheckResult

def test_custom_code_keeps_default():
    from app.domain.limits import LimitCheckContext
    from app.domain.rules import TransactionLimit
    item = LimitCheckContext(money("100"), money("0"), money("0"))
    assert TransactionLimit(money("50")).check(item).code == "TRANSACTION_LIMIT_EXCEEDED"
    assert TransactionLimit(money("50"), code="CUSTOM").check(item).code == "CUSTOM"
    assert_code("INVALID_CONFIG", lambda: TransactionLimit(money("50"), code=""))
