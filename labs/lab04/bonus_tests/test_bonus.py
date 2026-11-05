import pytest
from app import api
from app.support.errors import DomainError


def assert_code(code, operation):
    with pytest.raises(DomainError) as error:
        operation()
    assert error.value.code == code

from decimal import Decimal
from app.support.types import Money, money, CheckResult

def test_monthly_diagnostic_delegates():
    from app.domain.limits import LimitCheckContext
    from app.services.limits_service import monthly_diagnostic
    class ControlContext(LimitCheckContext):
        def projected_month(self):
            return money("777")
    item = ControlContext(money("50"), money("100"), money("200"))
    assert monthly_diagnostic(item) == money("777")
