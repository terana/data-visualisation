from datavis.LabelPlacement import LabelPlacement

if __name__ == "__main__":
    lp = LabelPlacement(canvas_width=250, canvas_height=250)
    lp.load_labels("samples/labels/hard1.txt")
    if not lp.calculate_placement():
        print("No solution for label placement.")
    else:
        lp.draw_labels()
