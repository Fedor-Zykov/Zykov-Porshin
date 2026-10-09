"""Готовая внешняя граница. HTTP и изменение API не нужны."""
from app.services.assembly import build_service
from app.services import limits_service as implementation


def create():
    return build_service()


def check(service, amount, spent_today, spent_month, contactless=False):
    return implementation.check_values(service, amount, spent_today, spent_month, contactless)


def projected_today(amount, spent_today, spent_month, contactless=False):
    return implementation.projected_values(amount, spent_today, spent_month, contactless)
