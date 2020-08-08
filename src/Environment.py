class Environment:
    def __init__(self, amb_temp=296, amb_humid=10, amb_carbon=400, total=700, percent=5):
        self.temp = amb_temp
        self.humid = amb_humid
        self.carbon = amb_carbon
        self.total_intensity = total
        self.blue = (percent / 100) * total

    def get_ambient_temperature(self):
        return self.temp

    def set_ambient_temperature(self, temp):
        self.temp = temp

    def get_ambient_water(self):
        return self.humid

    def set_ambient_water(self, humid):
        self.humid = humid

    def get_ambient_carbon(self):
        return self.carbon

    def set_ambient_carbon(self, carbon):
        self.carbon = carbon

    def get_total_intensity(self):
        return self.total_intensity

    def set_total_intensity(self, total):
        self.total_intensity = total

    def get_blue_intensity(self):
        return self.blue

    def set_blue_intensity(self, blue):
        self.blue = (blue / 100) * self.total_intensity




