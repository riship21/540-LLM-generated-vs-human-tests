from packaging.version import Version, InvalidVersion

class InvalidSdistFilename(ValueError):
    pass

def canonicalize_name(name: str) -> str:
    value = name.lower().replace("_", "-").replace(".", "-")
    while "--" in value:
        value = value.replace("--", "-")
    return value

def parse_sdist_filename(filename: str):
    if filename.endswith(".tar.gz"):
        file_stem = filename[: -len(".tar.gz")]
    elif filename.endswith(".zip"):
        file_stem = filename[: -len(".zip")]
    else:
        raise InvalidSdistFilename(
            f"Invalid sdist filename (extension must be '.tar.gz' or '.zip'): {filename!r}"
        )

    name_part, sep, version_part = file_stem.rpartition("-")
    if not sep:
        raise InvalidSdistFilename(f"Invalid sdist filename: {filename!r}")

    name = canonicalize_name(name_part)
    try:
        version = Version(version_part)
    except InvalidVersion as e:
        raise InvalidSdistFilename(
            f"Invalid sdist filename (invalid version): {filename!r}"
        ) from e

    return (name, version)
