###
# Interface (some components)
# REF: https://github.com/computervisioneng/face-attendance-system
###

import tkinter as tk
from tkinter import messagebox

def get_img_label(window):
    label = tk.Label(window, background = 'black')
    label.grid(row = 0, column = 0)
    return label

def msg_box(title, description):
    messagebox.showinfo(title, description)