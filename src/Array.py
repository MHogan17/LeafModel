from random import uniform
from Unit import Unit
from Gradient import Gradient
from scipy.optimize import fsolve


class Array:
    def __init__(self, length=100, width=100):
        self.temp_grad = Gradient(1000)
        self.array = []
        self.length = length
        self.width = width
        for i in range(length):
            self.array.append([])
            for j in range(width):
                self.array[i].append(Unit(i=i, j=j))

    def randomize(self):
        for i in range(len(self.array)):
            for unit in self.array[i]:
                unit.set_chi(uniform(.2, .35))
                '''
                if i < 10:
                    unit.set_chi(.1)
                elif i < 20:
                    unit.set_chi(.15)
                elif i < 30:
                    unit.set_chi(.2)
                elif i < 40:
                    unit.set_chi(.25)
                elif i < 50:
                    unit.set_chi(.3)
                elif i < 60:
                    unit.set_chi(.35)
                elif i < 70:
                    unit.set_chi(.4)
                elif i < 80:
                    unit.set_chi(.45)
                elif i < 90:
                    unit.set_chi(.5)
                else:
                    unit.set_chi(.55)'''

    def find_color(self, i, j):
        temp = int(self.array[i][j].get_temperature() * 1000)

        if temp < 295000:
            return self.temp_grad[0]
        elif temp > 305000:
            return self.temp_grad[len(self.temp_grad) - 1]
        else:
            return self.temp_grad[(temp - 295000) // 10]

    def calculate_next(self, environment, water, carbon):
        neighbors_water = []
        neighbors_carbon = []

        for i in range(len(self.array)):
            for unit in self.array[i]:
                neighbors_water.clear()
                neighbors_carbon.clear()
                try:
                    neighbors_water.append(water[i + 1][unit.get_col()].epid.get_epid_water_potential())
                    neighbors_carbon.append(carbon[i + 1][unit.get_col()].get_carbon_dioxide())
                except IndexError:
                    neighbors_water.append(water[0][unit.get_col()].epid.get_epid_water_potential())
                    neighbors_carbon.append(carbon[0][unit.get_col()].get_carbon_dioxide())
                try:
                    neighbors_water.append(water[i - 1][unit.get_col()].epid.get_epid_water_potential())
                    neighbors_carbon.append(carbon[i - 1][unit.get_col()].get_carbon_dioxide())
                except IndexError:
                    neighbors_water.append(water[len(water) - 1][unit.get_col()].epid.get_epid_water_potential())
                    neighbors_carbon.append(carbon[len(carbon) - 1][unit.get_col()].get_carbon_dioxide())
                try:
                    neighbors_water.append(water[i][unit.get_col() + 1].epid.get_epid_water_potential())
                    neighbors_carbon.append(carbon[i][unit.get_col() + 1].get_carbon_dioxide())
                except IndexError:
                    neighbors_water.append(water[i][0].epid.get_epid_water_potential())
                    neighbors_carbon.append(carbon[i][0].get_carbon_dioxide())
                try:
                    neighbors_water.append(water[i][unit.get_col() - 1].epid.get_epid_water_potential())
                    neighbors_carbon.append(carbon[i][unit.get_col() - 1].get_carbon_dioxide())
                except IndexError:
                    neighbors_water.append(water[i][len(water) - 1].epid.get_epid_water_potential())
                    neighbors_carbon.append(carbon[i][len(carbon) - 1].get_carbon_dioxide())

                average_carbon = sum(neighbors_carbon) / len(neighbors_carbon)
                average_water = sum(neighbors_water) / len(neighbors_water)

                unit.calculate_next(average_water)
                data = (environment.get_ambient_temperature(), environment.get_total_intensity() * 0.6,
                        environment.get_ambient_water())
                x, y = fsolve(unit.solve_for_temperature, (296, 30), args=data)
                unit.set_temperature(x)
                unit.set_es_water_vapor(y)
                unit.set_es_water_potential(unit.calculate_es_water_potential(environment.get_ambient_water()))
                unit.set_carbon_dioxide(unit.calculate_carbon_dioxide(environment.get_total_intensity(),
                                                                      environment.get_ambient_carbon(),
                                                                      average_carbon))
                unit.guard.set_guard_signal(unit.guard.calculate_guard_signal(environment.get_blue_intensity(),
                                                                              environment.get_total_intensity(),
                                                                              unit.get_carbon_dioxide()))
                unit.epid.set_epid_signal(unit.epid.calculate_epid_signal(environment.get_total_intensity(),
                                                                          unit.get_carbon_dioxide()))
                unit.guard.set_guard_water_potential(unit.guard.calculate_guard_water_potential(
                    unit.get_temperature()))
                unit.epid.set_epid_water_potential(unit.epid.calculate_epid_water_potential(
                    unit.get_temperature()))
                unit.set_pore_water_vapor(unit.calculate_pore_water_vapor(environment.get_ambient_water()))
                unit.set_pore_water_potential(unit.calculate_pore_water_potential())

        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                water[i][j].epid.set_epid_water_potential(self.array[i][j].epid.get_epid_water_potential())
                carbon[i][j].set_carbon_dioxide(self.array[i][j].get_carbon_dioxide())
        return

    def __getitem__(self, item):
        return self.array[item]

    def __repr__(self):
        return str(self.array)

    def __len__(self):
        return len(self.array)








