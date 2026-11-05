"""До ЛР5 сборка предоставляется готовой."""
from app.services.limits_service import new_service


def build_service():
    return new_service()
