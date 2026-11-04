class InvalidRangeError(ValueError):
    pass


class InvalidTupleOperationsError(ValueError):
    pass


class MigrationError(ValueError):
    pass


class StatsError(Exception):
    def __init__(self, code: str, details: str | None = None):
        self.code = code
        self.details = details
        super().__init__(f"StatsError: {code} (details: {details})")
