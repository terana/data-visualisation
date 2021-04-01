import math


class LayeredTreeDraw:
    def __init__(self, graph):
        self.graph = graph
        self.root = graph.root
        self.contour = []

    def set_coordinates(self):
        self._set_coordinates_with_dfs(self.root, 0, -1)
        self.contour = self._layered_tree_draw(self.root)

    def show(self):
        self.graph.show()

    def _set_coordinates_with_dfs(self, node, depth, num):
        if node is None:
            return num
        n = self._set_coordinates_with_dfs(node.left, depth + 1, num)
        node.y = depth
        node.x = n + 1
        return self._set_coordinates_with_dfs(node.right, depth + 1, n + 1)

    def _layered_tree_draw(self, node):
        if node is None:
            return []

        if node.left is None and node.right is None:
            return [(node.x, node.x)]

        contour_left = self._layered_tree_draw(node.left)
        contour_right = self._layered_tree_draw(node.right)

        shift = self._calculate_shift(contour_left, contour_right)
        contour = self._merge_contours(shift, contour_left, contour_right)
        self._shift_tree(node.right, shift)

        self._place_between_children(node)

        contour.insert(0, (node.x, node.x))

        return contour

    @staticmethod
    def _calculate_shift(contour_left, contour_right):
        max_shift = (-math.inf)
        depth = min(len(contour_left), len(contour_right))
        if depth == 0:
            return 0
        for i in range(depth):
            shift = contour_left[i][1] + 2 - contour_right[i][0]
            max_shift = max(max_shift, shift)

        return max_shift

    @staticmethod
    def _merge_contours(shift, contour_left, contour_right):
        contour = []

        for i in range(max(len(contour_left), len(contour_right))):
            if i < len(contour_right):
                right = contour_right[i][1] + shift
            else:
                # i must be < len(contour_left)
                right = contour_left[i][1]

            if i < len(contour_left):
                left = contour_left[i][0]
            else:
                # i must be < len(contour_right)
                left = contour_right[i][0]

            contour.append((left, right))

        return contour

    def _shift_tree(self, node, shift):
        if node is None:
            return
        node.x += shift
        self._shift_tree(node.left, shift)
        self._shift_tree(node.right, shift)

    @staticmethod
    def _place_between_children(node):
        if node.left is not None and node.right is not None:
            node.x = (node.left.x + node.right.x) // 2
        elif node.left is not None:
            node.x = node.left.x + 1
        else:
            node.x = node.right.x - 1
