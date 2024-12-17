from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: tuple[int, int]) -> Self:
        return self.__class__(self.x + other[0], self.y + other[1])

    def __eq__(self, other: object) -> bool:
        if isinstance(other, tuple):
            return (
                (self.x == other[0])
                and (self.y == other[1])
                and (len(other) == 2)
            )
        elif isinstance(other, self.__class__):
            return (self.x == other.x) and (self.y == other.y)
        else:
            return False

    def __lt__(self, other: Self) -> bool:
        return self.x < other.x

    def __le__(self, other: Self) -> bool:
        return self.x <= other.x
