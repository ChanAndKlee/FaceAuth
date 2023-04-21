import tkinter as tk
from tkinter import messagebox

def get_button(window, text, color, command, fg = "white"):
    button = tk.Button(window,
                       text = text,
                       activebackground = "black",
                       activeforeground = "white",
                       fg = fg,
                       bg = color,
                       command = command,
                       height = 2,
                       width = 20,
                       font = "Poppins",
                       borderwidth = 20)
    return button

def get_img_label(window):
    label = tk.Label(window, background = 'black')
    label.grid(row = 0, column = 0)
    return label

def msg_box(title, description):
    messagebox.showinfo(title, description)