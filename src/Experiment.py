from Array import Array
from Environment import Environment
from ArrayPainter import paint_array
import os
import time

def ExperimentFactory(name):
    if name == 'light':
        print('Valid experiment')
        return Light()
    elif name == 'humidity':
        print('Also a valid experiment')
        return Humidity()
    else:
        raise RuntimeError('Invalid experiment type.')


class Experiment:
    def __init__(self):
        self.array = Array()
        self.environment = Environment()

    def run(self):
        raise(RuntimeError("'run' is not defined for this experiment type"))

    def save(self):
        save = input("Would you like to save the experiment?")
        if save.lower() == 'y':
            pass
        else:
            pass


class Light(Experiment):
    def run(self):
        start = time.time()
        self.environment.set_total_intensity(0)
        self.array.randomize()
        t = 0
        while t < 5:
            self.array.calculate_next(t, self.environment)
            paint_array(self.array, str(t))
            t += 1
        self.environment.set_total_intensity(700)
        self.environment.set_blue_intensity(0)
        while t < 30:
            self.array.calculate_next(t, self.environment)
            paint_array(self.array, str(t))
            t += 1
        end = time.time()
        runtime = end - start
        print("This simulation took " + str(round(runtime / 60)) + " minutes.")
        #self.save()


class Humidity(Experiment):
    def run(self):
        print("This is a humidity experiment.")
