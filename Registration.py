from tkinter import *
from tkinter import messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageFilter
from sqlite3 import *


def Insertion(Var_adr, Var_nom, Var_mail, Var_num, Var_pass):
    # Se connecter à la base de données
  
    try:
        conn = connect('users.db')
        c = conn.cursor()

        Name = Var_nom.get()
        Mail = Var_mail.get()
        Number = int(Var_num.get())
        passw = Var_pass.get()
        Adress =  Var_adr.get()

        if(Name != "" and Mail != "" and Number != "" and passw != "" and Adress != ""):
            c.execute("INSERT INTO Client(Nom, Email, Mot_de_pass, Adresse, Numero) VALUES (?, ?, ?, ?, ?)", (Name, Mail, passw, Adress, Number))
            conn.commit()  # Valider l'insertion dans la base de données

            messagebox.showinfo(title="Message", message="Compte inscrit")
            
        else:
            messagebox.showerror(title="Erreur", message="Erreur lors de l'inscription")

        # Fermer la connexion à la base de données
        conn.close()

    except ValueError:
        messagebox.showerror(title="Erreur", message="Veuillez saisir un numero de téléphone valide")
 
