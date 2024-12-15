from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: tuple[int, int]) -> Self:
        return self.__class__(self.x + other[0], self.y + other[1])
