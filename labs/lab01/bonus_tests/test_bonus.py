import pytest
from app import api
from app.support.errors import DomainError


def assert_code(code, operation):
    with pytest.raises(DomainError) as error:
        operation()
    assert error.value.code == code

from decimal import Decimal
from app.support.types import Money, money, CheckResult

def test_context_description():
    from app.domain import limits
    assert hasattr(limits, "LimitCheckContext"), "Сначала выполните обязательную ЛР1"
    item = limits.LimitCheckContext(money("50"), money("100"), money("200"))
    assert item.describe() == "50.00 EUR; today=100.00 EUR"
