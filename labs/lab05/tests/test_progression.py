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

from app.domain.rules import LimitRule
from app.services.limits_service import LimitsService
from app.support.types import CheckResult

def test_progression_limit_control_called_once_per_request():
    calls = []
    class Once(LimitRule):
        def check(self, context):
            calls.append(context)
            if len(calls) == 1: raise DomainError("TEMPORARY")
            return CheckResult(True)
    rules = [Once(money("100"))]
    service = LimitsService(rules)
    rules.clear()
    context = LimitCheckContext(money("10"), money("0"), money("0"))
    code("TEMPORARY", lambda: service.check(context))
    assert len(calls) == 1
    assert service.check(context).allowed and len(calls) == 2

from app.services.limits_service import LimitsService
from app.support.types import CheckResult

def test_progression_extra_lab05(monkeypatch):
    calls = []
    def check(self, value):
        calls.append(value)
        return CheckResult(False, "LIMIT") if value == 2 else CheckResult(True)
    monkeypatch.setattr(LimitsService, "check", check)
    service = object.__new__(LimitsService)
    assert [r.allowed for r in service.check_many([1, 2, 3])] == [True, False, True]
    index, result = service.first_denial([1, 2, 3])
    assert index == 1 and result.code == "LIMIT"
    assert calls == [1, 2, 3, 1, 2]
    assert service.first_denial([1, 3]) is None
