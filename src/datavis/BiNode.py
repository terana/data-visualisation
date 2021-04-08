from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BiNode:
    id: str = None
    left: BiNode = None
    right: BiNode = None
    x: int = None
    y: int = None

    def dump(self):
        print(f"{self.id}: x={self.x} y={self.y}")
