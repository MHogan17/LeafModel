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
