from tkinter import *
from tkinter import messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageFilter
from sqlite3 import *
from main import creation_fenetre_connexion
 

def on_entry_click(event, entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, END)
        entry.config(fg='black')

def on_entry_leave(event, entry, default_text):
    if entry.get() == "":
        entry.insert(0, default_text)
        entry.config(fg='grey')
    

def on_password_entry_click(event, entry):
    # Efface le texte "password" lorsqu'on clique dans le champ
    if entry.get() == "password":
        entry.delete(0, END)
        entry.config(show='*', fg='black')

def on_password_entry_leave(event, entry):

    # Rétablit le texte "password" si le champ est vide
    if entry.get() == "":
        entry.config(show='', fg='grey')
        entry.insert(0, "password")


def animate_button(button):
    button.config(relief=SUNKEN)
    button.after(100, lambda: button.config(relief=RAISED))
