from app.support.types import CheckResult, money


def new_service():
    return {"transaction_maximum": money("500"), "daily_maximum": money("1000")}


def check_values(service, amount, spent_today, spent_month, contactless=False):
    context = {"amount": amount, "spent_today": spent_today,
               "spent_month": spent_month, "contactless": contactless}
    amount.same_currency(service["transaction_maximum"])
    amount.same_currency(service["daily_maximum"])
    if context["amount"].amount > service["transaction_maximum"].amount:
        return CheckResult(False, "TRANSACTION_LIMIT_EXCEEDED")
    projected = context["spent_today"].add(context["amount"])
    if projected.amount > service["daily_maximum"].amount:
        return CheckResult(False, "DAILY_LIMIT_EXCEEDED")
    return CheckResult(True)


def projected_values(amount, spent_today, spent_month, contactless=False):
    return spent_today.add(amount)
