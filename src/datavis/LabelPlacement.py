from datavis.Label import Label, Point, Rectangle
from typing import Dict
from pysat.solvers import Glucose3
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List
from random import randrange


class LabelPlacement:
    """
    Solves label placement problem.
    Deals with unlimited number of possible label positions, solving a general Boolean Satisfiability problem.
    The B-SAT problem is formulated with variables corresponding to all the globally possible labels positions.
    In case position i of label1 overlaps position j of label2, the Xi -> !Xj clause is added to the problem.
    Additionally, clauses for restricting choice to exactly one position per label are added.
    """
    canvas: Rectangle
    labels: List[Label] = None
    _point_by_id: Dict[int, Point] = {}
    _label_by_id: Dict[int, Label] = {}

    def __init__(self, canvas_width=500, canvas_height=500):
        self.canvas = Rectangle(Point(0, 0), Point(canvas_width, canvas_height))

    def load_labels(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        self.labels = [Label(line) for line in lines]

    def store_labels(self, filename):
        lines = "\n".join([str(l) for l in self.labels])
        with open(filename, "w") as f:
            f.write(lines)

    def generate_labels(self, max_label_size=50, min_label_size=10, tightness=200):
        """
        Generates a random set of labels with random possible positions, not always possible non-overlapping placement.
        1. Places rectangles on canvas.
        2. Generates random number of possible point positions inside each rectangle.
        3. Chooses some of the position for placing data point.
        """
        self.labels = []
        placed = []
        padding = 5
        while tightness > 0:
            w = randrange(max_label_size - min_label_size) + min_label_size
            h = randrange(max_label_size - min_label_size) + min_label_size
            ul = Point(padding + randrange(self.canvas.width() - w),
                       padding + randrange(self.canvas.height() - h))
            rect = Rectangle(ul, ul + Point(w, h))

            overlap = False
            for placed_rect in placed:
                if rect.overlaps(placed_rect):
                    overlap = True
                    tightness -= 1
                    break

            if overlap:
                continue
            placed.append(rect)

            offsets = []
            k1 = randrange(4) * randrange(2) + 1
            k2 = randrange(4) * randrange(2) + 1
            for j in range(k1 + 1):
                for i in range(k2 + 1):
                    if (i / k2 * w).is_integer() and (j / k1 * h).is_integer():
                        offsets.append(Point(int(i / k2 * w), int(j / k1 * h)))

            point = ul + offsets[randrange(len(offsets))]

            offsets = [f"{p}" for p in offsets]
            line = f"{point}\t{w},{h}\t{' '.join(offsets)}"
            self.labels.append(Label(line))

    @staticmethod
    def _invert_axis(ax):
        """
        Moves the beginning of axis to the upper left corner.
        """
        ax.set_ylim(ax.get_ylim()[::-1])  # invert the Y axis
        ax.xaxis.tick_top()  # move the X axis
        ax.yaxis.tick_left()  # remove right Y ticks

    def draw_labels(self, with_grid=True):
        frame = 5
        fig, ax = plt.subplots()
        plt.axis([-frame, self.canvas.width() + frame, -frame, self.canvas.height() + frame])
        plt.grid(with_grid)
        self._invert_axis(ax)
        ax.set_aspect('equal', adjustable='box')

        for l in self.labels:
            plt.plot(l.point.x, l.point.y, 'ko')
            x, y = l.chosen_placement.x, l.chosen_placement.y
            rect = patches.Rectangle((x, y), l.length, l.height, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
        plt.show()

    def calculate_placement(self):
        clauses = []
        next_id = 1
        for l in self.labels:
            ids = []
            for p in l.placements:
                p.id = next_id
                next_id += 1
                ids.append(p.id)

                self._point_by_id[p.id] = p
                self._label_by_id[p.id] = l

                rect = Rectangle(ul=p, lr=Point(p.x + l.length, p.y + l.height))
                if not rect.inside(self.canvas):
                    clauses.append([-p.id])  # Impossible placement.

            clauses.append(ids)  # At least one placement should be chosen for a label.
            for i in ids:
                # Xi -> !Xj -- Only one placement per label can be chosen.
                clauses.extend([[-i, -j] for j in range(i + 1, next_id)])

        for i, label1 in enumerate(self.labels):
            for label2 in self.labels[i + 1:]:
                clauses.extend(self._get_overlap_clauses(label1, label2))

        return self._solve_sat_problem(clauses)

    @classmethod
    def _get_overlap_clauses(cls, label1: Label, label2: Label):
        clauses = []
        for p1 in label1.placements:
            r1 = Rectangle(p1, p1 + Point(label1.length, label1.height))
            for p2 in label2.placements:
                r2 = Rectangle(p2, p2 + Point(label2.length, label2.height))

                if r1.overlaps(r2):
                    clauses.append([-p1.id, -p2.id])

        return clauses

    def _solve_sat_problem(self, clauses):
        g = Glucose3()
        for c in clauses:
            g.add_clause(c)

        if not g.solve():
            # No solution.
            return False

        model = g.get_model()
        for x in model:
            if x > 0:
                self._label_by_id[abs(x)].chosen_placement = self._point_by_id[abs(x)]

        return True
