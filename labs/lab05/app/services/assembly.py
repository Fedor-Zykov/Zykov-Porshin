from app.services.limits_service import LimitsService
from app.domain.rules import TransactionLimit, DailyLimit
from app.support.types import money

def build_service():
    # ЛР5: стандартные правила нужно создавать здесь, не в сервисе.
    return LimitsService((
        TransactionLimit(money("500")),  # Лимит одной покупки — 500
        DailyLimit(money("1000")),  # Лимит расходов за день — 1000
    ))
