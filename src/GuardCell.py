class Guard:
    __GAMMA_GO = 525
    __ALPHA_B = .1
    __ALPHA_G = .8
    __K_B = 20
    __K_GO = 100
    __R = 8.314

    def __init__(self, pressure=1.2, signal=.001, water=-1):
        self.__pressure = pressure
        self.__signal = signal
        self.__water = water

    def get_guard_pressure(self):
        return self.__pressure

    def set_guard_pressure(self, pressure):
        self.__pressure = pressure

    def get_guard_signal(self):
        return self.__signal

    def set_guard_signal(self, signal):
        self.__signal = signal

    def get_guard_water_potential(self):
        return self.__water

    def set_guard_water_potential(self, water):
        self.__water = water

    # Equation 4
    def calculate_guard_signal(self, blue_intensity, total_intensity, carbon_dioxide):
        return Guard.__GAMMA_GO * (1 + Guard.__ALPHA_B * (blue_intensity / (blue_intensity + Guard.__K_B)) +
                                   Guard.__ALPHA_G * (total_intensity / (total_intensity + Guard.__K_GO *
                                                                         carbon_dioxide))) * 10 ** -6

    # Equation 6
    def calculate_guard_water_potential(self, temperature):
        return self.__pressure - (self.__signal * Guard.__R * temperature)
