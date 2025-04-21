def mul(x: int = 1, y: int = 1) -> int:
    return x * y


def append_hello(s: str | None = None) -> str:
    if s is None:
        return "hello"
    return s + "hello"


def append_world(s: str | None = "hello") -> str:
    if s is None:
        return "world"
    return s + "world"
