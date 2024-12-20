from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: object) -> Self:
        if isinstance(other, tuple):
            if len(other) != 2:
                raise ValueError(
                    f"Tuple must be of length 2, recieved {len(other)}"
                )
            return self.__class__(self.x + other[0], self.y + other[1])
        elif isinstance(other, self.__class__):
            return self.__class__(self.x + other.x, self.y + other.y)
        else:
            raise ValueError(
                f"Unsupported object for addition: {type(other)}. Supported classes: tuple, Point"
            )

    def __sub__(self, other: object) -> Self:
        if isinstance(other, tuple):
            if len(other) != 2:
                raise ValueError(
                    f"Tuple must be of length 2, recieved {len(other)}"
                )
            return self.__class__(self.x - other[0], self.y - other[1])
        elif isinstance(other, self.__class__):
            return self.__class__(self.x - other.x, self.y - other.y)
        else:
            raise ValueError(
                f"Unsupported object for addition: {type(other)}. Supported classes: tuple, Point"
            )

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

    def abs(self) -> int:
        return abs(self.x) + abs(self.y)
