import re
from typing import cast

class InvalidName(ValueError):
    pass

_validate_regex = re.compile(r"^[A-Za-z0-9._-]+$")

def canonicalize_name(name: str, *, validate: bool = False):
    if validate and not _validate_regex.fullmatch(name):
        raise InvalidName(f"name is invalid: {name!r}")
    value = name.lower().replace("_", "-").replace(".", "-")
    while "--" in value:
        value = value.replace("--", "-")
    return cast(str, value)
