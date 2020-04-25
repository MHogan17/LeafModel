from Array import Array
from Environment import Environment

from tkinter import Tk, PhotoImage, Canvas, mainloop


def GradientPainter(gradient):
    win = Tk()
    win_size = len(gradient)
    photo = PhotoImage(width=win_size, height=win_size)
    canvas = Canvas(win, width=win_size, height=win_size, bg='#ffffff')
    canvas.create_image((win_size / 2, win_size / 2), image=photo, state="normal")

    for i in range(win_size):
        for j in range(win_size):
            color = gradient.get_color(i)
            photo.put(color, (i, j))
            canvas.pack()
            win.update()  # display a row of pixels


def ExperimentFactory(name):
    if name == 'light':
        print('Valid experiment')
        return Light()
    elif name == 'humidity':
        print('Also a valid experiment')
        return Humidity()


class Experiment:
    def __init__(self, time=5):
        self.array = Array()
        self.environment = Environment()
        self.time = time

    def run(self):
        raise(RuntimeError("'run' is not defined for this experiment type"))


class Light(Experiment):
    def run(self):
        print("This is a light experiment.")
        self.environment.set_total_intensity(0)
        array = Array()
        array.calculate_next(0, self.time, self.environment, array)


class Humidity(Experiment):
    def run(self):
        print("This is a humidity experiment.")
