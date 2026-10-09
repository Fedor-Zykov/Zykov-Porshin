import pytest
from app import api
from app.support.errors import DomainError


def assert_code(code, operation):
    with pytest.raises(DomainError) as error:
        operation()
    assert error.value.code == code

from decimal import Decimal
from app.support.types import Money, money, CheckResult

def test_projected_month_without_mutation():
    from app.domain.limits import LimitCheckContext
    item = LimitCheckContext(money("50"), money("100"), money("200"))
    assert item.projected_month() == money("250")
    assert item.projected_today().amount <= item.projected_month().amount
    assert item.spent_month == money("200")
