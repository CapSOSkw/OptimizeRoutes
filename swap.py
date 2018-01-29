
class Swap():

    def __init__(self, x):
        self.x = x

    def swap(self, i, j):
        self.x[i], self.x[j] = self.x[j], self.x[i]
        return self.x

class array(list):
    def swap(self, i, j):
        self[i], self[j] = self[j], self[i]

if __name__ == '__main__':
    pass