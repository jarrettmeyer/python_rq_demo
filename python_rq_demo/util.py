def add_if_unique(target, source):
    """Adds unique items from source to target. Does not add item
    to the target if it is already present."""
    for item in source:
        if item not in target:
            target.append(item)
    return target


def mask(value: str) -> str:
    """Convert a string to asterisks."""
    if value is None:
        return ''
    else:
        return '*' * len(value)
