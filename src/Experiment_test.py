from GradientPainter import GradientPainter
from Array import Array
from Environment import Environment

array = Array()
array.randomize()

environment = Environment()

array.calculate_next(0, 1, environment, array)
