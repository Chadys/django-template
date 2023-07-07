import enum


class EnvMode(enum.Enum):
    TEST = enum.auto()
    DEV = enum.auto()
    QA = enum.auto()
    PROD = enum.auto()
    DEMO = enum.auto()


def add_ending_slash(url: str) -> str:
    if url.endswith("/"):
        return url
    return f"{url}/"


def remove_ending_slash(url: str) -> str:
    if url.endswith("/"):
        return url[:-1]
    return url
