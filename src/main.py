from datavis.LabelPlacement import LabelPlacement

if __name__ == "__main__":
    lp = LabelPlacement()
    lp.generate_labels()
    lp.calculate_placement()
    lp.draw_labels()
