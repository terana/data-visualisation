from scipy.optimize import linprog
import math


class DummyVerticesMinimisation:
    def __init__(self, graph):
        self.graph = graph
        self.layers = []

    def dump_layers(self):
        for l in self.layers:
            node_ids = [n.id for n in l]
            print(" ".join(node_ids))
        print(f"Total layers: {len(self.layers)}")

    def calculate_layers(self):
        if not self._optimise():
            raise RuntimeError("Couldn't optimise the number of dummy vertices.")

        self._add_dummy_vertices()

    def _optimise(self):
        obj = []
        const = - len(self.graph.edges())
        idx = 0
        # Minimising: SUM(yu - yv - 1)
        for n in self.graph.nodes():
            coef = len(n.children()) - len(n.parent())
            obj.append(coef)
            n.idx = idx
            idx += 1

        lhs_ineq = []
        rhs_ineq = []
        # yu - yv >=1 -> -yu + yv <= -1
        for e in self.graph.edges():
            ineq = [0] * len(self.graph.nodes())
            ineq[e.node1.idx] = -1
            ineq[e.node2.idx] = 1
            lhs_ineq.append(ineq)
            rhs_ineq.append(-1)

        # yv >= 1
        bnd = [(1, math.inf)] * len(self.graph.nodes())

        opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq, bounds=bnd, method="revised simplex")

        print(f"{opt.message}")
        print(f"Iterations made: {opt.nit}")
        if opt.success:
            print(f"Minimal number of dummy vertices: {opt.fun + const}")
            for n in self.graph.nodes():
                n.y = round(opt.x[n.idx])
                while len(self.layers) < n.y:
                    self.layers.append([])
                self.layers[-n.y].append(n)
        return opt.success

    # TODO: extract this to the DAG implementation!
    def _add_dummy_vertices(self):
        n_dummies = 0
        for layer in self.layers:
            for n in layer:
                n.dummy = False
                for p in n.parent():
                    if p.y - n.y > 1:
                        prev = p
                        for y in range(p.y - 1, n.y, -1):
                            d = self.graph.add_node(id=f"d{n_dummies}")
                            n_dummies += 1
                            self.graph.add_edge(prev, d)
                            prev = d
                            d.dummy = True
                            d.y = y
                            # layer starts from 0, y starts from 1
                            self.layers[-y].append(d)
                        self.graph.add_edge(prev, n)
        pass
