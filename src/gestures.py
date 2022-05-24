import pandas as pd

class Gestures:
    def __init__(self, classes_path):
        self.data = pd.read_csv(classes_path, sep=',', header=None)

    def get_available_gestures(self):
        return list(self.data.iloc[:, 0])

if __name__ == '__main__':
    gestures = Gestures(classes_path = '../assets/datasets/labels.csv')
    available_gestures = gestures.get_available_gestures()