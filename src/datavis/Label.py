from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Point:
    x: int
    y: int
    id: int = None

    def __add__(self, that: Point):
        return Point(that.x + self.x, that.y + self.y)

    def __sub__(self, that: Point):
        return Point(self.x - that.x, self.y - that.y)

    def __neg__(self):
        return Point(- self.x, - self.y)

    def __str__(self):
        return f"{self.x},{self.y}"

    def __repr__(self):
        return f"{self.x},{self.y}"

    @staticmethod
    def parse(string):
        x, y = parse_ints(string)
        return Point(x, y)

    def in_rectangle(self, r: Rectangle):
        return r.ul.x <= self.x <= r.lr.x and r.ul.y <= self.y <= r.lr.y


@dataclass
class Rectangle:
    ul: Point  # Upper left corner.
    lr: Point  # Lower right corner.

    def height(self):
        return self.lr.y - self.ul.y

    def width(self):
        return self.lr.x - self.ul.x

    def overlaps(self, other: Rectangle):
        return (self.ul.y <= other.ul.y <= self.lr.y or other.ul.y <= self.ul.y <= other.lr.y) and \
               (self.ul.x <= other.ul.x <= self.lr.x or other.ul.x <= self.ul.x <= other.lr.x)

    def inside(self, other: Rectangle):
        return self.ul.in_rectangle(other) and self.lr.in_rectangle(other)


@dataclass()
class Label:
    length: int
    height: int
    point: Point  # Data point this label is describing.
    placements: List[Point]  # List of upper left corners of rectangles which can represent this label.
    chosen_placement: Point = None

    def __init__(self, string):
        """
        Creates Label from string with data point position, length and height,
        relative placement options separated with tabs, e.g.
        25,20	10,10	0,0 10,0 0,10 10,10
        Here, the relative placement option is a position (x,y) of data point inside the label,
        0,0 is for the upper left corner.
        :param string: sting with Label data
        """
        arr = string.split('\t')
        self.point = Point.parse(arr[0])
        self.length, self.height = parse_ints(arr[1])
        relative_placements = [Point.parse(pos) for pos in arr[2].split(' ')]
        self.placements = [self.point - rp for rp in relative_placements]

    def __str__(self):
        placements = " ".join([str(self.point - p) for p in self.placements])
        return f"{self.point}\t{self.length},{self.height}\t{placements}"


def parse_ints(string):
    x, y = string.split(',')
    return int(x), int(y)
