# widgets.py
import tkinter as tk

def create_button(parent, text, command=None):
    button = tk.Button(parent, text=text, command=command, bg="blue", fg="white")
    button.pack(padx=10, pady=5)
    return button
