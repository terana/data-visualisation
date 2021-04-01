
class Node:
    def __init__(self, id=None, left=None, right=None):
        """
        """
        self.id = id
        self.left = left
        self.right = right
        self.x = None
        self.y = None

    def dump(self):
        print(f"{self.id}: x={self.x} y={self.y}")
