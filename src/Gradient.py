from colour import Color


class Gradient:
    def __init__(self, length=100):
        self.grad = []
        cold = Color('black')
        hot = Color('white')
        for c in cold.range_to(hot, length):
            self.grad.append(c.get_hex_l())

    def get_color(self, n):
        return self.grad[n - 1]

    def __len__(self):
        return len(self.grad)

    def __getitem__(self, item):
        return self.grad[item]
