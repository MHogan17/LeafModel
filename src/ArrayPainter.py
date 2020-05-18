from tkinter import Tk, PhotoImage, Canvas


def paint_array(array, time):
    window = Tk()
    photo = PhotoImage(width=len(array), height=len(array))
    canvas = Canvas(window, width=len(array), height=len(array), bg='#ffffff')
    canvas.create_image((len(array)/2, len(array)/2), image=photo, state='normal')
    canvas.pack()

    for i in range(len(array)):
        for j in range(len(array[i])):
            color = array.find_color(i, j)
            photo.put(color, (i, j))
            window.update()

    photo.write('data/Minute ' + time + '.png', 'png')
    print(time, flush=True)
    window.destroy()
    return

