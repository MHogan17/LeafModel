class Epidermal:
    __GAMMA_EO = 100
    __ALPHA_E = 0
    __K_EO = 1
    __R = 8.314

    def __init__(self, pressure=.2, signal=0.001, water=-.04):
        self.__pressure = pressure
        self.__signal = signal
        self.__water = water

    def get_epid_pressure(self):
        return self.__pressure

    def set_epid_pressure(self, pressure):
        self.__pressure = pressure

    def get_epid_signal(self):
        return self.__signal

    def set_epid_signal(self, signal):
        self.__signal = signal

    def get_epid_water_potential(self):
        return self.__water

    def set_epid_water_potential(self, water):
        self.__water = water

    # Equation 5
    def calculate_epid_signal(self, total_intensity, carbon_dioxide):
        return Epidermal.__GAMMA_EO * (1 + Epidermal.__ALPHA_E * (total_intensity / (total_intensity + Epidermal.__K_EO
                                                                                     * carbon_dioxide))) * 10 ** -6

    # Equation 7
    def calculate_epid_water_potential(self, temperature):
        return self.__pressure - self.__signal * Epidermal.__R * temperature
