import pytest
from decimal import Decimal
from datetime import date, datetime, timezone, timedelta
from app import api
from app.support.errors import DomainError


def assert_code(code, action):
    with pytest.raises(DomainError) as caught:
        action()
    assert caught.value.code == code

from app.support.types import money

def test_review_injected_rules_run_in_order_and_only_once():
    from app.domain.limits import LimitCheckContext
    from app.domain.rules import LimitRule
    from app.services.limits_service import LimitsService
    from app.support.types import money,CheckResult
    calls=[]
    class Allow(LimitRule):
        def __init__(self,code):self.code=code
        def check(self,item):calls.append(self.code);return CheckResult(True)
    item=LimitCheckContext(money("10"),money("0"),money("0"))
    assert LimitsService([Allow("A"),Allow("B")]).check(item).allowed
    assert calls == ["A","B"]
