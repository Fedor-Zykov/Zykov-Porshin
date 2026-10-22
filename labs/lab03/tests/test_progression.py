import pytest
from datetime import date, datetime, timezone
from decimal import Decimal
from app import api
from app.support.errors import DomainError


def code(expected, operation):
    with pytest.raises(DomainError) as caught:
        operation()
    assert caught.value.code == expected

from app.domain.limits import LimitCheckContext
from app.support.types import money

def test_progression_limit_denial_is_not_cached():
    service = api.create()
    good = LimitCheckContext(money("20"), money("950"), money("950"))
    bad = LimitCheckContext(money("70"), money("950"), money("950"))
    assert service.check(good).allowed
    assert service.check(bad).code == "DAILY_LIMIT_EXCEEDED"
    assert service.check(good).allowed
    assert good.spent_today == bad.spent_today == money("950")
