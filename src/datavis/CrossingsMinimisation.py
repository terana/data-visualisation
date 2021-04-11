import statistics
from functools import cmp_to_key


class CrossingsMinimisation:
    MEDIAN = 1
    BARYCENTRIC = 2

    def __init__(self, layers):
        self.layers = layers

    def calculate(self):
        self._place_nodes(method=self.MEDIAN)

        max_iterations = 100
        crossings = 0
        for i in range(max_iterations):
            optimised, crossings = self._local_optimisation()
            if i % 10 == 0:
                print(f"Optimisation iteration {i}, total crossings: {crossings}")
            if not optimised:
                break
        print(f"Final crossings: {crossings}")

    @staticmethod
    def _init_layer(layer):
        next_x = 0
        for node in layer:
            node.x = next_x
            next_x += 1

    @staticmethod
    def _x_median(nodes):
        return statistics.median([node.x for node in nodes])

    @staticmethod
    def _x_mean(nodes):
        return statistics.mean([node.x for node in nodes])

    @classmethod
    def _calculate_x(cls, nodes, method):
        if len(nodes) < 1:
            return 0
        if method == cls.MEDIAN:
            return round(cls._x_median(nodes))
        else:
            return round(cls._x_mean(nodes))

    @staticmethod
    def _resolve_collision(x, occupied):
        if x not in occupied or len(occupied) < 1:
            return x

        step = 1
        while True:
            if x + step not in occupied:
                return x + step
            if x - step not in occupied:  # Can go to negative x-es.
                return x - step
            step += 1

    def _place_nodes(self, method=MEDIAN):
        if len(self.layers) < 1:
            return

        self._init_layer(self.layers[0])

        for layer in self.layers[1:]:
            occupied = []
            for node in layer:
                x = self._calculate_x(node.parent(), method)
                x = self._resolve_collision(x, occupied)
                occupied.append(x)
                node.x = x

    @staticmethod
    def _num_nodes_crossed(should_be_before, should_be_after):
        res = 0
        for n in should_be_before:
            for m in should_be_after:
                if m.x < n.x:
                    res += 1
        return res

    @staticmethod
    def _sort_by_x(layer):
        def compare(n1, n2):
            return n1.x - n2.x

        return sorted(layer, key=cmp_to_key(compare))

    @classmethod
    def _calculate_crossings(cls, layer):
        # children needed
        crossings = 0
        for i, n in enumerate(layer):
            for m in layer[i + 1:]:
                crossings += cls._num_nodes_crossed(n.parent(), m.parent())
                crossings += cls._num_nodes_crossed(n.children(), m.children())

        return crossings

    def _local_optimisation(self):
        # Expect edges to be placed only between neighbour layers (or achieving that with adding dummy vertices).
        if len(self.layers) < 2:
            return

        layers = []
        for layer in self.layers:
            layers.append(self._sort_by_x(layer))
        self.layers = layers

        optimised = False
        total_crossings = 0

        for l, layer in enumerate(self.layers[1:-1]):
            crossings = self._calculate_crossings(layer)
            total_crossings += crossings
            if crossings == 0:
                continue
            for i, ni in enumerate(layer):
                if crossings == 0:
                    break

                for j, nj in enumerate(layer):
                    if i == j:
                        continue

                    swapped = layer.copy()
                    swapped[i] = layer[j]
                    swapped[j] = layer[i]
                    swapped_crossings = self._calculate_crossings(swapped)
                    if swapped_crossings < crossings:
                        layer[i] = swapped[i]
                        layer[j] = swapped[j]
                        self.layers[l] = layer
                        ni.x, nj.x = nj.x, ni.x
                        # bad idea to iterate a changed list, going to the next layer for now
                        # TODO: think of a better way, e.g. change a copy, then substitute
                        crossings = 0
                        optimised = True
                        break
        return optimised, crossings
