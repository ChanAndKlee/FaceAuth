import tkinter as tk
import util
from PIL import Image, ImageTk


logged_in_window = tk.Tk()
logged_in_window.geometry("600x600+600+200")
logged_in_window.config(bg='black')


# Background
background = tk.PhotoImage(file='Resources/background.png')
label1 = tk.Label(logged_in_window, image = background)
label1.place(x=0, y=0)

# User Image
canvas = tk.Canvas(logged_in_window, bg='black', width= 300, height= 300, highlightthickness=0)
canvas.place(relx=0.5, rely=0.5, anchor='center')
user_img = ImageTk.PhotoImage(Image.open("Images/6388030.jpg"))
canvas.create_image(150, 150, image = user_img)

label2 = tk.Label(logged_in_window, text = f"Hello, Kulawut Makkamoltham")
label2.config(font =("Poppins", 16))
label2.place(x = 300, y = 500, anchor = 'center')


logged_in_window.mainloop()