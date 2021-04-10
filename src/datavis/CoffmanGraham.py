class CoffmanGraham:
    lexicographical_inf = "Z"

    def __init__(self, graph, width):
        self.graph = graph
        self.width = width
        self.layers = []

    def calculate(self):
        self._sort_nodes()
        self._set_layers()

    def damp_layers(self):
        max_width = 0
        for layer in self.layers:
            node_ids = [node.id for node in layer]
            print(" ".join(node_ids))
            max_width = max(max_width, len(node_ids))

        print(f"Total layers: {len(self.layers)}")
        print(f"Max width: {max_width}")

    def _init_order(self):
        for node in self.graph.nodes():
            node["label"] = self.lexicographical_inf

    @staticmethod
    def _get_input(node):
        input = []
        for p in node.parent():
            input.append(p["label"])

        return sorted(input, reverse=True)

    def _sort_nodes(self):
        self._init_order()

        unvisited = self.graph.nodes()[:]
        next = 1
        while len(unvisited):
            min_input = self._get_input(unvisited[0])
            min_input_node = unvisited[0]
            for node in unvisited:
                input = self._get_input(node)
                if input < min_input:
                    min_input = input
                    min_input_node = node

            min_input_node["label"] = next
            unvisited.remove(min_input_node)
            next += 1

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
        unvisited = self.graph.nodes()[:]
        visited = []
        curr_layer = 0
        curr_layer_nodes = []
        while len(unvisited) > 0:
            max_label = 0
            # TODO: smth more elegant?
            max_label_node = None
            for node in unvisited:
                label = int(node["label"])
                if label > max_label and self._all_children_in_list(node, visited):
                    max_label = label
                    max_label_node = node

            if not (len(curr_layer_nodes) < self.width and self._no_children_in_list(max_label_node, curr_layer_nodes)):
                curr_layer += 1
                self.layers.append(curr_layer_nodes)
                curr_layer_nodes = []

            curr_layer_nodes.append(max_label_node)
            max_label_node.y = curr_layer
            unvisited.remove(max_label_node)
            visited.append(max_label_node)

        self.layers.append(curr_layer_nodes)
