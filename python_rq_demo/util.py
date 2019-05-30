def mask(value: str) -> str:
    """Convert a string to asterisks."""
    if value is None:
        return ''
    else:
        return '*' * len(value)
