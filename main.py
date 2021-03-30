import pygraphml
import math
import networkx as nx
import matplotlib.pyplot as plt

from Node import Node

parser = pygraphml.GraphMLParser()
g = parser.parse("test_trees/tree-42n.xml")


def dfs(node, depth, num):
    if node is None:
        return num
    n = dfs(node.left, depth + 1, num)
    node.y = depth
    node.x = n + 1
    return dfs(node.right, depth + 1, n + 1)


def calculate_shift(contour_left, contour_right):
    max_shift = (-math.inf)
    depth = min(len(contour_left), len(contour_right))
    if depth == 0:
        return 0
    for i in range(depth):
        shift = contour_left[i][1] + 2 - contour_right[i][0]
        max_shift = max(max_shift, shift)

    return max_shift


def merge_contours(shift, contour_left, contour_right):
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


def shift_tree(node, shift):
    if node is None:
        return
    node.x += shift
    shift_tree(node.left, shift)
    shift_tree(node.right, shift)


def place_between_children(node):
    if node.left is not None and node.right is not None:
        node.x = (node.left.x + node.right.x) // 2
    elif node.left is not None:
        node.x = node.left.x + 1
    else:
        node.x = node.right.x - 1


def layered_tree_draw(node):
    if node is None:
        return []

    if node.left is None and node.right is None:
        return [(node.x, node.x)]

    contour_left = layered_tree_draw(node.left)
    contour_right = layered_tree_draw(node.right)

    shift = calculate_shift(contour_left, contour_right)
    contour = merge_contours(shift, contour_left, contour_right)
    shift_tree(node.right, shift)

    place_between_children(node)

    contour.insert(0, (node.x, node.x))

    return contour


n10 = Node("n10")
n9 = Node("n9")
n8 = Node("n8")
n7 = Node("n7", n9, n10)
n6 = Node("n6")
n5 = Node("n5")
n4 = Node("n4", n5, n6)
n3 = Node("n3", right=n4)
n2 = Node("n2", n7, n8)
n1 = Node("n1", n3)
n0 = Node("n0", n1, n2)

dfs(n0, 0, -1)
layered_tree_draw(n0)

n0.dump()
n1.dump()
n2.dump()
n3.dump()
n4.dump()
n5.dump()
n6.dump()
n7.dump()
n8.dump()
n9.dump()
n10.dump()


def add_node(g, n):
    g.add_node(n.id, pos=(n.x, -n.y))

    if n.left is not None:
        add_node(g, n.left)
        g.add_edge(n.id, n.left.id)

    if n.right is not None:
        add_node(g, n.right)
        g.add_edge(n.id, n.right.id)


G = nx.DiGraph()
add_node(G, n0)

# G.add_node("n0", pos=(0, 0))
# G.add_node("n1", pos=(-50, -50))
# G.add_node("n2", pos=(50, -50))
#
# G.add_edge("n0", "n1")
# G.add_edge("n0", "n2")
nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=False, node_size=15)
plt.show()
