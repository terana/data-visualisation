from datavis.Label import Label, Point, Rectangle
from typing import Dict
from pysat.solvers import Glucose3
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List
from random import randrange


class LabelPlacement:
    canvas_width: int = 500
    canvas_height: int = 500
    labels: List[Label] = None
    _point_by_id: Dict[int, Point] = {}
    _label_by_id: Dict[int, Label] = {}

    def __init__(self, canvas_width=None, canvas_height=None):
        if canvas_width:
            self.canvas_width = canvas_width
        if canvas_height:
            self.canvas_height = canvas_height

    def load_labels(self, filename):
        with open(filename) as f:
            lines = f.readlines()
        self.labels = [Label(line) for line in lines]

    def store_labels(self, filename):
        pass

    def generate_labels(self, tightness=400):
        self.labels = []
        placed = []
        padding = 5
        while tightness > 0:
            w = randrange(50) + 10
            h = randrange(40) + 10
            x0 = [padding + randrange(self.canvas_width - w), padding + randrange(self.canvas_height - h)]
            rect = [x0[0], x0[1], x0[0] + w, x0[1] + h]
            overlap = False
            for placedRect in placed:
                if self._is_overlap(Point(rect[0], rect[1]), Point(rect[2], rect[3]),
                                    Point(placedRect[0], placedRect[1]), Point(placedRect[2], placedRect[3])):
                    overlap = True
                    tightness -= 1
                    break

            if overlap:
                continue
            placed.append(rect)
            offsets = []
            k1 = randrange(3) * randrange(2) + 1
            k2 = randrange(3) * randrange(2) + 1
            for j in range(k1 + 1):
                for i in range(k2 + 1):
                    arr = [i // k2 * w, j // k1 * h]
                    offsets.append(arr)

            if len(offsets) < 1:
                continue

            chosen_index = randrange(len(offsets))
            pos = Point(offsets[chosen_index][0] + x0[0], offsets[chosen_index][1] + x0[1])

            offsets = [f"{x},{y}" for x, y in offsets]
            line = f"{pos}\t{w},{h}\t{' '.join(offsets)}"
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
        plt.axis([-frame, self.canvas_width + frame, -frame, self.canvas_height + frame])
        plt.grid(with_grid)
        self._invert_axis(ax)
        ax.set_aspect('equal', adjustable='box')

        for l in self.labels:
            plt.plot(l.point.x, l.point.y, 'ko')
            x, y = l.chosen_placement.x, l.chosen_placement.y
            rect = patches.Rectangle((x, y), l.length, l.height, linewidth=2, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
        plt.show()

    def calculate_placement(self):
        canvas = Rectangle(ul=Point(0, 0), lr=Point(self.canvas_height, self.canvas_width))
        clauses = []
        next_id = 1
        for l in self.labels:
            for p in l.placements:
                p.id = next_id
                next_id += 1
                self._point_by_id[p.id] = p
                self._label_by_id[p.id] = l
            for p in l.placements:
                rect = Rectangle(ul=p, lr=Point(p.x + l.length, p.y + l.height))
                if not rect.inside(canvas):
                    clauses.append([-p.id])
                for i in range(p.id + 1, next_id):
                    clauses.append([-p.id, -i])  # X_p.id -> !X_i
            clauses.append([p.id for p in l.placements])  # At least one should be chosen

        for i, label1 in enumerate(self.labels):
            for label2 in self.labels[i + 1:]:
                clauses.extend(self._get_clauses(label1, label2))

        g = Glucose3()
        for c in clauses:
            g.add_clause(c)
        if not g.solve():
            # No solution.
            return False

        model = g.get_model()
        for x in model:
            id = abs(x)
            if x > 0:
                self._label_by_id[id].chosen_placement = self._point_by_id[id]

        return True

    @classmethod
    def _get_clauses(cls, label1: Label, label2: Label):
        clauses = []
        for p1 in label1.placements:
            for p2 in label2.placements:
                if cls._is_overlap(p1, p1 + Point(label1.length, label1.height), p2,
                                   p2 + Point(label2.length, label2.height)):
                    clauses.append([-p1.id, -p2.id])

        return clauses

    @staticmethod
    def _is_overlap(upper_left1: Point, lower_right1: Point, upper_left2: Point, lower_right2: Point):
        return (
                       upper_left1.y <= upper_left2.y <= lower_right1.y or upper_left2.y <= upper_left1.y <= lower_right2.y) and \
               (upper_left1.x <= upper_left2.x <= lower_right1.x or upper_left2.x <= upper_left1.x <= lower_right2.x)
