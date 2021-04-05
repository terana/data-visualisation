import math


class CoffmanGraham:
    lexicographical_inf = "Z"
    lexicographical_zero = "0"

    def __init__(self, graph, width):
        self.graph = graph
        self.width = width

    def _init_order(self):
        for node in self.graph.nodes:
            node.label = self.lexicographical_inf

    @staticmethod
    def _get_input(node):
        input = ""
        for p in node.parents():
            input += p.label

        return input

    def _sort(self):
        unvisited = self.graph.nodes()
        if len(unvisited) < 1:
            return
        unvisited[0].label = "1"
        next = 2
        while len(unvisited):
            min_input = self._get_input(unvisited[0])
            min_input_node = unvisited[0]
            for node in unvisited:
                input = self._get_input(node)
                if input < min_input:
                    min_input = input
                    min_input_node = node

            min_input_node.number = f"{next}"
            unvisited.remove(min_input_node)

    @staticmethod
    def _all_children_in_list(node, l):
        children = node.children()
        # Zero set is subset of any set
        return set(children).issubset(set(l))

    @staticmethod
    def _no_children_in_list(node, l):
        children = node.children()
        for child in children:
            if child in l:
                return False

        return True

    def _set_layers(self):
        unvisited = self.graph.nodes
        visited = []
        curr_layer = 0
        curr_layer_nodes = []
        while len(unvisited) > 0:
            max_label = self.lexicographical_zero
            # TODO: smth more elegant?
            max_label_node = None
            for node in unvisited:
                if node.label > max_label and self._all_children_in_list(node, visited):
                    max_label = node.label
                    max_label_node = node

            if not (len(curr_layer_nodes) < self.width
                    and self._no_children_in_list(max_label_node, curr_layer_nodes)):
                curr_layer += 1
                curr_layer_nodes = []

            curr_layer_nodes.append(max_label_node)
            max_label_node.y = curr_layer
