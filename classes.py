from dataclasses import dataclass
import math
import pygame
import glob


@dataclass
class Point:
    """
    Represents a pixel on the canvas.
    """

    x: int | float
    y: int | float

    def __str__(self):
        return f"[{self.x}, {self.y}]"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        if isinstance(scalar, self.__class__):
            return Point(self.x * scalar.x, self.y * scalar.y)
        elif isinstance(scalar, tuple):
            return Point(self.x * scalar[0], self.y * scalar[1])
        else:
            return Point(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        if isinstance(scalar, self.__class__):
            return Point(self.x / scalar.x, self.y / scalar.y)
        elif isinstance(scalar, tuple):
            return Point(self.x / scalar[0], self.y / scalar[1])
        else:
            return Point(self.x / scalar, self.y / scalar)

    def __len__(self):
        return int(math.sqrt(self.x ** 2 + self.y ** 2))

    def tuple(self):
        return self.x, self.y


@dataclass
class GridCoordinate(Point):
    """
    Represents a coordinate on the map grid.
    """

    x: int
    y: int

    def __str__(self):
        return f"[{self.x}, {self.y}]"

    def __floordiv__(self, scalar):
        if isinstance(scalar, self.__class__):
            return Point(self.x // scalar.x, self.y // scalar.y)
        elif isinstance(scalar, tuple):
            return Point(self.x // scalar[0], self.y // scalar[1])
        else:
            return Point(self.x // scalar, self.y // scalar)

    def get_above(self):
        return GridCoordinate(self.x, self.y - 1)

    def get_below(self):
        return GridCoordinate(self.x, self.y + 1)

    def get_left(self):
        return GridCoordinate(self.x - 1, self.y)

    def get_right(self):
        return GridCoordinate(self.x + 1, self.y)

    def get_surrounding(self):
        surrounding_gc = []
        for rx in range(-1, 2):
            for ry in range(-1, 2):
                if not (rx == 0 and ry == 0):
                    surrounding_gc.append(GridCoordinate(self.x + rx, self.y + ry))

        return surrounding_gc
