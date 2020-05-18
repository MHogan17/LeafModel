from random import uniform
from Unit import Unit
from Gradient import Gradient
from scipy.optimize import fsolve


class Array:
    def __init__(self, length=100, width=100):
        self.temp_grad = Gradient(200)
        self.array = []
        self.length = length
        self.width = width

        self.wheel = {}
        for i in range(length):
            self.array.append([])
            for j in range(width):
                self.array[i].append(Unit(i=i, j=j))

    def randomize(self):
        for i in range(len(self.array)):
            for unit in self.array[i]:
                unit.set_chi(uniform(.25, .35))
                #unit.set_temperature(uniform(275, 325))

    def find_color(self, i, j):
        unit = self.array[i][j]
        temp = int(unit.get_temperature() * 100)

        if temp < 29500:
            return self.temp_grad[0]
        elif temp > 30500:
            return self.temp_grad[len(self.temp_grad) - 1]
        else:
            return self.temp_grad[(temp - 29500) // 5]

    def calculate_next(self, current_time, environment):
        neighbors_water = []
        neighbors_carbon = []
        self.wheel[current_time % 5] = []
        for i in range(len(self.array)):
            self.wheel[current_time % 5].append([])
            for unit in self.array[i]:
                neighbors_water.clear()
                neighbors_carbon.clear()
                neighbors_water.append(self.array[i][unit.get_col()].epid.get_epid_water_potential())
                neighbors_carbon.append(self.array[i][unit.get_col()].get_carbon_dioxide())
                try:
                    neighbors_water.append(self.array[i + 1][unit.get_col()].epid.get_epid_water_potential())
                    neighbors_water.append(self.array[i + 1][unit.get_col()].get_carbon_dioxide())
                except IndexError:
                    pass
                try:
                    neighbors_water.append(self.array[i - 1][unit.get_col()].epid.get_epid_water_potential())
                    neighbors_carbon.append(self.array[i - 1][unit.get_col()].get_carbon_dioxide())
                except IndexError:
                    pass
                try:
                    neighbors_water.append(self.array[i][unit.get_col() + 1].epid.get_epid_water_potential())
                    neighbors_carbon.append(self.array[i][unit.get_col() + 1].get_carbon_dioxide())
                except IndexError:
                    pass
                try:
                    neighbors_water.append(self.array[i][unit.get_col() - 1].epid.get_epid_water_potential())
                    neighbors_carbon.append(self.array[i][unit.get_col() - 1].get_carbon_dioxide())
                except IndexError:
                    pass
                self.wheel[current_time % 5][i].append((neighbors_carbon, neighbors_water))

        for i in range(len(self.array)):
            for unit in self.array[i]:
                try:
                    neighbors_carbon = self.wheel[(current_time - 4) % 5][i][unit.get_col()][0]
                except KeyError:
                    neighbors_carbon = self.wheel[current_time % 5][i][unit.get_col()][0]
                neighbors_water = self.wheel[current_time % 5][i][unit.get_col()][1]

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
        return

    def __getitem__(self, item):
        return self.array[item]

    def __repr__(self):
        return str(self.array)

    def __len__(self):
        return len(self.array)








