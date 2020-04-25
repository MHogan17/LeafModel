from random import uniform
from Unit import Unit
from Gradient import Gradient
from scipy.optimize import fsolve
from GradientPainter import GradientPainter
import os

from tkinter import Tk, PhotoImage, Canvas, mainloop


class Array:
    def __init__(self, length=100, width=100):
        self.temp_grad = Gradient(100)
        self.__array = []
        self.window = Tk()
        self.length = length
        self.width = width
        self.photo = PhotoImage(width=self.length, height=self.width)
        self.canvas = Canvas(self.window, width=self.length, height=self.width, bg='#ffffff')
        self.canvas.create_image((self.length / 2, self.width / 2), image=self.photo, state="normal")
        for i in range(length):
            self.__array.append([])
            for j in range(width):
                self.__array[i].append(Unit(i=i, j=j))

    def randomize(self):
        for i in range(len(self.__array)):
            for unit in self.__array[i]:
                unit.set_chi(uniform(.25, .35))

    def __find_color(self, temp):
        temp = int(temp)
        if temp < 275:
            return self.temp_grad[0]
        elif temp > 325:
            return self.temp_grad[len(self.temp_grad) - 1]
        else:
            return self.temp_grad[temp - 275]

    def calculate_next(self, current_time, max_time, environment, array):
        if current_time > max_time:
            return
        neighbors_carbon = [1]
        neighbors_water = [1]
        for i in range(len(array)):
            for unit in array[i]:
                color = self.__find_color(unit.get_temperature())
                self.paint(color, unit.get_row(), unit.get_col())
                '''
                TODO: Find a better way to set up counter for neighbors
                '''
                average_carbon = sum(neighbors_carbon) / len(neighbors_carbon)
                average_water = sum(neighbors_water) / len(neighbors_water)
                unit.calculate_next(average_water)
                x, y = fsolve(unit.solve_for_temperature, (environment.get_ambient_temperature(), environment.get_ambient_water()))
                unit.set_temperature(x)
                unit.set_es_water_vapor(y)
                unit.set_es_water_potential(unit.calculate_es_water_potential(environment.get_ambient_water()))
                unit.set_carbon_dioxide(unit.calculate_carbon_dioxide(0, environment.get_ambient_carbon(), average_carbon))
                unit.guard.set_guard_signal(unit.guard.calculate_guard_signal(0, 0,
                                                                              unit.get_carbon_dioxide()))
                unit.epid.set_epid_signal(unit.epid.calculate_epid_signal(0, unit.get_carbon_dioxide()))
                unit.guard.set_guard_water_potential(unit.guard.calculate_guard_water_potential(
                    unit.get_temperature()))
                unit.epid.set_epid_water_potential(unit.epid.calculate_epid_water_potential(
                    unit.get_temperature()))
                unit.set_pore_water_vapor(unit.calculate_pore_water_vapor(environment.get_ambient_water()))
                unit.set_pore_water_potential(unit.calculate_pore_water_potential())

        self.save("Minute" + str(current_time))
        self.calculate_next(current_time + 1, max_time, environment, array)

    def paint(self, color, i, j):
        self.photo.put(color, (i,  j))
        self.canvas.pack()
        self.window.update()

    def save(self, name):
        self.photo.write(name + '.png', 'png')


    def __getitem__(self, item):
        return self.__array[item]

    def __repr__(self):
        return str(self.__array)

    def __len__(self):
        return len(self.__array)
