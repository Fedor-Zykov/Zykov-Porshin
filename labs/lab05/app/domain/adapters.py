class LegacyLimitAdapter:
    def __init__(self, legacy, currency="EUR"):
        self._legacy = legacy
        self._currency = currency

    def check(self, context):
        raise NotImplementedError("Дополнительное задание ЛР5")
