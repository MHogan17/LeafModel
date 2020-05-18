from GuardCell import Guard
from EpidermalCell import Epidermal
from math import exp, log


class Unit:
    __R = 8.314
    __VOLUME = 0.000018
    __K_C = .005
    __SIGMA = 0.01
    __R_INT = .1
    __LAMBDA_G = .1
    __LAMBDA_E = 1.6
    __LATENT_HEAT = 40.8
    __W_O = 2.251 * 10 ** 9
    __T_W = 5387
    __M = 2
    __PHI_CC = .3
    __PHI_EE = .6

    def __init__(self, i, j, temperature=295, carbon_dioxide=80, pore_water_potential=-1.2,
                 es_water_potential=-.5, conductance=.18, pore_water_vapor=27, es_water_vapor=28, k_ae=50, chi=.15):
        self.__row = i
        self.__col = j
        self.__temperature = temperature
        self.__conductance = conductance
        self.__carbon_dioxide = carbon_dioxide
        self.__pore_potential = pore_water_potential
        self.__pore_vapor = pore_water_vapor
        self.__es_vapor = es_water_vapor
        self.__es_potential = es_water_potential
        self.__k_ae = k_ae
        self.__chi = chi
        self.guard = Guard()
        self.epid = Epidermal()

    def get_row(self):
        return self.__row

    def get_col(self):
        return self.__col

    def get_temperature(self):
        return self.__temperature

    def set_temperature(self, temperature):
        self.__temperature = temperature

    def get_conductance(self):
        return self.__conductance

    def set_conductance(self, conductance):
        self.__conductance = conductance

    def get_carbon_dioxide(self):
        return self.__carbon_dioxide

    def set_carbon_dioxide(self, carbon_dioxide):
        self.__carbon_dioxide = carbon_dioxide

    def get_pore_water_potential(self):
        return self.__pore_potential

    def set_pore_water_potential(self, water):
        self.__pore_potential = water

    def get_pore_water_vapor(self):
        return self.__pore_vapor

    def set_pore_water_vapor(self, water_vapor):
        self.__pore_vapor = water_vapor

    def get_es_water_potential(self):
        return self.__es_potential

    def set_es_water_potential(self, water):
        self.__es_potential = water

    def get_es_water_vapor(self):
        return self.__es_vapor

    def set_es_water_vapor(self, water_vapor):
        self.__es_vapor = water_vapor

    def set_k_ae(self, k_ae):
        self.__k_ae = k_ae

    def get_k_ae(self):
        return self.__k_ae

    def get_chi(self):
        return self.__chi

    def set_chi(self, chi):
        self.__chi = chi

    # Equation 9
    def calculate_pore_water_potential(self):
        return (self.__R * self.__temperature / self.__VOLUME * log(self.__pore_vapor / self.__es_vapor)) * 10 ** -6

    # Equation 3
    def calculate_carbon_dioxide(self, total_intensity, ambient_carbon, average_carbon):
        return self.__conductance * ambient_carbon + average_carbon * self.__PHI_CC / \
               (self.__conductance + self.__K_C * total_intensity + self.__PHI_CC) + .0001

    # Equation 8
    def calculate_pore_water_vapor(self, ambient_water):
        if self.__conductance != 0:
            return self.__SIGMA * ambient_water + (1 - self.__SIGMA) * self.__es_vapor
        else:
            return self.__es_vapor

    # Equation 2
    def calculate_es_water_potential(self, ambient_water):
        return -self.__R_INT * self.__conductance * (self.__es_vapor - ambient_water)

    # Equation 11
    def calculate_RHS_guard(self):
        return self.__LAMBDA_G * (self.__pore_potential - self.guard.get_guard_water_potential())

    # Equation 10
    def calculate_RHS_epid(self, average_water):
        return self.__LAMBDA_E * (self.__es_potential - self.epid.get_epid_water_potential() + self.__PHI_EE *
                                  (average_water - self.epid.get_epid_water_potential()))

    # Equation 1
    def solve_for_temperature(self, p, *data):
        x, y = p
        temp, absorbed, water = data
        return (x - temp - (absorbed - self.__LATENT_HEAT * self.__conductance *
                                           (y - water)) / (2 * self.__k_ae), y - self.__W_O *
                exp(-self.__T_W / x))

    def calculate_next(self, average_water, step=1):
        # Equation 12
        self.guard.set_guard_pressure(self.guard.get_guard_pressure() + step * self.calculate_RHS_guard())
        if self.guard.get_guard_pressure() < 0:
            self.guard.set_guard_pressure(0)
        # Equation 13
        self.epid.set_epid_pressure(self.epid.get_epid_pressure() + step * self.calculate_RHS_epid(average_water))
        if self.epid.get_epid_pressure() < 0:
            self.epid.set_epid_pressure(0)
        # Equation 14
        new_cond = self.__chi * (self.guard.get_guard_pressure() - self.__M * self.epid.get_epid_pressure())
        if new_cond <= 0:
            self.set_conductance(0.00000001)
        elif new_cond >= 1:
            self.set_conductance(1)
        else:
            self.set_conductance(new_cond)

    def __repr__(self):
        return str(self.__conductance)

    def __float__(self):
        return float(self.__conductance)

