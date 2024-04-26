from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from sqlite3 import *
from tkinter import font as tkfont
from datetime import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

T = 0

def Se_connecter(Fenetre_connexion, Email_entry, password_entry):
  
    global window_connexion 
    window_connexion = Fenetre_connexion
    global Email

 # Se connecter à la base de données
    conn = connect('users.db')
    c = conn.cursor()
    
    #Récupérer les valeurs des champs de saisie
    Email = Email_entry.get()
    password = password_entry.get()
    
    
    # Exécuter la requête pour vérifier les identifiants
    c.execute("SELECT * FROM Client WHERE Email=? AND Mot_de_pass=?", (Email, password))
    result = c.fetchone()
    
    # Fermer la connexion à la base de données
    conn.close()
    
    # Vérifier le résultat de la requête
    if result:
        Deploiement_Fenetre_Acceuil()
        
       
    else:
        messagebox.showerror(title="Erreur", message="Identifiants invalides.")

def Deploiement_Fenetre_Acceuil():

    global Panier
    Panier = []
    
    window_connexion.destroy()

    global Fenetre_Acceuil
    global frame_side_right
    global frame_side_left
    global frame_center
    Fenetre_Acceuil = Tk()
    Fenetre_Acceuil.title("SpeedyCart")
    Fenetre_Acceuil.resizable(False, False)
    frame_center = Frame(Fenetre_Acceuil, width = 1310, height = 850, bg="#f3f3f3", borderwidth=0)
    frame_center.place(x = 210, y = 0)
    global frame_side_right
    global frame_side_right_bottom
    frame_side_right_bottom = Frame(Fenetre_Acceuil, width=435, height=455, bg="#f3f3f3", highlightthickness=7)
    frame_side_right = Frame(Fenetre_Acceuil, width = 0, height = 850, bg="#f3f3f3", borderwidth=0, highlightthickness=5)
    frame_side_right.place(x = 1625, y = 0)
    global Total
    Total = IntVar()
    Lister_categories(None)

     # Obtenir la taille de l'écran
    screen_x = Fenetre_Acceuil.winfo_screenwidth()
    screen_y = Fenetre_Acceuil.winfo_screenheight()

    Fenetre_Acceuil.geometry(f"{screen_x}x{screen_y}")

    #cadre coté gauche
    frame_side_left = Frame(Fenetre_Acceuil, width=210, height=850, bg='#d11180', borderwidth=0)
    frame_side_left.place(x = 0, y = 0)

   # Image chapeau
    try:
        background_image = Image.open("chapeau.png")
        background_image = background_image.resize((65, 65))
            
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = Label(frame_side_left, image=background_photo, bg="#d11180")
        background_label.place(x=5, y=25)
    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    Titre = Label(Fenetre_Acceuil, text="SpeedyCart", width=10, bg="#d11180", fg="#ffffff", font=("Arial", 16))
    Titre.place(x = 77, y = 50)

     # Image acceuil
    try:
        background_image1 = Image.open("acceuil.png")
        background_image1 = background_image1.resize((80, 65))
            
        background_photo1 = ImageTk.PhotoImage(background_image1)
        background_label1 = Label(frame_side_left, image=background_photo1, bg="#d11180")
        background_label1.place(x=50, y=155)
         # Lier l'événement de clic à l'image avec la fonction image_click
        background_label1.bind("<Button-1>", Lister_categories)
    
    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    Acceuil_Label = Label(Fenetre_Acceuil, text="Home", width=15, bg="#d11180", fg="#ffffff", font=("Arial", 16))
    Acceuil_Label.place(x = 0, y = 216)

         # Image profil
    try:
        background_image2 = Image.open("profil.png")
        background_image2 = background_image2.resize((80, 65))
            
        background_photo2 = ImageTk.PhotoImage(background_image2)
        background_label2 = Label(frame_side_left, image=background_photo2, bg="#d11180")
        background_label2.place(x=50, y=313)
         # Lier l'événement de clic à l'image avec la fonction image_click
        background_label2.bind("<Button-1>", Affiche_profil)
    
    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    Profil_Label = Label(Fenetre_Acceuil, text="Profil", width=15, bg="#d11180", fg="#ffffff", font=("Arial", 16))
    Profil_Label.place(x = 0, y = 381)

    global id_client
    
    conn = connect('users.db')
    c = conn.cursor()
        
    # Exécution de la requête SQL
    c.execute("SELECT ID_Client FROM Client WHERE Email = ?", (Email, ))

    # Récupération des résultats dans une variable
    id_client = c.fetchall()

        # Fermeture de la connexion
    c.close()

    Fenetre_Acceuil.mainloop()


def Affiche_profil(event):

    vider_frame(frame_center)
    vider_frame(frame_side_right)
    vider_frame(frame_side_right_bottom)
    frame_side_right_bottom.place_forget()
    frame_side_right.place_forget()

    global Adresse
    global Numero
    global password
    global mail

    Adresse = StringVar()
    Numero = StringVar()
    password = StringVar()
    mail = StringVar()


    Adresse_Entry = Entry(frame_center, font = ("Arial", 13), width=30, fg = "black", bg = "#d9d9d9", textvariable=Adresse, borderwidth=0)
    Numero_Entry = Entry(frame_center, font = ("Arial", 13), width=30, fg = "black", bg = "#d9d9d9", textvariable=Numero, borderwidth=0)
    password_Entry = Entry(frame_center, font = ("Arial", 13), width=30, fg = "black", bg = "#d9d9d9", textvariable=password, borderwidth=0)
    Email_Entry = Entry(frame_center, font = ("Arial", 13), width=30, fg = "black", bg = "#d9d9d9", textvariable=mail, borderwidth=0)
    
    Email_label = Label(frame_center, text="Email", width=15, bg="#f3f3f3", fg="#000000", font=("Arial", 16))
    Numero_label = Label(frame_center, text="Numero", width=15, bg="#f3f3f3", fg="#000000", font=("Arial", 16))
    password_label = Label(frame_center, text="Mot de passe", width=15, bg="#f3f3f3", fg="#000000", font=("Arial", 16))
    Adresse_label = Label(frame_center, text="Adresse", width=15, bg="#f3f3f3", fg="#000000", font=("Arial", 16))

    Email_label.place(x = -8, y = 135)
    Numero_label.place(x = 3, y = 225)
    password_label.place(x = 326, y = 225)
    Adresse_label.place(x = 303, y = 135) 

    Email_Entry.place(x = 60, y = 170, height = 35)
    Numero_Entry.place(x = 60, y = 260, height = 35)
    Adresse_Entry.place(x = 355, y = 170, height = 35)
    password_Entry.place(x = 355, y = 260, height = 35)

    profil_label = Label(frame_center, text="Profil", fg="#000000", bg="#f3f3f3", font=("Arial", 17))
    profil_label.place(x = 60, y = 25)
    
    # Création du Canvas
    canvas = Canvas(frame_center, width=1300, height=30, bg="#f3f3f3")
    canvas.create_line(60, 30, 1290, 30)
    canvas.place(x = 3, y = 55)

    conn = connect('users.db')
    c = conn.cursor()

    c.execute("SELECT Email, Mot_de_pass, Adresse, Numero FROM Client WHERE ID_Client=?", (id_client[0][0], ))
    result = c.fetchall()

    mail.set(result[0][0])
    password.set(result[0][1])
    Adresse.set(result[0][2])
    Numero.set(result[0][3])

    

    # Fermeture de la connexion
    c.close()

    button_font = tkfont.Font(family='Arial', size=11, weight='bold')

    update_button = Button(frame_center, text="Modifier", command = Update_information, height=2, width=13, font=button_font, bg='#d11180', fg='#FFFFFF', borderwidth=0)
    update_button.place(x=504, y=315)

def Update_information():

    try:
        mail2 = mail.get()
        Adresse2 = Adresse.get()
        Numero2 = int(Numero.get())
        password2 = password.get()

    except ValueError:
        messagebox.showerror(title="Erreur", message="Veuillez saisir un numéro valide")

    
    if(mail2 != "" and Adresse2 != "" and Numero2 != "" and password2 != ""):

        conn = connect('users.db')
        c = conn.cursor()

        c.execute("UPDATE Client SET Email = ?, Mot_de_pass = ?, Adresse = ?, Numero = ? WHERE ID_Client = ?", (mail2, password2, Adresse2, Numero2, id_client[0][0]))
        conn.commit()  # Valider l'insertion dans la base de données
        messagebox.showinfo(title="Info", message="Compte mis à jour")

    else:
        messagebox.showerror(title="Erreur", message="Un des champs ou tous les champs sont vides, Réessayer")



def Lister_categories(event):
   

    global background_photo2
    global background_photo3
    global background_photo4
    global background_photo5
    global background_photo6
    global background_photo7
    global background_photo8
    global Total_payer
    global T

    global background_photo_Peperonni_large
    global background_photo_Peperonni_medium
    global background_photo_Peperonni_small
    global background_photo_Italienne_large
    global background_photo_Italienne_medium
    global background_photo_Italienne_small
    global background_photo_Margherita_large
    global background_photo_Margherita_medium
    global background_photo_Margherita_small
    global background_photo_Mozarella_large
    global background_photo_Mozarella_medium
    global background_photo_Mozarella_small
    global background_photo_Capelini
    global background_photo_Bucatini
    global background_photo_Bolognese
    global background_photo_Papaye
    global background_photo_Mango
    global background_photo_vegan_burger
    global background_photo_chicken
    global background_photo_crunch_burger
    global background_photo_french_tacos
    global background_photo_mexicos_tacos
    global background_photo_crispy_tacos
    global background_photo_cesar
    global background_photo_grec
    global background_photo_nicoise


    global background_label_Peperonni_large
    global background_label_Peperonni_medium
    global background_label_Peperonni_small
    global background_label_Italienne_large
    global background_label_Italienne_medium
    global background_label_Italienne_small
    global background_label_Margherita_large
    global background_label_Margherita_medium
    global background_label_Margherita_small
    global background_label_Mozarella_large
    global background_label_Mozarella_medium
    global background_label_Mozarella_small
    global background_label_Capelini
    global background_label_Bucatini
    global background_label_Bolognese
    global background_label_Papaye
    global background_label_Mango
    global background_label_vegan_burger
    global background_label_chicken
    global background_label_crunch_burger
    global background_label_french_tacos
    global background_label_mexicos_tacos
    global background_label_crispy_tacos
    global background_label_cesar
    global background_label_grec
    global background_label_nicoise



    global Prix_Quan_peperonni_large
    global Prix_Quan_peperonni_medium
    global Prix_Quan_peperonni_small
    global Prix_Quan_Italienne_large
    global Prix_Quan_Italienne_medium
    global Prix_Quan_Italienne_small
    global Prix_Quan_Margherita_large
    global Prix_Quan_Margherita_medium
    global Prix_Quan_Margherita_small
    global Prix_Quan_Mozarella_large
    global Prix_Quan_Mozarella_medium
    global Prix_Quan_Mozarella_small
    global Prix_Quan_Capelini
    global Prix_Quan_Bucatini
    global Prix_Quan_Bolognese
    global Prix_Quan_Papaye
    global Prix_Quan_Mango
    global Prix_Quan_vegan_burger
    global Prix_Quan_chicken
    global Prix_Quan_crunch_burger
    global Prix_Quan_french_tacos
    global Prix_Quan_mexicos_tacos
    global Prix_Quan_crispy_tacos
    global Prix_Quan_cesar
    global Prix_Quan_grec
    global Prix_Quan_nicoise


    global Peperonni_label_large
    global Peperonni_label_medium
    global Peperonni_label_small
    global Italienne_label_large
    global Italienne_label_medium
    global Italienne_label_small
    global Margherita_label_large
    global Margherita_label_medium
    global Margherita_label_small
    global Mozarella_label_large
    global Mozarella_label_medium
    global Mozarella_label_small
    global Capelini_label
    global Bucatini_label
    global Bolognese_label
    global Papaye_label
    global Mango_label
    global vegan_burger_label
    global chicken_label
    global crunch_burger_label
    global french_tacos_label
    global mexicos_tacos_label
    global crispy_tacos_label
    global cesar_label
    global grec_label
    global nicoise_label

    Information = 0

    background_image10 = Image.open("moins.png")
    background_image10 = background_image10.resize((20, 20))                            
    background_photo_Peperonni_large = ImageTk.PhotoImage(background_image10)

    background_image11 = Image.open("moins.png")
    background_image11 = background_image11.resize((20, 20))                            
    background_photo_Peperonni_medium= ImageTk.PhotoImage(background_image11)

    background_image12 = Image.open("moins.png")
    background_image12 = background_image12.resize((20, 20))                            
    background_photo_Peperonni_small= ImageTk.PhotoImage(background_image12)

    background_image13 = Image.open("moins.png")
    background_image13 = background_image13.resize((20, 20))                            
    background_photo_Italienne_large= ImageTk.PhotoImage(background_image13)

    background_image14 = Image.open("moins.png")
    background_image14 = background_image14.resize((20, 20))                            
    background_photo_Italienne_medium= ImageTk.PhotoImage(background_image14)

    background_image15 = Image.open("moins.png")
    background_image15 = background_image15.resize((20, 20))                            
    background_photo_Italienne_small= ImageTk.PhotoImage(background_image15)

    background_image16 = Image.open("moins.png")
    background_image16 = background_image16.resize((20, 20))                            
    background_photo_Margherita_large= ImageTk.PhotoImage(background_image16)

    background_image17 = Image.open("moins.png")
    background_image17 = background_image17.resize((20, 20))                            
    background_photo_Margherita_medium = ImageTk.PhotoImage(background_image17)

    background_image18 = Image.open("moins.png")
    background_image18 = background_image18.resize((20, 20))                            
    background_photo_Margherita_small= ImageTk.PhotoImage(background_image18)

    background_image19 = Image.open("moins.png")
    background_image19 = background_image19.resize((20, 20))                            
    background_photo_Mozarella_large= ImageTk.PhotoImage(background_image19)

    background_image20 = Image.open("moins.png")
    background_image20 = background_image20.resize((20, 20))                            
    background_photo_Mozarella_medium= ImageTk.PhotoImage(background_image20)

    background_image21 = Image.open("moins.png")
    background_image21 = background_image21.resize((20, 20))                            
    background_photo_Mozarella_small= ImageTk.PhotoImage(background_image21)

    background_image22 = Image.open("moins.png")
    background_image22 = background_image22.resize((20, 20))                            
    background_photo_Papaye= ImageTk.PhotoImage(background_image22)

    background_image23 = Image.open("moins.png")
    background_image23 = background_image23.resize((20, 20))                            
    background_photo_Mango = ImageTk.PhotoImage(background_image23)

    background_image24 = Image.open("moins.png")
    background_image24 = background_image24.resize((20, 20))                            
    background_photo_Capelini = ImageTk.PhotoImage(background_image24)

    background_image25 = Image.open("moins.png")
    background_image25 = background_image25.resize((20, 20))                            
    background_photo_Bucatini = ImageTk.PhotoImage(background_image25)

    background_image26 = Image.open("moins.png")
    background_image26 = background_image26.resize((20, 20))                            
    background_photo_Bolognese = ImageTk.PhotoImage(background_image26)

    background_image27 = Image.open("moins.png")
    background_image27 = background_image27.resize((20, 20))                            
    background_photo_vegan_burger = ImageTk.PhotoImage(background_image27)

    background_image28 = Image.open("moins.png")
    background_image28 = background_image28.resize((20, 20))                            
    background_photo_chicken = ImageTk.PhotoImage(background_image28)

    background_image29 = Image.open("moins.png")
    background_image29 = background_image29.resize((20, 20))                            
    background_photo_crunch_burger = ImageTk.PhotoImage(background_image29)

    background_image30 = Image.open("moins.png")
    background_image30 = background_image30.resize((20, 20))                            
    background_photo_french_tacos = ImageTk.PhotoImage(background_image30)

    background_image31 = Image.open("moins.png")
    background_image31 = background_image31.resize((20, 20))                            
    background_photo_mexicos_tacos = ImageTk.PhotoImage(background_image31)

    background_image32 = Image.open("moins.png")
    background_image32 = background_image32.resize((20, 20))                            
    background_photo_crispy_tacos = ImageTk.PhotoImage(background_image32)

    background_image33 = Image.open("moins.png")
    background_image33 = background_image33.resize((20, 20))                            
    background_photo_cesar = ImageTk.PhotoImage(background_image33)

    background_image34 = Image.open("moins.png")
    background_image34 = background_image34.resize((20, 20))                            
    background_photo_grec = ImageTk.PhotoImage(background_image34)

    background_image35 = Image.open("moins.png")
    background_image35 = background_image35.resize((20, 20))                            
    background_photo_nicoise = ImageTk.PhotoImage(background_image35)

   


    Peperonni_label_large = Label(frame_side_right_bottom, text="Peperonni - Large - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_peperonni_large = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Peperonni_large = Label(frame_side_right_bottom, image=background_photo_Peperonni_large, borderwidth=0)

    Peperonni_label_medium = Label(frame_side_right_bottom, text="Peperonni - Medium - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_peperonni_medium = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Peperonni_medium = Label(frame_side_right_bottom, image=background_photo_Peperonni_medium, borderwidth=0)

    Peperonni_label_small = Label(frame_side_right_bottom, text="Peperonni - Small - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_peperonni_small = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Peperonni_small = Label(frame_side_right_bottom, image=background_photo_Peperonni_small, borderwidth=0)

    Italienne_label_large = Label(frame_side_right_bottom, text="Italienne - Large - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_Italienne_large = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Italienne_large = Label(frame_side_right_bottom, image=background_photo_Italienne_large, borderwidth=0)

    Italienne_label_medium = Label(frame_side_right_bottom, text="Italienne - Medium - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_Italienne_medium = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Italienne_medium = Label(frame_side_right_bottom, image=background_photo_Italienne_medium, borderwidth=0)

    Italienne_label_small = Label(frame_side_right_bottom, text="Italienne - Small - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_Italienne_small = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Italienne_small = Label(frame_side_right_bottom, image=background_photo_Italienne_small, borderwidth=0)

    Margherita_label_large = Label(frame_side_right_bottom, text="Margherita - Large - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_Margherita_large = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Margherita_large = Label(frame_side_right_bottom, image=background_photo_Margherita_large, borderwidth=0)

    Margherita_label_medium = Label(frame_side_right_bottom, text="Margherita - Medium - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_Margherita_medium = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Margherita_medium = Label(frame_side_right_bottom, image=background_photo_Margherita_medium, borderwidth=0)

    Margherita_label_small = Label(frame_side_right_bottom, text="Margherita - Small - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_Margherita_small = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Margherita_small = Label(frame_side_right_bottom, image=background_photo_Margherita_small, borderwidth=0)

    Mozarella_label_large = Label(frame_side_right_bottom, text="Mozarella - Large - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_Mozarella_large = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Mozarella_large = Label(frame_side_right_bottom, image=background_photo_Mozarella_large, borderwidth=0)

    Mozarella_label_medium = Label(frame_side_right_bottom, text="Mozarella - Medium - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_Mozarella_medium = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Mozarella_medium = Label(frame_side_right_bottom, image=background_photo_Mozarella_medium, borderwidth=0)

    Mozarella_label_small = Label(frame_side_right_bottom, text="Mozarella - Small - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_Mozarella_small = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Mozarella_small = Label(frame_side_right_bottom, image=background_photo_Mozarella_small, borderwidth=0)

    Papaye_label = Label(frame_side_right_bottom, text="Papaye - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_Papaye = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Papaye = Label(frame_side_right_bottom, image=background_photo_Papaye, borderwidth=0)

    Mango_label = Label(frame_side_right_bottom, text="Mango - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_Mango = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Mango = Label(frame_side_right_bottom, image=background_photo_Mango, borderwidth=0)

    Capelini_label = Label(frame_side_right_bottom, text="Capelini - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_Capelini = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Capelini = Label(frame_side_right_bottom, image=background_photo_Capelini, borderwidth=0)

    Bucatini_label = Label(frame_side_right_bottom, text="Bucatini - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_Bucatini = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Bucatini = Label(frame_side_right_bottom, image=background_photo_Bucatini, borderwidth=0)

    Bolognese_label = Label(frame_side_right_bottom, text="Bolognese - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_Bolognese = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_Bolognese = Label(frame_side_right_bottom, image=background_photo_Bolognese, borderwidth=0)

    vegan_burger_label = Label(frame_side_right_bottom, text="Vegan Burger - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_vegan_burger = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_vegan_burger = Label(frame_side_right_bottom, image=background_photo_vegan_burger, borderwidth=0)

    chicken_label = Label(frame_side_right_bottom, text="Chicken Burger - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_chicken = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_chicken = Label(frame_side_right_bottom, image=background_photo_chicken, borderwidth=0)

    crunch_burger_label = Label(frame_side_right_bottom, text="Crunch Burger - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_crunch_burger = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_crunch_burger = Label(frame_side_right_bottom, image=background_photo_crunch_burger, borderwidth=0)
    
    french_tacos_label = Label(frame_side_right_bottom, text="French Tacos - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_french_tacos = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_french_tacos = Label(frame_side_right_bottom, image=background_photo_french_tacos, borderwidth=0)
    
    mexicos_tacos_label = Label(frame_side_right_bottom, text="Mexicos Tacos - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_mexicos_tacos = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_mexicos_tacos = Label(frame_side_right_bottom, image=background_photo_mexicos_tacos, borderwidth=0)
    
    crispy_tacos_label = Label(frame_side_right_bottom, text="Crispy Tacos - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_crispy_tacos = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_crispy_tacos = Label(frame_side_right_bottom, image=background_photo_crispy_tacos, borderwidth=0)
    
    cesar_label = Label(frame_side_right_bottom, text="Salade Cesar - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_cesar = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_cesar = Label(frame_side_right_bottom, image=background_photo_cesar, borderwidth=0)

    grec_label = Label(frame_side_right_bottom, text="Salade Grecque - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_grec = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_grec = Label(frame_side_right_bottom, image=background_photo_grec, borderwidth=0)

    nicoise_label = Label(frame_side_right_bottom, text="Salade Niçoise - ", bg="#f3f3f3", font=("Arial", 13), fg="black")
    Prix_Quan_nicoise = Label(frame_side_right_bottom, text=Information, bg="#f3f3f3", font=("Arial", 13), fg="black")
    background_label_nicoise = Label(frame_side_right_bottom, image=background_photo_nicoise, borderwidth=0)

    vider_frame(frame_center)
    vider_frame(frame_side_right)

    frame_side_right.config(width = 0, bg="#f3f3f3")
    frame_side_right.place(x = 1620, y = 0)

    Menu_label = Label(frame_center, text="Menu", fg="#000000", bg="#f3f3f3", font=("Arial", 17))
    Menu_label.place(x = 22, y = 24)
    
    # Création du Canvas
    canvas = Canvas(frame_center, width=1300, height=30, bg="#f3f3f3")
    canvas.create_line(20, 30, 1290, 30)
    canvas.place(x = 3, y = 55)

      # Image Pizza
    try:
        background_image2 = Image.open("pizza_categorie.png")
        background_image2 = background_image2.resize((145, 120))
            
        background_photo2 = ImageTk.PhotoImage(background_image2)
        background_label2 = Label(frame_center, image=background_photo2, borderwidth=0)
        background_label2.place(x=65, y=107)
        #Lier l'événement de clic à l'image avec la fonction image_click
        background_label2.bind("<Button-1>", Categorie_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    Pizza_Label = Label(frame_center, text="Pizza", fg="#000000", bg="#f3f3f3", font=("Arial", 16))
    Pizza_Label.place(x = 108, y = 227)

       # Image Spaghetti
    try:
        background_image3 = Image.open("Categorie_Spaghetti.png")
        background_image3 = background_image3.resize((145, 120))
            
        background_photo3 = ImageTk.PhotoImage(background_image3)
        background_label3 = Label(frame_center, image=background_photo3, borderwidth=0)
        background_label3.place(x=270, y=107)
        #Lier l'événement de clic à l'image avec la fonction image_click
        background_label3.bind("<Button-1>", Categorie_spaghetti)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    Spaghetti_Label = Label(frame_center, text="Spaghetti", fg="#000000", bg="#f3f3f3", font=("Arial", 16))
    Spaghetti_Label.place(x = 295, y = 227)

      # Image Burger
    try:
        background_image4 = Image.open("Categorie_Burger.png")
        background_image4 = background_image4.resize((145, 120))
            
        background_photo4 = ImageTk.PhotoImage(background_image4)
        background_label4 = Label(frame_center, image=background_photo4, borderwidth=0)
        background_label4.place(x=475, y=107)
        #Lier l'événement de clic à l'image avec la fonction image_click
        background_label4.bind("<Button-1>", Categorie_burger)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    Hamburger_Label = Label(frame_center, text="Hamburger", fg="#000000", bg="#f3f3f3", font=("Arial", 16))
    Hamburger_Label.place(x = 495, y = 227)

    
      # Image poisson
    try:
        background_image6 = Image.open("categorie_salad.png")
        background_image6 = background_image6.resize((165, 130))
            
        background_photo6 = ImageTk.PhotoImage(background_image6)
        background_label6 = Label(frame_center, image=background_photo6, borderwidth=0)
        background_label6.place(x=680, y=107)
        #Lier l'événement de clic à l'image avec la fonction image_click
        background_label6.bind("<Button-1>", Categorie_salad)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    Salade_Label = Label(frame_center, text="Salade", fg="#000000", bg="#f3f3f3", font=("Arial", 16))
    Salade_Label.place(x = 725, y = 227)


    
   # Image tacos
    try:
        background_image8 = Image.open("Categorie_tacos.png")
        background_image8 = background_image8.resize((165, 130))
            
        background_photo8 = ImageTk.PhotoImage(background_image8)
        background_label8 = Label(frame_center, image=background_photo8, borderwidth=0)
        background_label8.place(x=888, y=100)
        #Lier l'événement de clic à l'image avec la fonction image_click
        background_label8.bind("<Button-1>", Categorie_tacos)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    Tacos_Label = Label(frame_center, text="Tacos", fg="#000000", bg="#f3f3f3", font=("Arial", 16))
    Tacos_Label.place(x = 921, y = 227)
    T = Total.get() + T
    Total.set(0)
    
    if(T > 0):

        Affiche_panier()   
        Total_payer = StringVar()   
        To = str(T)
        devise = "fd"
        Tot = To + "" + devise
        Total_payer.set(Tot)          
        Total_commande = Entry(frame_side_right_bottom, state = "readonly", font = ("Arial", 13, "bold"), width=10, fg = "black", bg = "#f0f0f0", textvariable=Total_payer, borderwidth=0)
        Total_commande.place(x = 300, y = 390)
        
# Fonction pour vider le contenu du Frame
def vider_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def Categorie_spaghetti(event):
    vider_frame(frame_center)
    vider_frame(frame_side_right)
    vider_frame(frame_side_right_bottom)
    frame_side_right_bottom.place_forget()

    global background_photo2
    global background_photo3
    global background_photo4
    global background_photo5
    global background_photo6
    global background_photo7
    global Total_entry 
  
    global Prix_entry 
    global Prix
   
    Prix =  IntVar()
    global capelini_radio
    global bucatini_radio
    global bolognese_radio
    global Papaye_radio
    global Mango_radio
    global plat_a_personnalise
    plat_a_personnalise = IntVar()
    plat_a_personnalise.set(0)
    global spin_w
    global Quantite
    global taille
    global Ajouter_panier

    Quantite = IntVar()
    Quantite.set(0)
    Quantite.trace("w", update_prix_spaghetti)
    taille = IntVar()
    taille.set(0)


    Ajouter_panier = Button(frame_side_right, text="Ajouter au panier", font=("Arial", 13, "bold"), bg="#d11180", width=15, height=2, fg="white", command=Ajout_au_panier)

    capelini_radio = Radiobutton(frame_side_right, text="Capelini", font=("Arial", 13), bg="#f3f3f3", value = 11, variable=plat_a_personnalise, command=personnaliser_plat_spaghetti)
    bucatini_radio = Radiobutton(frame_side_right, text="Bucatini", font=("Arial", 13), bg="#f3f3f3", value = 12, variable=plat_a_personnalise, command=personnaliser_plat_spaghetti)
    bolognese_radio = Radiobutton(frame_side_right, text="Bolognese", font=("Arial", 13), bg="#f3f3f3", value = 13, variable=plat_a_personnalise, command=personnaliser_plat_spaghetti)
    Papaye_radio = Radiobutton(frame_side_right, text="Papaye", font=("Arial", 13), bg="#f3f3f3", value = 14, variable=plat_a_personnalise, command=personnaliser_plat_spaghetti)
    Mango_radio = Radiobutton(frame_side_right, text="Mango", font=("Arial", 13), bg="#f3f3f3", value = 15, variable=plat_a_personnalise, command=personnaliser_plat_spaghetti)
   
    spin_w = Spinbox(frame_side_right, from_ = 0, to = 100, textvariable=Quantite)

    

    Total_Label = Label(frame_side_right, text="Total", fg="#000000", bg="#f3f3f3", font=("Arial", 16))
    Total_Label.place(x = 10, y = 265)
    Total_entry = Entry(frame_side_right, width = 10, font=("Arial", 12, "bold"), bg="#d9d9d9", fg="black", borderwidth=0, textvariable=Total, state='readonly')
    Total_entry.place(x = 10, y = 295, height=32) 

    Prix_entry = Entry(frame_side_right, width = 10, font=("Arial", 12, "bold"), bg="#d9d9d9", fg="black", borderwidth=0, textvariable=Prix, state='readonly')
    

    frame_side_right.config(width = 440, bg="#f3f3f3", height=350)
    frame_side_right.place(x = 1070, y = 100)
    
    Plat_label = Label(frame_center, text="Plats", fg="#000000", bg="#f3f3f3", font=("Arial", 17))
    Plat_label.place(x = 22, y = 24)
    
    # Création du Canvas
    canvas1 = Canvas(frame_center, width=1300, height=30, bg="#f3f3f3", highlightthickness=1)
    canvas1.create_line(20, 30, 1290, 30)
    canvas1.place(x = 3, y = 55)

    Boissons_label = Label(frame_center, text="Boissons", fg="#000000", bg="#f3f3f3", font=("Arial", 17))
    Boissons_label.place(x = 22, y = 415)

     # Création du Canvas
    canvas2 = Canvas(frame_center, width=1300, height=30, bg="#f3f3f3", highlightthickness=1)
    canvas2.create_line(20, 30, 1290, 30)
    canvas2.place(x = 3, y = 446)

 # Image spaghetti_capelini
    try:
        background_image2 = Image.open("spaghetti_capelini.png")
        background_image2 = background_image2.resize((125, 130))
            
        background_photo2 = ImageTk.PhotoImage(background_image2)
        background_label2 = Label(frame_center, image=background_photo2, borderwidth=0)
        background_label2.place(x=67, y=107)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    # Variable pour stocker l'option sélectionnée
    global choix_capelini
    choix_capelini = BooleanVar()
    choix_capelini.set(False)

    # Création du bouton checkbox
    checkbox_capelini = Checkbutton(frame_center, text="Capelini", variable=choix_capelini, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_spaghetti)
    checkbox_capelini.place(x = 65, y = 227)

  # Image spaghetti_bucatini
    try:
        background_image3 = Image.open("spaghetti_bucatini.png")
        background_image3 = background_image3.resize((153, 139))
            
        background_photo3 = ImageTk.PhotoImage(background_image3)
        background_label3 = Label(frame_center, image=background_photo3, borderwidth=0)
        background_label3.place(x=251, y=95)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_bucatini
    choix_bucatini = BooleanVar()
    choix_bucatini.set(False)

    # Création du bouton checkbox
    checkbox_bucatini = Checkbutton(frame_center, text="Bucatini", variable=choix_bucatini, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_spaghetti)
    checkbox_bucatini.place(x = 275, y = 227)


    # Image spaghetti_bolognese
    try:
        background_image4 = Image.open("spaghetti_bolognese.png")
        background_image4 = background_image4.resize((125, 130))
            
        background_photo4 = ImageTk.PhotoImage(background_image4)
        background_label4 = Label(frame_center, image=background_photo4, borderwidth=0)
        background_label4.place(x=473, y=102)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_bolognese
    choix_bolognese = BooleanVar()
    choix_bolognese.set(False)

    # Création du bouton checkbox
    checkbox_bolognese = Checkbutton(frame_center, text="Bolognese", variable=choix_bolognese, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_spaghetti)
    checkbox_bolognese.place(x = 475, y = 227)

 # Image boisson_papaye
    try:
        background_image6 = Image.open("papaye_boisson.png")
        background_image6 = background_image6.resize((170, 135))
            
        background_photo6 = ImageTk.PhotoImage(background_image6)
        background_label6 = Label(frame_center, image=background_photo6, borderwidth=0)
        background_label6.place(x=52, y=500)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_Papaye
    choix_Papaye = BooleanVar()
    choix_Papaye.set(False)
    
    # Création du bouton checkbox
    checkbox_Papaye = Checkbutton(frame_center, text="Papaye", variable=choix_Papaye, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_spaghetti)
    checkbox_Papaye.place(x = 71, y = 650)

 # Image boisson_mango
    try:
        background_image7 = Image.open("mango_boisson.png")
        background_image7 = background_image7.resize((170, 135))
            
        background_photo7 = ImageTk.PhotoImage(background_image7)
        background_label7 = Label(frame_center, image=background_photo7, borderwidth=0)
        background_label7.place(x=270, y=500)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_Mango
    choix_Mango = BooleanVar()
    choix_Mango.set(False)
    
    # Création du bouton checkbox
    checkbox_Mango = Checkbutton(frame_center, text="Mango", variable=choix_Mango, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_spaghetti)
    checkbox_Mango.place(x = 295, y = 650)

def Categorie_pizza(event):
    vider_frame(frame_center)
    vider_frame(frame_side_right)
    vider_frame(frame_side_right_bottom)
    frame_side_right_bottom.place_forget()

    global background_photo2
    global background_photo3
    global background_photo4
    global background_photo5
    global background_photo6
    global background_photo7
    global Total_entry 
  
    global Prix_entry 
    global Prix
   
    Prix =  IntVar()
    global Peperonni_radio
    global Italienne_radio
    global Margherita_radio
    global Mozarella_radio
    global Papaye_radio
    global Mango_radio
    global plat_a_personnalise
    plat_a_personnalise = IntVar()
    plat_a_personnalise.set(0)
    global spin_w
    global Quantite
    global Large_button, Medium_button, Small_button, taille
    global Ajouter_panier


    Quantite = IntVar()
    Quantite.set(0)
    Quantite.trace("w", update_prix_pizza)
    taille = IntVar()
    taille.set(0)

    Ajouter_panier = Button(frame_side_right, text="Ajouter au panier", font=("Arial", 13, "bold"), bg="#d11180", width=15, height=2, fg="white", command=Ajout_au_panier)

    Peperonni_radio = Radiobutton(frame_side_right, text="Peperonni", font=("Arial", 13), bg="#f3f3f3", value = 1, variable=plat_a_personnalise, command=personnaliser_plat_pizza)
    Italienne_radio = Radiobutton(frame_side_right, text="Italienne", font=("Arial", 13), bg="#f3f3f3", value = 2, variable=plat_a_personnalise, command=personnaliser_plat_pizza)
    Margherita_radio = Radiobutton(frame_side_right, text="Margherita", font=("Arial", 13), bg="#f3f3f3", value = 3, variable=plat_a_personnalise, command=personnaliser_plat_pizza)
    Mozarella_radio = Radiobutton(frame_side_right, text="Mozarella", font=("Arial", 13), bg="#f3f3f3", value = 4, variable=plat_a_personnalise, command=personnaliser_plat_pizza)
    Papaye_radio = Radiobutton(frame_side_right, text="Papaye", font=("Arial", 13), bg="#f3f3f3", value = 5, variable=plat_a_personnalise, command=personnaliser_plat_pizza)
    Mango_radio = Radiobutton(frame_side_right, text="Mango", font=("Arial", 13), bg="#f3f3f3", value = 6, variable=plat_a_personnalise, command=personnaliser_plat_pizza)

    spin_w = Spinbox(frame_side_right, from_ = 0, to = 100, textvariable=Quantite)

    Large_button = Radiobutton(frame_side_right, text="Large", font=("Helvetica", 10), bg="#f3f3f3", value = 1, variable=taille, command =  update_prix_pizza)
    Medium_button = Radiobutton(frame_side_right, text="Medium", font=("Helvetica", 10), bg="#f3f3f3", value = 2, variable=taille, command =  update_prix_pizza)
    Small_button = Radiobutton(frame_side_right, text="Small", font=("Helvetica", 10), bg="#f3f3f3", value = 3, variable=taille, command =  update_prix_pizza)
    
    

    Total_Label = Label(frame_side_right, text="Total", fg="#000000", bg="#f3f3f3", font=("Arial", 16))
    Total_Label.place(x = 10, y = 265)
    Total_entry = Entry(frame_side_right, width = 10, font=("Arial", 12, "bold"), bg="#d9d9d9", fg="black", borderwidth=0, textvariable=Total, state='readonly')
    Total_entry.place(x = 10, y = 295, height=32) 

    Prix_entry = Entry(frame_side_right, width = 10, font=("Arial", 12, "bold"), bg="#d9d9d9", fg="black", borderwidth=0, textvariable=Prix, state='readonly')
    

    frame_side_right.config(width = 440, bg="#f3f3f3", height=350)
    frame_side_right.place(x = 1070, y = 100)
    
    Plat_label = Label(frame_center, text="Plats", fg="#000000", bg="#f3f3f3", font=("Arial", 17))
    Plat_label.place(x = 22, y = 24)
    
    # Création du Canvas
    canvas1 = Canvas(frame_center, width=1300, height=30, bg="#f3f3f3", highlightthickness=1)
    canvas1.create_line(20, 30, 1290, 30)
    canvas1.place(x = 3, y = 55)

    Boissons_label = Label(frame_center, text="Boissons", fg="#000000", bg="#f3f3f3", font=("Arial", 17))
    Boissons_label.place(x = 22, y = 415)

     # Création du Canvas
    canvas2 = Canvas(frame_center, width=1300, height=30, bg="#f3f3f3", highlightthickness=1)
    canvas2.create_line(20, 30, 1290, 30)
    canvas2.place(x = 3, y = 446)

     # Image pizza_peperonni
    try:
        background_image2 = Image.open("pizza_peperonni.png")
        background_image2 = background_image2.resize((125, 130))
            
        background_photo2 = ImageTk.PhotoImage(background_image2)
        background_label2 = Label(frame_center, image=background_photo2, borderwidth=0)
        background_label2.place(x=67, y=107)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
  
    # Variable pour stocker l'option sélectionnée
    global choix_Peperonni
    choix_Peperonni = BooleanVar()
    choix_Peperonni.set(False)

    # Création du bouton checkbox
    checkbox_Peperonni = Checkbutton(frame_center, text="Peperonni", variable=choix_Peperonni, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_pizza)
    checkbox_Peperonni.place(x = 65, y = 227)
        

    # Image pizza_italienne
    try:
        background_image3 = Image.open("pizza_italienne.png")
        background_image3 = background_image3.resize((153, 139))
            
        background_photo3 = ImageTk.PhotoImage(background_image3)
        background_label3 = Label(frame_center, image=background_photo3, borderwidth=0)
        background_label3.place(x=251, y=95)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_Italienne
    choix_Italienne = BooleanVar()
    choix_Italienne.set(False)

    # Création du bouton checkbox
    checkbox_Italienne = Checkbutton(frame_center, text="Italienne", variable=choix_Italienne, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_pizza)
    checkbox_Italienne.place(x = 275, y = 227)


    # Image pizza_margherita
    try:
        background_image4 = Image.open("pizza_margherita.png")
        background_image4 = background_image4.resize((125, 130))
            
        background_photo4 = ImageTk.PhotoImage(background_image4)
        background_label4 = Label(frame_center, image=background_photo4, borderwidth=0)
        background_label4.place(x=473, y=102)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_Margherita
    choix_Margherita = BooleanVar()
    choix_Margherita.set(False)

    # Création du bouton checkbox
    checkbox_Margherita = Checkbutton(frame_center, text="Margherita", variable=choix_Margherita, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_pizza)
    checkbox_Margherita.place(x = 475, y = 227)

 # Image pizza_mozarella
    try:
        background_image5 = Image.open("pizza_mozarella.png")
        background_image5 = background_image5.resize((130, 128))
            
        background_photo5 = ImageTk.PhotoImage(background_image5)
        background_label5 = Label(frame_center, image=background_photo5, borderwidth=0)
        background_label5.place(x=675, y=102)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_Mozarella
    choix_Mozarella = BooleanVar()
    choix_Mozarella.set(False)
    
    # Création du bouton checkbox
    checkbox_Mozarella = Checkbutton(frame_center, text="Mozarella", variable=choix_Mozarella, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_pizza)
    checkbox_Mozarella.place(x = 680, y = 227)
  # Image boisson_papaye
    try:
        background_image6 = Image.open("papaye_boisson.png")
        background_image6 = background_image6.resize((170, 135))
            
        background_photo6 = ImageTk.PhotoImage(background_image6)
        background_label6 = Label(frame_center, image=background_photo6, borderwidth=0)
        background_label6.place(x=52, y=500)
       
    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_Papaye
    choix_Papaye = BooleanVar()
    choix_Papaye.set(False)
    
    # Création du bouton checkbox
    checkbox_Papaye = Checkbutton(frame_center, text="Papaye", variable=choix_Papaye, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_pizza)
    checkbox_Papaye.place(x = 71, y = 650)

 # Image boisson_mango
    try:
        background_image7 = Image.open("mango_boisson.png")
        background_image7 = background_image7.resize((170, 135))
            
        background_photo7 = ImageTk.PhotoImage(background_image7)
        background_label7 = Label(frame_center, image=background_photo7, borderwidth=0)
        background_label7.place(x=270, y=500)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_Mango
    choix_Mango = BooleanVar()
    choix_Mango.set(False)
    
    # Création du bouton checkbox
    checkbox_Mango = Checkbutton(frame_center, text="Mango", variable=choix_Mango, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_pizza)
    checkbox_Mango.place(x = 295, y = 650)


def Categorie_burger(event):

    vider_frame(frame_center)
    vider_frame(frame_side_right)
    vider_frame(frame_side_right_bottom)
    frame_side_right_bottom.place_forget()

    global background_photo2
    global background_photo3
    global background_photo4
    global background_photo5
    global background_photo6
    global background_photo7
    global Total_entry 
  
    global Prix_entry 
    global Prix
   
    Prix =  IntVar()
    global vegan_burger_radio
    global chicken_radio
    global crunch_burger_radio
    global Papaye_radio
    global Mango_radio
    global plat_a_personnalise
    plat_a_personnalise = IntVar()
    plat_a_personnalise.set(0)
    global spin_w
    global Quantite
    global taille
    global Ajouter_panier

    Quantite = IntVar()
    Quantite.set(0)
    Quantite.trace("w", update_prix_burger)
    taille = IntVar()
    taille.set(0)


    Ajouter_panier = Button(frame_side_right, text="Ajouter au panier", font=("Arial", 13, "bold"), bg="#d11180", width=15, height=2, fg="white", command=Ajout_au_panier)

    vegan_burger_radio = Radiobutton(frame_side_right, text="Vegan Burger", font=("Arial", 13), bg="#f3f3f3", value = 21, variable=plat_a_personnalise, command=personnaliser_plat_burger)
    chicken_radio = Radiobutton(frame_side_right, text="Chicken Burger", font=("Arial", 13), bg="#f3f3f3", value = 22, variable=plat_a_personnalise, command=personnaliser_plat_burger)
    crunch_burger_radio = Radiobutton(frame_side_right, text="Crunch Burger", font=("Arial", 13), bg="#f3f3f3", value = 23, variable=plat_a_personnalise, command=personnaliser_plat_burger)
    Papaye_radio = Radiobutton(frame_side_right, text="Papaye", font=("Arial", 13), bg="#f3f3f3", value = 24, variable=plat_a_personnalise, command=personnaliser_plat_burger)
    Mango_radio = Radiobutton(frame_side_right, text="Mango", font=("Arial", 13), bg="#f3f3f3", value = 25, variable=plat_a_personnalise, command=personnaliser_plat_burger)
   
    spin_w = Spinbox(frame_side_right, from_ = 0, to = 100, textvariable=Quantite)

    

    Total_Label = Label(frame_side_right, text="Total", fg="#000000", bg="#f3f3f3", font=("Arial", 16))
    Total_Label.place(x = 10, y = 265)
    Total_entry = Entry(frame_side_right, width = 10, font=("Arial", 12, "bold"), bg="#d9d9d9", fg="black", borderwidth=0, textvariable=Total, state='readonly')
    Total_entry.place(x = 10, y = 295, height=32) 

    Prix_entry = Entry(frame_side_right, width = 10, font=("Arial", 12, "bold"), bg="#d9d9d9", fg="black", borderwidth=0, textvariable=Prix, state='readonly')
    

    frame_side_right.config(width = 440, bg="#f3f3f3", height=350)
    frame_side_right.place(x = 1070, y = 100)
    
    Plat_label = Label(frame_center, text="Plats", fg="#000000", bg="#f3f3f3", font=("Arial", 17))
    Plat_label.place(x = 22, y = 24)
    
    # Création du Canvas
    canvas1 = Canvas(frame_center, width=1300, height=30, bg="#f3f3f3", highlightthickness=1)
    canvas1.create_line(20, 30, 1290, 30)
    canvas1.place(x = 3, y = 55)

    Boissons_label = Label(frame_center, text="Boissons", fg="#000000", bg="#f3f3f3", font=("Arial", 17))
    Boissons_label.place(x = 22, y = 415)

     # Création du Canvas
    canvas2 = Canvas(frame_center, width=1300, height=30, bg="#f3f3f3", highlightthickness=1)
    canvas2.create_line(20, 30, 1290, 30)
    canvas2.place(x = 3, y = 446)

 # Image spaghetti_capelini
    try:
        background_image2 = Image.open("vegan_burger.png")
        background_image2 = background_image2.resize((175, 185))
            
        background_photo2 = ImageTk.PhotoImage(background_image2)
        background_label2 = Label(frame_center, image=background_photo2, borderwidth=0)
        background_label2.place(x=62, y=87)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    # Variable pour stocker l'option sélectionnée
    global choix_vegan_burger
    choix_vegan_burger = BooleanVar()
    choix_vegan_burger.set(False)

    # Création du bouton checkbox
    checkbox_vegan_burger = Checkbutton(frame_center, text="Vegan Burger", variable=choix_vegan_burger, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_burger)
    checkbox_vegan_burger.place(x = 65, y = 227)

  # Image spaghetti_bucatini
    try:
        background_image3 = Image.open("chicken_burger.png")
        background_image3 = background_image3.resize((155, 132))
            
        background_photo3 = ImageTk.PhotoImage(background_image3)
        background_label3 = Label(frame_center, image=background_photo3, borderwidth=0)
        background_label3.place(x=290, y=105)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_chicken
    choix_chicken = BooleanVar()
    choix_chicken.set(False)

    # Création du bouton checkbox
    checkbox_chicken = Checkbutton(frame_center, text="Chicken Burger", variable=choix_chicken, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_burger)
    checkbox_chicken.place(x = 280, y = 227)


    # Image spaghetti_bolognese
    try:
        background_image4 = Image.open("crunch_burger.png")
        background_image4 = background_image4.resize((165, 175))
            
        background_photo4 = ImageTk.PhotoImage(background_image4)
        background_label4 = Label(frame_center, image=background_photo4, borderwidth=0)
        background_label4.place(x=510, y=86)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_crunch_burger
    choix_crunch_burger = BooleanVar()
    choix_crunch_burger.set(False)

    # Création du bouton checkbox
    checkbox_crunch_burger = Checkbutton(frame_center, text="Crunch Burger", variable=choix_crunch_burger, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_burger)
    checkbox_crunch_burger.place(x = 512, y = 227)

 # Image boisson_papaye
    try:
        background_image6 = Image.open("papaye_boisson.png")
        background_image6 = background_image6.resize((170, 135))
            
        background_photo6 = ImageTk.PhotoImage(background_image6)
        background_label6 = Label(frame_center, image=background_photo6, borderwidth=0)
        background_label6.place(x=52, y=500)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_Papaye
    choix_Papaye = BooleanVar()
    choix_Papaye.set(False)
    
    # Création du bouton checkbox
    checkbox_Papaye = Checkbutton(frame_center, text="Papaye", variable=choix_Papaye, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_burger)
    checkbox_Papaye.place(x = 71, y = 650)

 # Image boisson_mango
    try:
        background_image7 = Image.open("mango_boisson.png")
        background_image7 = background_image7.resize((170, 135))
            
        background_photo7 = ImageTk.PhotoImage(background_image7)
        background_label7 = Label(frame_center, image=background_photo7, borderwidth=0)
        background_label7.place(x=270, y=500)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_Mango
    choix_Mango = BooleanVar()
    choix_Mango.set(False)
    
    # Création du bouton checkbox
    checkbox_Mango = Checkbutton(frame_center, text="Mango", variable=choix_Mango, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_burger)
    checkbox_Mango.place(x = 295, y = 650)

def Categorie_salad(event):
    
    vider_frame(frame_center)
    vider_frame(frame_side_right)
    vider_frame(frame_side_right_bottom)
    frame_side_right_bottom.place_forget()

    global background_photo2
    global background_photo3
    global background_photo4
    global background_photo5
    global background_photo6
    global background_photo7
    global Total_entry 
  
    global Prix_entry 
    global Prix
   
    Prix =  IntVar()
    global grec_radio
    global nicoise_radio
    global cesar_radio
    global Papaye_radio
    global Mango_radio
    global plat_a_personnalise
    plat_a_personnalise = IntVar()
    plat_a_personnalise.set(0)
    global spin_w
    global Quantite
    global taille
    global Ajouter_panier

    Quantite = IntVar()
    Quantite.set(0)
    Quantite.trace("w", update_prix_salad)
    taille = IntVar()
    taille.set(0)


    Ajouter_panier = Button(frame_side_right, text="Ajouter au panier", font=("Arial", 13, "bold"), bg="#d11180", width=15, height=2, fg="white", command=Ajout_au_panier)

    cesar_radio = Radiobutton(frame_side_right, text="Salade Cesar", font=("Arial", 13), bg="#f3f3f3", value = 31, variable=plat_a_personnalise, command=personnaliser_plat_salad)
    grec_radio = Radiobutton(frame_side_right, text="Salade Grecque", font=("Arial", 13), bg="#f3f3f3", value = 32, variable=plat_a_personnalise, command=personnaliser_plat_salad)
    nicoise_radio = Radiobutton(frame_side_right, text="Salade Niçoise", font=("Arial", 13), bg="#f3f3f3", value = 33, variable=plat_a_personnalise, command=personnaliser_plat_salad)
    Papaye_radio = Radiobutton(frame_side_right, text="Papaye", font=("Arial", 13), bg="#f3f3f3", value = 34, variable=plat_a_personnalise, command=personnaliser_plat_salad)
    Mango_radio = Radiobutton(frame_side_right, text="Mango", font=("Arial", 13), bg="#f3f3f3", value = 35, variable=plat_a_personnalise, command=personnaliser_plat_salad)
   
    spin_w = Spinbox(frame_side_right, from_ = 0, to = 100, textvariable=Quantite)

    

    Total_Label = Label(frame_side_right, text="Total", fg="#000000", bg="#f3f3f3", font=("Arial", 16))
    Total_Label.place(x = 10, y = 265)
    Total_entry = Entry(frame_side_right, width = 10, font=("Arial", 12, "bold"), bg="#d9d9d9", fg="black", borderwidth=0, textvariable=Total, state='readonly')
    Total_entry.place(x = 10, y = 295, height=32) 

    Prix_entry = Entry(frame_side_right, width = 10, font=("Arial", 12, "bold"), bg="#d9d9d9", fg="black", borderwidth=0, textvariable=Prix, state='readonly')
    

    frame_side_right.config(width = 440, bg="#f3f3f3", height=350)
    frame_side_right.place(x = 1070, y = 100)
    
    Plat_label = Label(frame_center, text="Plats", fg="#000000", bg="#f3f3f3", font=("Arial", 17))
    Plat_label.place(x = 22, y = 24)
    
    # Création du Canvas
    canvas1 = Canvas(frame_center, width=1300, height=30, bg="#f3f3f3", highlightthickness=1)
    canvas1.create_line(20, 30, 1290, 30)
    canvas1.place(x = 3, y = 55)

    Boissons_label = Label(frame_center, text="Boissons", fg="#000000", bg="#f3f3f3", font=("Arial", 17))
    Boissons_label.place(x = 22, y = 415)

     # Création du Canvas
    canvas2 = Canvas(frame_center, width=1300, height=30, bg="#f3f3f3", highlightthickness=1)
    canvas2.create_line(20, 30, 1290, 30)
    canvas2.place(x = 3, y = 446)

 # Image spaghetti_capelini
    try:
        background_image2 = Image.open("salade_cesar.png")
        background_image2 = background_image2.resize((165, 118))
            
        background_photo2 = ImageTk.PhotoImage(background_image2)
        background_label2 = Label(frame_center, image=background_photo2, borderwidth=0)
        background_label2.place(x=58, y=115)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    # Variable pour stocker l'option sélectionnée
    global choix_cesar
    choix_cesar = BooleanVar()
    choix_cesar.set(False)

    # Création du bouton checkbox
    checkbox_cesar = Checkbutton(frame_center, text=" Salade Cesar", variable=choix_cesar, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_salade)
    checkbox_cesar.place(x = 52, y = 227)

  # Image spaghetti_bucatini
    try:
        background_image3 = Image.open("Salade_Grecque.png")
        background_image3 = background_image3.resize((155, 101))
            
        background_photo3 = ImageTk.PhotoImage(background_image3)
        background_label3 = Label(frame_center, image=background_photo3, borderwidth=0)
        background_label3.place(x=290, y=136)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_grec
    choix_grec = BooleanVar()
    choix_grec.set(False)

    # Création du bouton checkbox
    checkbox_grec = Checkbutton(frame_center, text="Salade Grecque", variable=choix_grec, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_salade)
    checkbox_grec.place(x = 280, y = 227)


    # Image spaghetti_bolognese
    try:
        background_image4 = Image.open("salade_nicoise.png")
        background_image4 = background_image4.resize((125, 130))
            
        background_photo4 = ImageTk.PhotoImage(background_image4)
        background_label4 = Label(frame_center, image=background_photo4, borderwidth=0)
        background_label4.place(x=528, y=109)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_nicoise
    choix_nicoise = BooleanVar()
    choix_nicoise.set(False)

    # Création du bouton checkbox
    checkbox_nicoise = Checkbutton(frame_center, text="Salade Niçoise", variable=choix_nicoise, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_salade)
    checkbox_nicoise.place(x = 510, y = 227)

 # Image boisson_papaye
    try:
        background_image6 = Image.open("papaye_boisson.png")
        background_image6 = background_image6.resize((170, 135))
            
        background_photo6 = ImageTk.PhotoImage(background_image6)
        background_label6 = Label(frame_center, image=background_photo6, borderwidth=0)
        background_label6.place(x=52, y=500)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_Papaye
    choix_Papaye = BooleanVar()
    choix_Papaye.set(False)
    
    # Création du bouton checkbox
    checkbox_Papaye = Checkbutton(frame_center, text="Papaye", variable=choix_Papaye, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_salade)
    checkbox_Papaye.place(x = 71, y = 650)

 # Image boisson_mango
    try:
        background_image7 = Image.open("mango_boisson.png")
        background_image7 = background_image7.resize((170, 135))
            
        background_photo7 = ImageTk.PhotoImage(background_image7)
        background_label7 = Label(frame_center, image=background_photo7, borderwidth=0)
        background_label7.place(x=270, y=500)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_Mango
    choix_Mango = BooleanVar()
    choix_Mango.set(False)
    
    # Création du bouton checkbox
    checkbox_Mango = Checkbutton(frame_center, text="Mango", variable=choix_Mango, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_salade)
    checkbox_Mango.place(x = 295, y = 650)
    

def Categorie_tacos(event):
    
    vider_frame(frame_center)
    vider_frame(frame_side_right)
    vider_frame(frame_side_right_bottom)
    frame_side_right_bottom.place_forget()

    global background_photo2
    global background_photo3
    global background_photo4
    global background_photo5
    global background_photo6
    global background_photo7
    global Total_entry 
  
    global Prix_entry 
    global Prix
   
    Prix =  IntVar()
    global french_tacos_radio
    global mexicos_tacos_radio
    global crispy_tacos_radio
    global Papaye_radio
    global Mango_radio
    global plat_a_personnalise
    plat_a_personnalise = IntVar()
    plat_a_personnalise.set(0)
    global spin_w
    global Quantite
    global taille
    global Ajouter_panier

    Quantite = IntVar()
    Quantite.set(0)
    Quantite.trace("w", update_prix_tacos)
    taille = IntVar()
    taille.set(0)


    Ajouter_panier = Button(frame_side_right, text="Ajouter au panier", font=("Arial", 13, "bold"), bg="#d11180", width=15, height=2, fg="white", command=Ajout_au_panier)

    french_tacos_radio = Radiobutton(frame_side_right, text="French Tacos", font=("Arial", 13), bg="#f3f3f3", value = 41, variable=plat_a_personnalise, command=personnaliser_plat_tacos)
    mexicos_tacos_radio = Radiobutton(frame_side_right, text="Mexicos Tacos", font=("Arial", 13), bg="#f3f3f3", value = 42, variable=plat_a_personnalise, command=personnaliser_plat_tacos)
    crispy_tacos_radio = Radiobutton(frame_side_right, text="Crispy Tacos", font=("Arial", 13), bg="#f3f3f3", value = 43, variable=plat_a_personnalise, command=personnaliser_plat_tacos)
    Papaye_radio = Radiobutton(frame_side_right, text="Papaye", font=("Arial", 13), bg="#f3f3f3", value = 44, variable=plat_a_personnalise, command=personnaliser_plat_tacos)
    Mango_radio = Radiobutton(frame_side_right, text="Mango", font=("Arial", 13), bg="#f3f3f3", value = 45, variable=plat_a_personnalise, command=personnaliser_plat_tacos)
   
    spin_w = Spinbox(frame_side_right, from_ = 0, to = 100, textvariable=Quantite)

    

    Total_Label = Label(frame_side_right, text="Total", fg="#000000", bg="#f3f3f3", font=("Arial", 16))
    Total_Label.place(x = 10, y = 265)
    Total_entry = Entry(frame_side_right, width = 10, font=("Arial", 12, "bold"), bg="#d9d9d9", fg="black", borderwidth=0, textvariable=Total, state='readonly')
    Total_entry.place(x = 10, y = 295, height=32) 

    Prix_entry = Entry(frame_side_right, width = 10, font=("Arial", 12, "bold"), bg="#d9d9d9", fg="black", borderwidth=0, textvariable=Prix, state='readonly')
    

    frame_side_right.config(width = 440, bg="#f3f3f3", height=350)
    frame_side_right.place(x = 1070, y = 100)
    
    Plat_label = Label(frame_center, text="Plats", fg="#000000", bg="#f3f3f3", font=("Arial", 17))
    Plat_label.place(x = 22, y = 24)
    
    # Création du Canvas
    canvas1 = Canvas(frame_center, width=1300, height=30, bg="#f3f3f3", highlightthickness=1)
    canvas1.create_line(20, 30, 1290, 30)
    canvas1.place(x = 3, y = 55)

    Boissons_label = Label(frame_center, text="Boissons", fg="#000000", bg="#f3f3f3", font=("Arial", 17))
    Boissons_label.place(x = 22, y = 415)

     # Création du Canvas
    canvas2 = Canvas(frame_center, width=1300, height=30, bg="#f3f3f3", highlightthickness=1)
    canvas2.create_line(20, 30, 1290, 30)
    canvas2.place(x = 3, y = 446)

 # Image spaghetti_capelini
    try:
        background_image2 = Image.open("french_tacos.png")
        background_image2 = background_image2.resize((125, 112))
            
        background_photo2 = ImageTk.PhotoImage(background_image2)
        background_label2 = Label(frame_center, image=background_photo2, borderwidth=0)
        background_label2.place(x=67, y=112)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    # Variable pour stocker l'option sélectionnée
    global choix_french_tacos
    choix_french_tacos = BooleanVar()
    choix_french_tacos.set(False)

    # Création du bouton checkbox
    checkbox_french_tacos = Checkbutton(frame_center, text="French Tacos", variable=choix_french_tacos, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_tacos)
    checkbox_french_tacos.place(x = 55, y = 227)

  # Image spaghetti_bucatini
    try:
        background_image3 = Image.open("mexicos_tacos.png")
        background_image3 = background_image3.resize((148, 95))
            
        background_photo3 = ImageTk.PhotoImage(background_image3)
        background_label3 = Label(frame_center, image=background_photo3, borderwidth=0)
        background_label3.place(x=270, y=130)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_mexicos_tacos
    choix_mexicos_tacos = BooleanVar()
    choix_mexicos_tacos.set(False)

    # Création du bouton checkbox
    checkbox_mexicos_tacos = Checkbutton(frame_center, text="Mexicos Tacos", variable=choix_mexicos_tacos, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_tacos)
    checkbox_mexicos_tacos.place(x = 267, y = 227)


    # Image spaghetti_bolognese
    try:
        background_image4 = Image.open("crispy_tacos.png")
        background_image4 = background_image4.resize((158, 130))
            
        background_photo4 = ImageTk.PhotoImage(background_image4)
        background_label4 = Label(frame_center, image=background_photo4, borderwidth=0)
        background_label4.place(x=474, y=97)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_crispy_tacos
    choix_crispy_tacos = BooleanVar()
    choix_crispy_tacos.set(False)

    # Création du bouton checkbox
    checkbox_crispy_tacos = Checkbutton(frame_center, text="Crispy Tacos", variable=choix_crispy_tacos, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_tacos)
    checkbox_crispy_tacos.place(x = 485, y = 227)

 # Image boisson_papaye
    try:
        background_image6 = Image.open("papaye_boisson.png")
        background_image6 = background_image6.resize((170, 135))
            
        background_photo6 = ImageTk.PhotoImage(background_image6)
        background_label6 = Label(frame_center, image=background_photo6, borderwidth=0)
        background_label6.place(x=52, y=500)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_Papaye
    choix_Papaye = BooleanVar()
    choix_Papaye.set(False)
    
    # Création du bouton checkbox
    checkbox_Papaye = Checkbutton(frame_center, text="Papaye", variable=choix_Papaye, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_tacos)
    checkbox_Papaye.place(x = 71, y = 650)

 # Image boisson_mango
    try:
        background_image7 = Image.open("mango_boisson.png")
        background_image7 = background_image7.resize((170, 135))
            
        background_photo7 = ImageTk.PhotoImage(background_image7)
        background_label7 = Label(frame_center, image=background_photo7, borderwidth=0)
        background_label7.place(x=270, y=500)
        #Lier l'événement de clic à l'image avec la fonction image_click
        #background_label2.bind("<Button-1>", Lister_types_pizza)

    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")
    
    # Variable pour stocker l'option sélectionnée
    global choix_Mango
    choix_Mango = BooleanVar()
    choix_Mango.set(False)
    
    # Création du bouton checkbox
    checkbox_Mango = Checkbutton(frame_center, text="Mango", variable=choix_Mango, bg="#f3f3f3", font=("Helvetica", 16), command=Lance_double_methode_tacos)
    checkbox_Mango.place(x = 295, y = 650)


def Afficher_Liste_Plat_pizza():
    PosY = 10
    # Création d'une liste de tuples (checkbox, texte) pour faciliter la gestion
    choix = [
        (choix_Peperonni, "Peperonni"),
        (choix_Italienne, "Italienne"),
        (choix_Margherita, "Margherita"),
        (choix_Mozarella, "Mozarella"),
        (choix_Papaye, "Papaye"),
        (choix_Mango, "Mango")
        ]
   

  # Parcours de chaque choix pour afficher le bouton s'il est sélectionné
    for choix_checkbox, texte in choix:
        if choix_checkbox.get():
            # Si la checkbox est cochée, afficher le bouton
            if texte == "Peperonni":
                Peperonni_radio.place(x=10, y=PosY)
            elif texte == "Italienne":
                Italienne_radio.place(x=10, y=PosY)
            elif texte == "Margherita":
                Margherita_radio.place(x=10, y=PosY)
            elif texte == "Mozarella":
                Mozarella_radio.place(x=10, y=PosY)
            elif texte == "Papaye":
                Papaye_radio.config(text = "Papaye - 250fd")
                Papaye_radio.place(x=10, y=PosY)
            elif texte == "Mango":
                Mango_radio.config(text = "Mango - 350fd")
                Mango_radio.place(x=10, y=PosY)
            PosY += 30  # Augmentation de la position Y pour le prochain bouton
        else:
            # Si la checkbox n'est pas cochée, cacher le bouton
            if texte == "Peperonni":
                Peperonni_radio.place_forget()
            elif texte == "Italienne":
                Italienne_radio.place_forget()
            elif texte == "Margherita":
                Margherita_radio.place_forget()
            elif texte == "Mozarella":
                Mozarella_radio.place_forget()
            elif texte == "Papaye":
                Papaye_radio.place_forget()
            elif texte == "Mango":
                Mango_radio.place_forget()
    
   
def update_prix_pizza(*args):
    Prix.set(0)
    if(Quantite.get()>=1):
        Prix.set(0)

        possibilite1 = [1, 2, 3, 4, 5, 6]
        prix_menu = [[3150, 1700, 900], [3300, 1850, 1150], [3000, 1500, 850], [3500, 1850, 1200], 250, 350]


        for i in possibilite1:
            if(plat_a_personnalise.get() == i):

                if(i == 1):
                    if(taille.get() == 1):
                        Prix.set(0)
                        Prix_plat = Quantite.get() * prix_menu[i-1][0]
                        Prix.set(Prix_plat)
                    elif(taille.get() == 2):
                        Prix.set(0)
                        Prix_plat = Quantite.get() * prix_menu[i-1][1]
                        Prix.set(Prix_plat)
                    else:
                        Prix.set(0)
                        Prix_plat = Quantite.get() * prix_menu[i-1][2]
                        Prix.set(Prix_plat)

                elif(i == 2):
                    if(taille.get() == 1):
                        Prix.set(0)
                        Prix_plat = Quantite.get() * prix_menu[i-1][0]
                        Prix.set(Prix_plat)
                    elif(taille.get() == 2):
                        Prix.set(0)
                        Prix_plat = Quantite.get() * prix_menu[i-1][1]
                        Prix.set(Prix_plat)
                    else:
                        Prix.set(0)
                        Prix_plat = Quantite.get() * prix_menu[i-1][2]
                        Prix.set(Prix_plat)

                elif(i == 3):
                    if(taille.get() == 1):
                        Prix.set(0)
                        Prix_plat = Quantite.get() * prix_menu[i-1][0]
                        Prix.set(Prix_plat)
                    elif(taille.get() == 2):
                        Prix.set(0)
                        Prix_plat = Quantite.get() * prix_menu[i-1][1]
                        Prix.set(Prix_plat)
                    else:
                        Prix.set(0)
                        Prix_plat = Quantite.get() * prix_menu[i-1][2]
                        Prix.set(Prix_plat)

                elif(i == 4):
                    if(taille.get() == 1):
                        Prix.set(0)
                        Prix_plat = Quantite.get() * prix_menu[i-1][0]
                        Prix.set(Prix_plat)
                    elif(taille.get() == 2):
                        Prix.set(0)
                        Prix_plat = Quantite.get() * prix_menu[i-1][1]
                        Prix.set(Prix_plat)
                    else:
                        Prix.set(0)
                        Prix_plat = Quantite.get() * prix_menu[i-1][2]
                        Prix.set(Prix_plat)

                if(i == 5):
                    Prix_plat = Quantite.get() * prix_menu[i-1]
                    Prix.set(Prix_plat)

                if(i == 6):
                    Prix_plat = Quantite.get() * prix_menu[i-1]
                    Prix.set(Prix_plat)
        Ajouter_panier.place(x = 270, y = 277)
    else:
        Ajouter_panier.place_forget()

def Ajout_au_panier():
    Panier.extend([plat_a_personnalise.get() ,taille.get(), Quantite.get(), Prix.get()])
    print(Panier)
    global T
    Total.set(Total.get() + Prix.get())
    Prix.set(0)
    Quantite.set(0)
   
    
    

def personnaliser_plat_pizza():
   
    l = 0
    k = 0
    possibilite1 = [1, 2, 3, 4, 5, 6]
    possibilite2 = [choix_Peperonni, choix_Italienne, choix_Margherita, choix_Mozarella, choix_Mango, choix_Papaye]
    
    for i in possibilite1:
        if(plat_a_personnalise.get() == i):
            spin_w.place(x = 290, y = 18)
            Quantite.set(0)
            Prix_entry.place(x = 330, y = 44, height=30)
            Prix.set(0)
            if(i==1):
                Large_button.config(text="Large - 3150fd")
                Medium_button.config(text="Medium - 1700fd")
                Small_button.config(text="Small - 900fd")
                Large_button.place(x = 155, y = 20)
                Medium_button.place(x = 155, y = 50)
                Small_button.place(x = 155, y = 80)
            elif(i==2):
                Large_button.config(text="Large - 3300fd")
                Medium_button.config(text="Medium - 1850fd")
                Small_button.config(text="Small - 1150fd")
                Large_button.place(x = 155, y = 20)
                Medium_button.place(x = 155, y = 50)
                Small_button.place(x = 155, y = 80)
            elif(i==3):
                Large_button.config(text="Large - 3000fd")
                Medium_button.config(text="Medium - 1500fd")
                Small_button.config(text="Small - 850fd")
                Large_button.place(x = 155, y = 20)
                Medium_button.place(x = 155, y = 50)
                Small_button.place(x = 155, y = 80)
            elif(i==4):
                Large_button.config(text="Large - 3500fd")
                Medium_button.config(text="Medium - 1850fd")
                Small_button.config(text="Small - 1200fd")
                Large_button.place(x = 155, y = 20)
                Medium_button.place(x = 155, y = 50)
                Small_button.place(x = 155, y = 80)
         
    for choix in possibilite2:
        if(not choix.get()):
            l = l + 1

    
    for i in possibilite1:
        if ((plat_a_personnalise.get()!=1) and (plat_a_personnalise.get()!=2) and (plat_a_personnalise.get()!=3) and (plat_a_personnalise.get()!=4)):
             k = 4
            
            

    if(l == 6):
         spin_w.place_forget()
         Prix_entry.place_forget()
         Large_button.place_forget()
         Medium_button.place_forget()
         Small_button.place_forget()
         plat_a_personnalise.set(0)
    if(k == 4):
         Large_button.place_forget()
         Medium_button.place_forget()
         Small_button.place_forget()

def Lance_double_methode_pizza():
    Afficher_Liste_Plat_pizza()
    personnaliser_plat_pizza()

def update_prix_spaghetti(*args):
    Prix.set(0)
    if(Quantite.get()>=1):
        Prix.set(0)

        possibilite1 = [11, 12, 13, 14, 15]
        prix_menu = [600, 850, 650, 250, 350]


        for i in possibilite1:
            if(plat_a_personnalise.get() == i):

                if(i == 11):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-11]
                    Prix.set(Prix_plat)
                   
                elif(i == 12):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-11]
                    Prix.set(Prix_plat)
               
                elif(i == 13):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-11]
                    Prix.set(Prix_plat)
                
                elif(i == 14):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-11]
                    Prix.set(Prix_plat)
             
                if(i == 15):
                    Prix_plat = Quantite.get() * prix_menu[i-11]
                    Prix.set(Prix_plat)

        Ajouter_panier.place(x = 270, y = 277)
    else:
        Ajouter_panier.place_forget()

def personnaliser_plat_spaghetti():

     l = 0
     
     possibilite1 = [11, 12, 13, 14, 15]
     possibilite2 = [choix_capelini, choix_bucatini, choix_bolognese, choix_Mango, choix_Papaye]
    
     for i in possibilite1:
        if(plat_a_personnalise.get() == i):
            spin_w.place(x = 290, y = 18)
            Quantite.set(0)
            Prix_entry.place(x = 330, y = 44, height=30)
            Prix.set(0)
            
         
     for choix in possibilite2:
        if(not choix.get()):
            l = l + 1

     if(l == 5):
         print("hhh") 
         spin_w.place_forget()
         Prix_entry.place_forget()
         plat_a_personnalise.set(0)

def  Afficher_Liste_Plat_spaghetti():

    PosY = 10
    # Création d'une liste de tuples (checkbox, texte) pour faciliter la gestion
    choix = [
        (choix_capelini, "Capelini"),
        (choix_bucatini, "Bucatini"),
        (choix_bolognese, "Bolognese"),
        (choix_Papaye, "Papaye"),
        (choix_Mango, "Mango")
        ]
   
  # Parcours de chaque choix pour afficher le bouton s'il est sélectionné
    for choix_checkbox, texte in choix:
        if choix_checkbox.get():
            # Si la checkbox est cochée, afficher le bouton
            if texte == "Capelini":
                capelini_radio.place(x=10, y=PosY)
                capelini_radio.config(text="Capelini - 600fd")
            elif texte == "Bucatini":
                bucatini_radio.place(x=10, y=PosY)
                bucatini_radio.config(text="Bucatini - 850fd")
            elif texte == "Bolognese":
                bolognese_radio.place(x=10, y=PosY)
                bolognese_radio.config(text="Bolognese - 650fd")
            elif texte == "Papaye":
                Papaye_radio.place(x=10, y=PosY)
                Papaye_radio.config(text="Papaye - 250fd")
            elif texte == "Mango":
                Mango_radio.place(x=10, y=PosY)
                Mango_radio.config(text="Mango - 350fd")
            PosY += 30  # Augmentation de la position Y pour le prochain bouton
        else:
            # Si la checkbox n'est pas cochée, cacher le bouton
            if texte == "Capelini":
                capelini_radio.place_forget()
            elif texte == "Bucatini":
                bucatini_radio.place_forget()
            elif texte == "Bolognese":
                bolognese_radio.place_forget()
            elif texte == "Papaye":
                Papaye_radio.place_forget()
            elif texte == "Mango":
                Mango_radio.place_forget()
    
   
def Afficher_Liste_Plat_burger():

    
    PosY = 10
    # Création d'une liste de tuples (checkbox, texte) pour faciliter la gestion
    choix = [
        (choix_vegan_burger, "Vegan Burger"),
        (choix_chicken, "Chicken Burger"),
        (choix_crunch_burger, "Crunch Burger"),
        (choix_Papaye, "Papaye"),
        (choix_Mango, "Mango")
        ]
   
  # Parcours de chaque choix pour afficher le bouton s'il est sélectionné
    for choix_checkbox, texte in choix:
        if choix_checkbox.get():
            # Si la checkbox est cochée, afficher le bouton
            if texte == "Vegan Burger":
                vegan_burger_radio.place(x=10, y=PosY)
                vegan_burger_radio.config(text="Vegan Burger - 550fd")
            elif texte == "Chicken Burger":
                chicken_radio.place(x=10, y=PosY)
                chicken_radio.config(text="Chicken Burger - 750fd")
            elif texte == "Crunch Burger":
                crunch_burger_radio.place(x=10, y=PosY)
                crunch_burger_radio.config(text="Crunch Burger - 950fd")
            elif texte == "Papaye":
                Papaye_radio.place(x=10, y=PosY)
                Papaye_radio.config(text="Papaye - 250fd")
            elif texte == "Mango":
                Mango_radio.place(x=10, y=PosY)
                Mango_radio.config(text="Mango - 350fd")
            PosY += 30  # Augmentation de la position Y pour le prochain bouton
        else:
            # Si la checkbox n'est pas cochée, cacher le bouton
            if texte == "Vegan Burger":
                vegan_burger_radio.place_forget()
            elif texte == "Chicken Burger":
                chicken_radio.place_forget()
            elif texte == "Crunch Burger":
                crunch_burger_radio.place_forget()
            elif texte == "Papaye":
                Papaye_radio.place_forget()
            elif texte == "Mango":
                Mango_radio.place_forget()


def Afficher_Liste_Plat_tacos():

    PosY = 10
    # Création d'une liste de tuples (checkbox, texte) pour faciliter la gestion
    choix = [
        (choix_french_tacos, "French Tacos"),
        (choix_mexicos_tacos, "Mexicos Tacos"),
        (choix_crispy_tacos, "Crispy Tacos"),
        (choix_Papaye, "Papaye"),
        (choix_Mango, "Mango")
        ]
   
  # Parcours de chaque choix pour afficher le bouton s'il est sélectionné
    for choix_checkbox, texte in choix:
        if choix_checkbox.get():
            # Si la checkbox est cochée, afficher le bouton
            if texte == "French Tacos":
                french_tacos_radio.place(x=10, y=PosY)
                french_tacos_radio.config(text="French Tacos - 850fd")
            elif texte == "Mexicos Tacos":
                mexicos_tacos_radio.place(x=10, y=PosY)
                mexicos_tacos_radio.config(text="Mexicos Tacos - 900fd")
            elif texte == "Crispy Tacos":
                crispy_tacos_radio.place(x=10, y=PosY)
                crispy_tacos_radio.config(text="Crispy Tacos - 1050fd")
            elif texte == "Papaye":
                Papaye_radio.place(x=10, y=PosY)
                Papaye_radio.config(text="Papaye - 250fd")
            elif texte == "Mango":
                Mango_radio.place(x=10, y=PosY)
                Mango_radio.config(text="Mango - 350fd")
            PosY += 30  # Augmentation de la position Y pour le prochain bouton
        else:
            # Si la checkbox n'est pas cochée, cacher le bouton
            if texte == "French Tacos":
                french_tacos_radio.place_forget()
            elif texte == "Mexicos Tacos":
                mexicos_tacos_radio.place_forget()
            elif texte == "Crispy Tacos":
                crispy_tacos_radio.place_forget()
            elif texte == "Papaye":
                Papaye_radio.place_forget()
            elif texte == "Mango":
                Mango_radio.place_forget()
    

def Afficher_Liste_Plat_salad():

    PosY = 10
    # Création d'une liste de tuples (checkbox, texte) pour faciliter la gestion
    choix = [
        (choix_cesar, "Salade Cesar"),
        (choix_grec, "Salade Grecque"),
        (choix_nicoise, "Salade Niçoise"),
        (choix_Papaye, "Papaye"),
        (choix_Mango, "Mango")
        ]
   
  # Parcours de chaque choix pour afficher le bouton s'il est sélectionné
    for choix_checkbox, texte in choix:
        if choix_checkbox.get():
            # Si la checkbox est cochée, afficher le bouton
            if texte == "Salade Cesar":
                cesar_radio.place(x=10, y=PosY)
                cesar_radio.config(text="Salade Cesar - 650fd")
            elif texte == "Salade Grecque":
                grec_radio.place(x=10, y=PosY)
                grec_radio.config(text="Salade Grecque - 800fd")
            elif texte == "Salade Niçoise":
                nicoise_radio.place(x=10, y=PosY)
                nicoise_radio.config(text="Salade Niçoise - 1100fd")
            elif texte == "Papaye":
                Papaye_radio.place(x=10, y=PosY)
                Papaye_radio.config(text="Papaye - 250fd")
            elif texte == "Mango":
                Mango_radio.place(x=10, y=PosY)
                Mango_radio.config(text="Mango - 350fd")
            PosY += 30  # Augmentation de la position Y pour le prochain bouton
        else:
            # Si la checkbox n'est pas cochée, cacher le bouton
            if texte == "Salade Cesar":
                cesar_radio.place_forget()
            elif texte == "Salade Grecque":
                grec_radio.place_forget()
            elif texte == "Salade Niçoise":
                nicoise_radio.place_forget()
            elif texte == "Papaye":
                Papaye_radio.place_forget()
            elif texte == "Mango":
                Mango_radio.place_forget()
    


def personnaliser_plat_burger():

    l = 0
     
    possibilite1 = [21, 22, 23, 24, 25]
    possibilite2 = [choix_vegan_burger, choix_chicken, choix_crunch_burger, choix_Mango, choix_Papaye]
    
    for i in possibilite1:
        if(plat_a_personnalise.get() == i):
            spin_w.place(x = 290, y = 18)
            Quantite.set(0)
            Prix_entry.place(x = 330, y = 44, height=30)
            Prix.set(0)
            
         
    for choix in possibilite2:
        if(not choix.get()):
            l = l + 1

    if(l == 5):
         
         spin_w.place_forget()
         Prix_entry.place_forget()
         plat_a_personnalise.set(0)

def personnaliser_plat_tacos():

    l = 0
     
    possibilite1 = [41, 42, 43, 44, 45]
    possibilite2 = [choix_french_tacos, choix_mexicos_tacos, choix_crispy_tacos, choix_Mango, choix_Papaye]
    
    for i in possibilite1:
        if(plat_a_personnalise.get() == i):
            spin_w.place(x = 290, y = 18)
            Quantite.set(0)
            Prix_entry.place(x = 330, y = 44, height=30)
            Prix.set(0)
            
         
    for choix in possibilite2:
        if(not choix.get()):
            l = l + 1

    if(l == 5):
         
         spin_w.place_forget()
         Prix_entry.place_forget()
         plat_a_personnalise.set(0)



def personnaliser_plat_salad():

    l = 0
     
    possibilite1 = [31, 32, 33, 34, 35]
    possibilite2 = [choix_cesar, choix_grec, choix_nicoise, choix_Mango, choix_Papaye]
    
    for i in possibilite1:
        if(plat_a_personnalise.get() == i):
            spin_w.place(x = 290, y = 18)
            Quantite.set(0)
            Prix_entry.place(x = 330, y = 44, height=30)
            Prix.set(0)
            
         
    for choix in possibilite2:
        if(not choix.get()):
            l = l + 1

    if(l == 5):
         
         spin_w.place_forget()
         Prix_entry.place_forget()
         plat_a_personnalise.set(0)

def update_prix_burger(*args):
    Prix.set(0)
    if(Quantite.get()>=1):
        Prix.set(0)

        possibilite1 = [21, 22, 23, 24, 25]
        prix_menu = [550, 750, 950, 250, 350]


        for i in possibilite1:
            if(plat_a_personnalise.get() == i):

                if(i == 21):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-21]
                    Prix.set(Prix_plat)
                   
                elif(i == 22):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-21]
                    Prix.set(Prix_plat)
               
                elif(i == 23):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-21]
                    Prix.set(Prix_plat)
                
                elif(i == 24):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-21]
                    Prix.set(Prix_plat)
             
                if(i == 25):
                    Prix_plat = Quantite.get() * prix_menu[i-21]
                    Prix.set(Prix_plat)

        Ajouter_panier.place(x = 270, y = 277)
    else:
        Ajouter_panier.place_forget()

def update_prix_tacos(*args):

    Prix.set(0)
    if(Quantite.get()>=1):
        Prix.set(0)

        possibilite1 = [41, 42, 43, 44, 45]
        prix_menu = [850, 900, 1050, 250, 350]


        for i in possibilite1:
            if(plat_a_personnalise.get() == i):

                if(i == 41):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-41]
                    Prix.set(Prix_plat)
                   
                elif(i == 42):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-41]
                    Prix.set(Prix_plat)
               
                elif(i == 43):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-41]
                    Prix.set(Prix_plat)
                
                elif(i == 44):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-41]
                    Prix.set(Prix_plat)
             
                if(i == 45):
                    Prix_plat = Quantite.get() * prix_menu[i-41]
                    Prix.set(Prix_plat)

        Ajouter_panier.place(x = 270, y = 277)
    else:
        Ajouter_panier.place_forget()


def update_prix_salad(*args):

    Prix.set(0)
    if(Quantite.get()>=1):
        Prix.set(0)

        possibilite1 = [31, 32, 33, 34, 35]
        prix_menu = [650, 800, 1100, 250, 350]


        for i in possibilite1:
            if(plat_a_personnalise.get() == i):

                if(i == 31):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-31]
                    Prix.set(Prix_plat)
                   
                elif(i == 32):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-31]
                    Prix.set(Prix_plat)
               
                elif(i == 33):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-31]
                    Prix.set(Prix_plat)
                
                elif(i == 34):
                    Prix.set(0)
                    Prix_plat = Quantite.get() * prix_menu[i-31]
                    Prix.set(Prix_plat)
             
                if(i == 35):
                    Prix_plat = Quantite.get() * prix_menu[i-31]
                    Prix.set(Prix_plat)

        Ajouter_panier.place(x = 270, y = 277)
    else:
        Ajouter_panier.place_forget()


   
def Lance_double_methode_spaghetti():
    Afficher_Liste_Plat_spaghetti()
    personnaliser_plat_spaghetti()

def Lance_double_methode_burger():
    Afficher_Liste_Plat_burger()
    personnaliser_plat_burger()

def Lance_double_methode_pizza():
    Afficher_Liste_Plat_pizza()
    personnaliser_plat_pizza()

def Lance_double_methode_tacos():
    Afficher_Liste_Plat_tacos()
    personnaliser_plat_tacos()

def Lance_double_methode_salade():
    Afficher_Liste_Plat_salad()
    personnaliser_plat_salad()


def Affiche_panier():
  


    i = 0
    j = 0
    k = 0
    lengh = len(Panier)
    PosY = 10
    ensemble_pizza = {1, 2, 3, 4, 5, 6}
    ensemble_spaghetti = {11, 12, 13, 14, 15}
    ensemble_burger = {21, 22, 23, 24, 25}
    ensemble_salade = {31, 32, 33, 34, 35}
    ensemble_tacos = {41, 42, 43, 44, 45}
    


    if(not Panier):
                print("vide")
    else:
                
                while(i < lengh): 
                    k = 0
                    
                    if(Panier[j + i * 3] in ensemble_pizza):

                        possibilite = [1, 2, 3, 4, 5, 6]
                      
                        frame_side_right_bottom.place(x = 1095, y = 380)
                        Button_Commander = Button(frame_side_right_bottom, text="Commander", font=("Arial", 13, "bold"), bg="#d11180", width=11, height=2, fg="white", command=Commander)
                        Button_Commander.place(x = 10, y = 365)
                        
                        if(Panier[j + i * 3] == possibilite[k]):
                            if(Panier[j + i * 3 + 1] == 1):
                                Peperonni_label_large.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_peperonni_large.config(text = Information)
                                Prix_Quan_peperonni_large.place(x = 160, y = PosY)
                
                                try:
                                    
                                    background_label_Peperonni_large.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Peperonni_large.bind("<Button-1>", Retire_peperonni_large)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30


                            elif(Panier[j + i * 3 + 1] == 2):
                                Peperonni_label_medium.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_peperonni_medium.config(text = Information)
                                Prix_Quan_peperonni_medium.place(x = 175, y = PosY)
                                try:
                                   
                                    background_label_Peperonni_medium.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Peperonni_medium.bind("<Button-1>", Retire_peperonni_medium)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                            else:
                                Peperonni_label_small.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_peperonni_small.config(text = Information)
                                Prix_Quan_peperonni_small.place(x = 160, y = PosY)
                                try:
                                    
                                    background_label_Peperonni_small.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Peperonni_small.bind("<Button-1>", Retire_peperonni_small)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                            if(Panier[j + i * 3 + 1] == 1):
                                Italienne_label_large.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Italienne_large.config(text = Information)
                                Prix_Quan_Italienne_large.place(x = 145, y = PosY)
                                try:
                                
                                
                                    background_label_Italienne_large.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Italienne_large.bind("<Button-1>", Retire_Italienne_large)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                            elif(Panier[j + i * 3 + 1] == 2):
                                Italienne_label_medium.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Italienne_medium.config(text = Information)
                                Prix_Quan_Italienne_medium.place(x = 160, y = PosY)
                                try:
                                  
                                
                                    background_label_Italienne_medium.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Italienne_medium.bind("<Button-1>", Retire_Italienne_medium)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                            else:
                                Italienne_label_small.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Italienne_small.config(text = Information)
                                Prix_Quan_Italienne_small.place(x = 145, y = PosY)
                                try:
                                    
                                    background_label_Italienne_small.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Italienne_small.bind("<Button-1>", Retire_Italienne_small)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                            if(Panier[j + i * 3 + 1] == 1):
                                Margherita_label_large.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Margherita_large.config(text = Information)
                                Prix_Quan_Margherita_large.place(x = 165, y = PosY)
                                try:
                                   
                                    background_label_Margherita_large.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Margherita_large.bind("<Button-1>", Retire_Margherita_large)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                            elif(Panier[j + i * 3 + 1] == 2):
                                Margherita_label_medium.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Margherita_medium.config(text = Information)
                                Prix_Quan_Margherita_medium.place(x = 175, y = PosY)
                                try:
                                  
                                    background_label_Margherita_medium.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Margherita_medium.bind("<Button-1>", Retire_Margherita_medium)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                            else:
                                Margherita_label_small.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Margherita_small.config(text = Information)
                                Prix_Quan_Margherita_small.place(x = 165, y = PosY)
                                try:
                                    
                                    background_label_Margherita_small.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Margherita_small.bind("<Button-1>", Retire_Margherita_small)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                            if(Panier[j + i * 3 + 1] == 1):
                                Mozarella_label_large.place(x = 10, y = PosY)
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Mozarella_large.config(text = Information)
                                Prix_Quan_Mozarella_large.place(x = 150, y = PosY)
                                try:
                                   
                                    background_label_Mozarella_large.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Mozarella_large.bind("<Button-1>", Retire_Mozarella_large)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                            elif(Panier[j + i * 3 + 1] == 2):
                                Mozarella_label_medium.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Mozarella_medium.config(text = Information)
                                Prix_Quan_Mozarella_medium.place(x = 165, y = PosY)
                                try:
                                   
                                    background_label_Mozarella_medium.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Mozarella_medium.bind("<Button-1>", Retire_Mozarella_medium)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                            else:
                                Mozarella_label_small.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Mozarella_small.config(text = Information)
                                Prix_Quan_Mozarella_small.place(x = 150, y = PosY)
                                try:
                                    
                                    background_label_Mozarella_small.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Mozarella_small.bind("<Button-1>", Retire_Mozarella_small)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                        
                                Papaye_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Papaye.config(text = Information)
                                Prix_Quan_Papaye.place(x = 80, y = PosY)
                                try:
                                  
                                    background_label_Papaye.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Papaye.bind("<Button-1>", Retire_Papaye)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                        
                                Mango_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Mango.config(text = Information)
                                Prix_Quan_Mango.place(x = 75, y = PosY)
                                try:
                                   
                                    background_label_Mango.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Mango.bind("<Button-1>", Retire_Mango)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30
                                                                                                            
                     

                    elif(Panier[j + i * 3] in ensemble_spaghetti):
                        possibilite = [11, 12, 13, 14, 15]
                        frame_side_right_bottom.place(x = 1095, y = 380)
                        Button_Commander = Button(frame_side_right_bottom, text="Commander", font=("Arial", 13, "bold"), bg="#d11180", width=11, height=2, fg="white", command=Commander)
                        Button_Commander.place(x = 10, y = 365)

                        if(Panier[j + i * 3] == possibilite[k]):
                                Capelini_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Capelini.config(text = Information)
                                Prix_Quan_Capelini.place(x = 84, y = PosY)
                                try:
                                                                    
                                    background_label_Capelini.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Capelini.bind("<Button-1>", Retire_Capelini)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                Bucatini_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Bucatini.config(text = Information)
                                Prix_Quan_Bucatini.place(x = 84, y = PosY)
                                try:
                        
                                    background_label_Bucatini.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Bucatini.bind("<Button-1>", Retire_Bucatini)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                Bolognese_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Bolognese.config(text = Information)
                                Prix_Quan_Bolognese.place(x = 102, y = PosY)
                                try:
                                
                                    background_label_Bolognese.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Bolognese.bind("<Button-1>", Retire_Bolognese)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                    
                                Papaye_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Papaye.config(text = Information)
                                Prix_Quan_Papaye.place(x = 80, y = PosY)
                                try:
                        
                                    background_label_Papaye.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Papaye.bind("<Button-1>", Retire_Papaye)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                    
                                Mango_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Mango.config(text = Information)
                                Prix_Quan_Mango.place(x = 75, y = PosY)
                                try:
                           
                                    background_label_Mango.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Mango.bind("<Button-1>", Retire_Mango)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30


                    elif(Panier[j + i * 3] in ensemble_burger):
                        possibilite = [21, 22, 23, 24, 25]
                        frame_side_right_bottom.place(x = 1095, y = 380)
                        Button_Commander = Button(frame_side_right_bottom, text="Commander", font=("Arial", 13, "bold"), bg="#d11180", width=11, height=2, fg="white", command=Commander)
                        Button_Commander.place(x = 10, y = 365)

                        if(Panier[j + i * 3] == possibilite[k]):
                                vegan_burger_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_vegan_burger.config(text = Information)
                                Prix_Quan_vegan_burger.place(x = 130, y = PosY)
                                try:
                                                                    
                                    background_label_vegan_burger.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_vegan_burger.bind("<Button-1>", Retire_vegan_burger)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                chicken_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_chicken.config(text = Information)
                                Prix_Quan_chicken.place(x = 140, y = PosY)
                                try:
                        
                                    background_label_chicken.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_chicken.bind("<Button-1>", Retire_chicken)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                crunch_burger_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_crunch_burger.config(text = Information)
                                Prix_Quan_crunch_burger.place(x = 137, y = PosY)
                                try:
                                
                                    background_label_crunch_burger.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_crunch_burger.bind("<Button-1>", Retire_crunch_burger)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                    
                                Papaye_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Papaye.config(text = Information)
                                Prix_Quan_Papaye.place(x = 80, y = PosY)
                                try:
                        
                                    background_label_Papaye.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Papaye.bind("<Button-1>", Retire_Papaye)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                    
                                Mango_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Mango.config(text = Information)
                                Prix_Quan_Mango.place(x = 75, y = PosY)
                                try:
                           
                                    background_label_Mango.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Mango.bind("<Button-1>", Retire_Mango)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30


                    elif(Panier[j + i * 3] in ensemble_salade):
                        possibilite = [31, 32, 33, 34, 35]
                        frame_side_right_bottom.place(x = 1095, y = 380)
                        Button_Commander = Button(frame_side_right_bottom, text="Commander", font=("Arial", 13, "bold"), bg="#d11180", width=11, height=2, fg="white", command=Commander)
                        Button_Commander.place(x = 10, y = 365)

                        if(Panier[j + i * 3] == possibilite[k]):
                                cesar_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_cesar.config(text = Information)
                                Prix_Quan_cesar.place(x = 130, y = PosY)
                                try:
                                                                    
                                    background_label_cesar.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_cesar.bind("<Button-1>", Retire_cesar)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                grec_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_grec.config(text = Information)
                                Prix_Quan_grec.place(x = 140, y = PosY)
                                try:
                        
                                    background_label_grec.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_grec.bind("<Button-1>", Retire_grec)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                nicoise_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_nicoise.config(text = Information)
                                Prix_Quan_nicoise.place(x = 140, y = PosY)
                                try:
                                
                                    background_label_nicoise.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_nicoise.bind("<Button-1>", Retire_nicoise)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                    
                                Papaye_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Papaye.config(text = Information)
                                Prix_Quan_Papaye.place(x = 80, y = PosY)
                                try:
                        
                                    background_label_Papaye.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Papaye.bind("<Button-1>", Retire_Papaye)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                    
                                Mango_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Mango.config(text = Information)
                                Prix_Quan_Mango.place(x = 75, y = PosY)
                                try:
                           
                                    background_label_Mango.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Mango.bind("<Button-1>", Retire_Mango)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30 

                    elif(Panier[j + i * 3] in ensemble_tacos):
                        possibilite = [41, 42, 43, 44, 45]
                        frame_side_right_bottom.place(x = 1095, y = 380)
                        Button_Commander = Button(frame_side_right_bottom, text="Commander", font=("Arial", 13, "bold"), bg="#d11180", width=11, height=2, fg="white", command=Commander)
                        Button_Commander.place(x = 10, y = 365)

                        if(Panier[j + i * 3] == possibilite[k]):
                                french_tacos_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_french_tacos.config(text = Information)
                                Prix_Quan_french_tacos.place(x = 130, y = PosY)
                                try:
                                                                    
                                    background_label_french_tacos.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_french_tacos.bind("<Button-1>", Retire_french_tacos)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                mexicos_tacos_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_mexicos_tacos.config(text = Information)
                                Prix_Quan_mexicos_tacos.place(x = 135, y = PosY)
                                try:
                        
                                    background_label_mexicos_tacos.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_mexicos_tacos.bind("<Button-1>", Retire_mexicos_tacos)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                crispy_tacos_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_crispy_tacos.config(text = Information)
                                Prix_Quan_crispy_tacos.place(x = 130, y = PosY)
                                try:
                                
                                    background_label_crispy_tacos.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_crispy_tacos.bind("<Button-1>", Retire_crispy_tacos)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                    
                                Papaye_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Papaye.config(text = Information)
                                Prix_Quan_Papaye.place(x = 80, y = PosY)
                                try:
                        
                                    background_label_Papaye.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Papaye.bind("<Button-1>", Retire_Papaye)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30

                        k = k + 1
                        if(Panier[j + i * 3] == possibilite[k]):
                                    
                                Mango_label.place(x = 10, y = PosY) 
                                Prix = str(Panier[j + i * 3 + 3])
                                Quan = str(Panier[j + i * 3 + 2])
                                Information = Quan + " - " + Prix
                                Prix_Quan_Mango.config(text = Information)
                                Prix_Quan_Mango.place(x = 75, y = PosY)
                                try:
                           
                                    background_label_Mango.place(x=265, y=PosY + 2)
                                    #Lier l'événement de clic à l'image avec la fonction image_click
                                    background_label_Mango.bind("<Button-1>", Retire_Mango)

                                except FileNotFoundError:
                                    print("Image non trouvée. Assurez-vous que le chemin est correct.")
                                PosY = PosY + 30                                                                    
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                    i = i + 1
                    j = j + 1
                    if(i + j * 3 == lengh):
                        break
                            


def Retire_peperonni_large(event):

    
    global T
    prix_menu = [[3150, 1700, 900], [3300, 1850, 1150], [3000, 1500, 850], [3500, 1850, 1200], 250, 350]
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 1):
            if(Panier[j] == 1):
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[0][0] * Panier[j + 1]
                    
                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Peperonni_large.place_forget()
                    Prix_Quan_peperonni_large.place_forget()
                    Peperonni_label_large.place_forget()    
                    Affiche_panier()
                else:
                    background_label_Peperonni_large.place_forget()
                    Prix_Quan_peperonni_large.place_forget()
                    Peperonni_label_large.place_forget()
                  
                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier) 
                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break    
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)      
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()
   

def Retire_peperonni_medium(event):
 
    global T
    prix_menu = [[3150, 1700, 900], [3300, 1850, 1150], [3000, 1500, 850], [3500, 1850, 1200], 250, 350]
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 1):
            if(Panier[j] == 2):
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[0][1] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Peperonni_medium.place_forget()
                    Prix_Quan_peperonni_medium.place_forget()
                    Peperonni_label_medium.place_forget()    
                    Affiche_panier()
                else:
                    background_label_Peperonni_medium.place_forget()
                    Prix_Quan_peperonni_medium.place_forget()
                    Peperonni_label_medium.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()    
    

def Retire_peperonni_small(event):

    global T
    prix_menu = [[3150, 1700, 900], [3300, 1850, 1150], [3000, 1500, 850], [3500, 1850, 1200], 250, 350]
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 1):
            if(Panier[j] == 3):
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[0][2] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Peperonni_small.place_forget()
                    Prix_Quan_peperonni_small.place_forget()
                    Peperonni_label_small.place_forget()
                    Affiche_panier()
                else:
                    background_label_Peperonni_small.place_forget()
                    Prix_Quan_peperonni_small.place_forget()
                    Peperonni_label_small.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
  
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()    
    

def Retire_Italienne_large(event):

    global T
    prix_menu = [[3150, 1700, 900], [3300, 1850, 1150], [3000, 1500, 850], [3500, 1850, 1200], 250, 350]
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 2):
            if(Panier[j] == 1):
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[1][0] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Italienne_large.place_forget()
                    Prix_Quan_Italienne_large.place_forget()
                    Italienne_label_large.place_forget()
                    Affiche_panier()
                else:
                    background_label_Italienne_large.place_forget()
                    Prix_Quan_Italienne_large.place_forget()
                    Italienne_label_large.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
  
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()    

def Retire_Italienne_medium(event):

    global T
    prix_menu = [[3150, 1700, 900], [3300, 1850, 1150], [3000, 1500, 850], [3500, 1850, 1200], 250, 350]
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 2):
            if(Panier[j] == 2):
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[1][1] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Italienne_medium.place_forget()
                    Prix_Quan_Italienne_medium.place_forget()
                    Italienne_label_medium.place_forget()
                    Affiche_panier()
                else:
                    background_label_Italienne_medium.place_forget()
                    Prix_Quan_Italienne_medium.place_forget()
                    Italienne_label_medium.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()    
      

def Retire_Italienne_small(event):

    global T
    prix_menu = [[3150, 1700, 900], [3300, 1850, 1150], [3000, 1500, 850], [3500, 1850, 1200], 250, 350]
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 2):
            if(Panier[j] == 3):
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[1][2] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Italienne_small.place_forget()
                    Prix_Quan_Italienne_small.place_forget()
                    Italienne_label_small.place_forget()
                    Affiche_panier()
                else:
                    background_label_Italienne_small.place_forget()
                    Prix_Quan_Italienne_small.place_forget()
                    Italienne_label_small.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
   
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()    

def Retire_Margherita_large(event):
      
    global T
    prix_menu = [[3150, 1700, 900], [3300, 1850, 1150], [3000, 1500, 850], [3500, 1850, 1200], 250, 350]
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 3):
            if(Panier[j] == 1):
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[2][0] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Margherita_large.place_forget()
                    Prix_Quan_Margherita_large.place_forget()
                    Margherita_label_large.place_forget()
                    Affiche_panier()
                else:
                    background_label_Margherita_large.place_forget()
                    Prix_Quan_Margherita_large.place_forget()
                    Margherita_label_large.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()    
        
def Retire_Margherita_medium(event):

    global T
    prix_menu = [[3150, 1700, 900], [3300, 1850, 1150], [3000, 1500, 850], [3500, 1850, 1200], 250, 350]
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 3):
            if(Panier[j] == 2):
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[2][1] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Margherita_medium.place_forget()
                    Prix_Quan_Margherita_medium.place_forget()
                    Margherita_label_medium.place_forget()
                    Affiche_panier()
                else:
                    background_label_Margherita_medium.place_forget()
                    Prix_Quan_Margherita_medium.place_forget()
                    Margherita_label_medium.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()    
    
def Retire_Margherita_small(event):

    global T
    prix_menu = [[3150, 1700, 900], [3300, 1850, 1150], [3000, 1500, 850], [3500, 1850, 1200], 250, 350]
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 3):
            if(Panier[j] == 3):
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[2][2] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Margherita_small.place_forget()
                    Prix_Quan_Margherita_small.place_forget()
                    Margherita_label_small.place_forget()
                    Affiche_panier()
                else:
                    background_label_Margherita_small.place_forget()
                    Prix_Quan_Margherita_small.place_forget()
                    Margherita_label_small.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()    
        
def Retire_Mozarella_large(event):

    global T
    prix_menu = [[3150, 1700, 900], [3300, 1850, 1150], [3000, 1500, 850], [3500, 1850, 1200], 250, 350]
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 4):
            if(Panier[j] == 1):
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[3][0] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Mozarella_large.place_forget()
                    Prix_Quan_Mozarella_large.place_forget()
                    Mozarella_label_large.place_forget()
                    Affiche_panier()
                else:
                    background_label_Mozarella_large.place_forget()
                    Prix_Quan_Mozarella_large.place_forget()
                    Mozarella_label_large.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()    
    
def Retire_Mozarella_medium(event):

    global T
    prix_menu = [[3150, 1700, 900], [3300, 1850, 1150], [3000, 1500, 850], [3500, 1850, 1200], 250, 350]
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 4):
            if(Panier[j] == 2):
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[3][1] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Mozarella_medium.place_forget()
                    Prix_Quan_Mozarella_medium.place_forget()
                    Mozarella_label_medium.place_forget()
                    Affiche_panier()
                else:
                    background_label_Mozarella_medium.place_forget()
                    Prix_Quan_Mozarella_medium.place_forget()
                    Mozarella_label_medium.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()    
        
def Retire_Mozarella_small(event):

    global T
    prix_menu = [[3150, 1700, 900], [3300, 1850, 1150], [3000, 1500, 850], [3500, 1850, 1200], 250, 350]
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 4):
            if(Panier[j] == 3):
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[3][2] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Mozarella_small.place_forget()
                    Prix_Quan_Mozarella_small.place_forget()
                    Mozarella_label_small.place_forget()
                    Affiche_panier()
                else:
                    background_label_Mozarella_small.place_forget()
                    Prix_Quan_Mozarella_small.place_forget()
                    Mozarella_label_small.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()    
    
def Retire_Papaye(event):
    global T
    prix_menu = [[3150, 1700, 900], [3300, 1850, 1150], [3000, 1500, 850], [3500, 1850, 1200], 250, 350]
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 5 or Panier[i] == 14 or Panier[i] == 24 or Panier[i] == 34 or Panier[i] == 44):
            
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[4] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Papaye.place_forget()
                    Prix_Quan_Papaye.place_forget()
                    Papaye_label.place_forget()
                    Affiche_panier()
                else:
                    background_label_Papaye.place_forget()
                    Prix_Quan_Papaye.place_forget()
                    Papaye_label.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()    
    
def Retire_Mango(event):

    global T
    prix_menu = [[3150, 1700, 900], [3300, 1850, 1150], [3000, 1500, 850], [3500, 1850, 1200], 250, 350]
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 6 or Panier[i] == 15 or Panier[i] == 25 or Panier[i] == 35 or Panier[i] == 45):
        
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[5] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Mango.place_forget()
                    Prix_Quan_Mango.place_forget()
                    Mango_label.place_forget()
                    Affiche_panier()
                else:
                    background_label_Mango.place_forget()
                    Prix_Quan_Mango.place_forget()
                    Mango_label.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()    

def Retire_Capelini(event):

    global T
    prix_menu = [600, 850, 650, 250, 350]
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 11):
        
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[0] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Capelini.place_forget()
                    Prix_Quan_Capelini.place_forget()
                    Capelini_label.place_forget()
                    Affiche_panier()
                else:
                    background_label_Capelini.place_forget()
                    Prix_Quan_Capelini.place_forget()
                    Capelini_label.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()    

def Retire_Bucatini(event):

    global T
    prix_menu = [600, 850, 650, 250, 350]    
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 12):
        
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[1] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Bucatini.place_forget()
                    Prix_Quan_Bucatini.place_forget()
                    Bucatini_label.place_forget()
                    Affiche_panier()
                else:
                    background_label_Bucatini.place_forget()
                    Prix_Quan_Bucatini.place_forget()
                    Bucatini_label.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()    

def Retire_Bolognese(event):

    global T
    prix_menu = [600, 850, 650, 250, 350] 
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 13):
        
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[2] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_Bolognese.place_forget()
                    Prix_Quan_Bolognese.place_forget()
                    Bolognese_label.place_forget()
                    Affiche_panier()
                else:
                    background_label_Bolognese.place_forget()
                    Prix_Quan_Bolognese.place_forget()
                    Bolognese_label.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()


def Retire_vegan_burger(event):

    global T
    prix_menu = [550, 750, 950, 250, 350] 
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 21):
        
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[0] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_vegan_burger.place_forget()
                    Prix_Quan_vegan_burger.place_forget()
                    vegan_burger_label.place_forget()
                    Affiche_panier()
                else:
                    background_label_vegan_burger.place_forget()
                    Prix_Quan_vegan_burger.place_forget()
                    vegan_burger_label.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()

def Retire_chicken(event):

    global T
    prix_menu = [550, 750, 950, 250, 350] 
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 22):
        
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[1] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_chicken.place_forget()
                    Prix_Quan_chicken.place_forget()
                    chicken_label.place_forget()
                    Affiche_panier()
                else:
                    background_label_chicken.place_forget()
                    Prix_Quan_chicken.place_forget()
                    chicken_label.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()

def Retire_crunch_burger(event):

    global T
    prix_menu = [550, 750, 950, 250, 350] 
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 23):
        
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[2] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_crunch_burger.place_forget()
                    Prix_Quan_crunch_burger.place_forget()
                    crunch_burger_label.place_forget()
                    Affiche_panier()
                else:
                    background_label_crunch_burger.place_forget()
                    Prix_Quan_crunch_burger.place_forget()
                    crunch_burger_label.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()


def Retire_cesar(event):

    global T
    prix_menu = [650, 800, 1100, 250, 350] 
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 31):
        
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[0] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_cesar.place_forget()
                    Prix_Quan_cesar.place_forget()
                    cesar_label.place_forget()
                    Affiche_panier()
                else:
                    background_label_cesar.place_forget()
                    Prix_Quan_cesar.place_forget()
                    cesar_label.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()


def Retire_grec(event):

    global T
    prix_menu = [650, 800, 1100, 250, 350] 
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 32):
        
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[1] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_grec.place_forget()
                    Prix_Quan_grec.place_forget()
                    grec_label.place_forget()
                    Affiche_panier()
                else:
                    background_label_grec.place_forget()
                    Prix_Quan_grec.place_forget()
                    grec_label.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()


def Retire_nicoise(event):

    global T
    prix_menu = [650, 800, 1100, 250, 350] 
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 33):
        
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[2] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_nicoise.place_forget()
                    Prix_Quan_nicoise.place_forget()
                    nicoise_label.place_forget()
                    Affiche_panier()
                else:
                    background_label_nicoise.place_forget()
                    Prix_Quan_nicoise.place_forget()
                    nicoise_label.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()




def Retire_french_tacos(event):

    global T
    prix_menu = [850, 900, 1050, 250, 350] 
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 41):
        
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[0] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_french_tacos.place_forget()
                    Prix_Quan_french_tacos.place_forget()
                    french_tacos_label.place_forget()
                    Affiche_panier()
                else:
                    background_label_french_tacos.place_forget()
                    Prix_Quan_french_tacos.place_forget()
                    french_tacos_label.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()



def Retire_mexicos_tacos(event):

    global T
    prix_menu = [850, 900, 1050, 250, 350] 
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 42):
        
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[1] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_mexicos_tacos.place_forget()
                    Prix_Quan_mexicos_tacos.place_forget()
                    mexicos_tacos_label.place_forget()
                    Affiche_panier()
                else:
                    background_label_mexicos_tacos.place_forget()
                    Prix_Quan_mexicos_tacos.place_forget()
                    mexicos_tacos_label.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()



def Retire_crispy_tacos(event):

    global T
    prix_menu = [850, 900, 1050, 250, 350] 
    lengh = len(Panier)
    i = 0
    
    while(i < lengh):
        j = i + 1
        if(Panier[i] == 43):
        
                if(Panier[j + 1] > 1):
                    Panier[j + 1] = Panier[j + 1] - 1
                    Panier[j + 2] = prix_menu[2] * Panier[j + 1]

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        To = str(T)
                        devise = "fd"
                        Tot = To + "" + devise
                        Total_payer.set(Tot)
                        k = k + 4
                        if(k == lengh):
                            break
                    background_label_crispy_tacos.place_forget()
                    Prix_Quan_crispy_tacos.place_forget()
                    crispy_tacos_label.place_forget()
                    Affiche_panier()
                else:
                    background_label_crispy_tacos.place_forget()
                    Prix_Quan_crispy_tacos.place_forget()
                    crispy_tacos_label.place_forget()

                    n = 0
                    while(n < 4):
                        del Panier[i]
                        n = n + 1
                    lengh = len(Panier)    

                    k = 0
                    T = 0
                    while(k < lengh):
                        p = Panier[k + 3]
                        T = T + p
                        k = k + 4
                        if(k == lengh):
                            break    
                    Affiche_panier()

        i = i + 4 
        if(i == lengh):
            break      
  
    To = str(T)
    devise = "fd"
    Tot = To + "" + devise
    Total_payer.set(Tot)
    if(T == 0):
        vider_frame(frame_side_right_bottom)
        frame_side_right_bottom.place_forget()



def Commander():
    messagebox.showinfo(title = "Info", message = "Commande prise en charge, livraison en cours...")
    vider_frame(frame_side_right_bottom)
    frame_side_right_bottom.place_forget()
    

    global Plats
    Plats = []
    global Plats_commandes
    Plats = [1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 21, 22, 23, 24, 25, 31, 32, 33, 34, 35, 41, 42, 43, 44, 45]
    i = 0
    k = 0
    lengh = len(Panier)
    choix = [
        (1, "Peperonni"),
        (2, "Italienne"),
        (3, "Margherita"),
        (4, "Mozarella"),
        (11, "Capelini"),
        (12, "Bucatini"),
        (13, "Bolognese"),
        (21, "Cheese Burger"),
        (22, "Chicken Burger"),
        (23, "Crunch Burger"),
        (31, "Salade Cesar"),
        (32, "Salade Grecque"),
        (33, "Salade Niçoise"),
        (41, "French Tacos"),
        (42, "Mexicos Tacos"),
        (43, "American Tacos"),
        (5, "Papaye"),
        (6, "Mango"),
        (14, "Papaye"),
        (15, "Mango"),
        (24, "Papaye"),
        (25, "Mango"),
        (34, "Papaye"),
        (35, "Mango"),
        (44, "Papaye"),
        (45, "Mango"),
            ]
    l = 0
    plats = ""
    global quantite
    global price

    while(k < lengh):
        if(i in Plats):#Si i correspond à un plat
            
            if(Panier[k] == i):#Si i est commandé
                l = l + 1 
                
                if(i in {1, 2, 3, 4}):#Si i est une pizza
                    
                    taille = Panier[k + 1]
                    quantite = Panier[k + 2]
                    price = Panier[k + 3]

                    for numero, plat in choix:
                        if(i == numero):
                            
                            if(taille == 1 and l == 1 and quantite == 1):
                                nom_plat = str(quantite) + " " + plat + " " + "Large" + " : " + str(price)  + "FDJ" + "\n"
                                Plats_commandes = nom_plat
                                plats = Plats_commandes
                                i = -1
                              
                            elif(taille == 1 and l != 1 and quantite == 1):
                                nom_plat = str(quantite) + " " + plat + " " + "Large" + " : " + str(price)  + "FDJ" + "\n"
                                Plats_commandes = plats + nom_plat
                                plats = Plats_commandes
                                i = -1

                            if(taille == 1 and l == 1 and quantite != 1):
                                nom_plat = str(quantite) + " " + plat + " " + "Large" + " : " + str(price)  + "FDJ" + "\n"
                                Plats_commandes = nom_plat
                                plats = Plats_commandes
                                i = -1
                              
                            elif(taille == 1 and l != 1 and quantite != 1):
                                nom_plat = str(quantite) + " " + plat + " " + "Large" + " : " + str(price)  + "FDJ" + "\n"
                                Plats_commandes = plats + nom_plat
                                plats = Plats_commandes
                                i = -1



                            if(taille == 2 and l == 1 and quantite == 1):
                                nom_plat = str(quantite) + " " + plat + " " + "Medium" + " : " + str(price)  + "FDJ" + "\n"
                                Plats_commandes = nom_plat
                                plats = Plats_commandes
                                print("ICI B")
                                i = -1
                              
                            elif(taille == 2 and l != 1 and quantite == 1):
                                nom_plat = str(quantite) + " " + plat + " " + "Medium" + " : " + str(price)  + "FDJ" + "\n"
                                Plats_commandes = plats + nom_plat
                                plats = Plats_commandes
                                i = -1

                            if(taille == 2 and l == 1 and quantite != 1):
                                nom_plat = str(quantite) + " " + plat + " " + "Medium" + " : " + str(price)  + "FDJ" + "\n"
                                Plats_commandes = nom_plat
                                plats = Plats_commandes
                                i = -1
                              
                            elif(taille == 2 and l != 1 and quantite != 1):
                                nom_plat = str(quantite) + " " + plat + " " + "Medium" + " : " + str(price)  + "FDJ" + "\n"
                                Plats_commandes = plats + nom_plat
                                plats = Plats_commandes
                                i = -1



                            if(taille == 3 and l == 1 and quantite == 1):
                                nom_plat = str(quantite) + " " + plat + " " + "Small" + " : " + str(price)  + "FDJ" + "\n"
                                Plats_commandes = nom_plat
                                plats = Plats_commandes
                                i = -1
                              
                            elif(taille == 3 and l != 1 and quantite == 1):
                                nom_plat = str(quantite) + " " + plat + " " + "Small" + " : " + str(price)  + "FDJ" + "\n"
                                Plats_commandes = plats + nom_plat
                                plats = Plats_commandes
                                i = -1

                            if(taille == 3 and l == 1 and quantite != 1):
                                nom_plat = str(quantite) + " " + plat + " " + "Small" + " : " + str(price)  + "FDJ" + "\n"
                                Plats_commandes = nom_plat
                                plats = Plats_commandes
                                i = -1
                              
                            elif(taille == 3 and l != 1 and quantite != 1):
                                nom_plat = str(quantite) + " " + plat + " " + "Small" + " : " + str(price)  + "FDJ" + "\n"
                                Plats_commandes = plats + nom_plat
                                plats = Plats_commandes
                                i = -1

                elif(i in {11, 12, 13}):
                    quantite = Panier[k + 2]
                    price = Panier[k + 3]
                    for numero, plat in choix:
                        if(i == numero and l == 1):
                            nom_plat = str(quantite) + " " + plat + " : " + str(price)  + "FDJ" + "\n"
                            Plats_commandes = nom_plat
                            plats = Plats_commandes
                            i = -1

                        elif(i == numero and l != 1):
                            nom_plat = str(quantite) + " " + plat + " : " + str(price)  + "FDJ" + "\n"
                            Plats_commandes = plats + nom_plat
                            plats = Plats_commandes
                            i = -1
                          

                elif(i in {21, 22, 23}):
                    quantite = Panier[k + 2]
                    price = Panier[k + 3]
                    for numero, plat in choix:
                        if(i == numero and l == 1):
                            nom_plat = str(quantite) + " " + plat + " : " + str(price)  + "FDJ" + "\n"
                            Plats_commandes = nom_plat
                            plats = Plats_commandes
                            i = -1

                        elif(i == numero and l != 1):
                            nom_plat = str(quantite) + " " + plat + " : " + str(price)  + "FDJ" + "\n"
                            Plats_commandes = plats +  nom_plat
                            plats = Plats_commandes
                            i = -1

                elif(i in {31, 32, 33}):
                     quantite = Panier[k + 2]
                     price = Panier[k + 3]
                     for numero, plat in choix:
                        if(i == numero and l == 1):
                            nom_plat = str(quantite) + " " + plat + " : " + str(price)  + "FDJ" + "\n"
                            Plats_commandes = nom_plat
                            plats = Plats_commandes
                            i = -1

                        elif(i == numero and l != 1):
                            nom_plat = str(quantite) + " " + plat + " : " + str(price)  + "FDJ" + "\n"
                            Plats_commandes = plats +  nom_plat
                            plats = Plats_commandes
                            i = -1

                elif(i in {41, 42, 43}):
                     quantite = Panier[k + 2]
                     price = Panier[k + 3]
                     for numero, plat in choix:
                        if(i == numero and l == 1):
                            nom_plat = str(quantite) + " " + plat + " : " + str(price)  + "FDJ" + "\n"
                            Plats_commandes = nom_plat
                            plats = Plats_commandes
                            i = -1

                        elif(i == numero and l != 1):
                            nom_plat = str(quantite) + " " + plat + " : " + str(price)  + "FDJ" + "\n"
                            Plats_commandes = plats + nom_plat 
                            plats = Plats_commandes
                            i = -1

                elif(i in {5, 6, 14, 15, 24, 25, 34, 35, 44, 45}):
                     quantite = Panier[k + 2]
                     price = Panier[k + 3]
                     for numero, plat in choix:
                        if(i == numero and l == 1):
                            nom_plat = str(quantite) + " " + plat + " : " + str(price)  + "FDJ" + "\n"
                            Plats_commandes = nom_plat
                            plats = Plats_commandes
                            i = -1

                        elif(i == numero and l != 1):
                            nom_plat = str(quantite) + " " + plat + " : " + str(price)  + "FDJ" + "\n"
                            Plats_commandes = plats +  nom_plat 
                            plats = Plats_commandes 
                            i = -1           

            else:
                 i = i + 1
                 continue
            
            i = i + 1
            k = k + 4
            if(k == lengh):
                break

        else:
                i = i + 1

    print(Plats_commandes)

     # Obtention de la date actuelle
    date_actuelle = datetime.now()
    date_format = "%d-%m-%Y %H:%M:%S"
    date_actuelle = datetime.now().strftime(date_format)


    conn = connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO Commande(Plats_commandes, ID_Client, Total_commande, Date_commande) VALUES (?, ?, ?, ?)", (Plats_commandes, id_client[0][0], T, date_actuelle))
    conn.commit() 

    c.execute("SELECT ID_Commande FROM Commande WHERE Date_commande = ?", (date_actuelle,))
    result = c.fetchall()

    c.execute("INSERT INTO Facture(ID_Client, ID_Commande, Total_facture, Date_facture) VALUES (?, ?, ?, ?)", (id_client[0][0], result[0][0], T, date_actuelle))
    conn.commit() 

    c.execute("SELECT ID_Facture FROM Facture WHERE Date_facture = ?", (date_actuelle,))
    result = c.fetchall()

    c.close()
    

    global text
    L1 = Plats_commandes
    L2 = str(T)
    Titre = "***************Facture du commande***************"
    text = Titre + "\n" + L1 + L2 + "FDJ"


    created_pdf("facture.pdf", text)
    sender_email = "speedycart564@gmail.com"
    sender_password = "txsv yhew txsd mkyr"
    recipient_email = Email
    subject = "Facture à payer"
    body = f"""Bonjour,

Nous vous écrivons pour vous informer qu'une facture est actuellement en attente de paiement pour votre compte. Veuillez trouver ci-joint les détails de la facture :

- Numéro de facture : {result[0][0]}
- Date de facturation : {str(date_actuelle)}
- Montant total dû : {T} FDJ


Si vous avez des questions ou avez besoin d'assistance supplémentaire, n'hésitez pas à nous contacter à [adresse e-mail] ou au [numéro de téléphone].

Cordialement,
[Speedy Cart]
"""
    
    attachment_path = "facture.pdf"
    send_email(sender_email, sender_password, recipient_email, subject, body, attachment_path)

    sender_email = "speedycart564@gmail.com"
    sender_password = "txsv yhew txsd mkyr"
    recipient_email = "speedycartcaissier@gmail.com"
    subject = "Facture à payer"
    body = f"""

Cher/Chère [Caissier/ Caissière],

Nous vous envoyons la facture ci-dessous qui nécessite votre attention et votre action pour le paiement :

- Numéro de la facture : {result[0][0]}
- Date d'émission : {str(date_actuelle)}
- Montant total dû : {T} FDJ

Nous vous remercions pour votre attention à cette affaire.

Cordialement,
[SpeedyCart]
"""
    
    send_email(sender_email, sender_password, recipient_email, subject, body, attachment_path)

def created_pdf(file_name, text):
    # Créer un fichier PDF
    c = canvas.Canvas(file_name, pagesize=letter)

    # Séparation du texte en lignes individuelles
    lines = text.split("\n")

    # Position de départ pour dessiner le texte
    x = 100
    y = 750

    # Dessiner chaque ligne individuelle avec un saut de ligne
    for line in lines:
        c.drawString(x, y, line)
        y -= 20  # Ajuster la position verticale pour la prochaine ligne
        if y < 50:
            c.showPage()  # Si la page est pleine, passer à la page suivante
            y = 750     # Réinitialiser la position verticale pour la nouvelle page

    # Enregistrer le fichier PDF
    c.save()

def send_email(sender_email, sender_password, recipient_email, subject, body, attachment_path):
    # Configurer le serveur SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Créer le message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Corps du message
    msg.attach(MIMEText(body, 'plain'))

    
    # Pièce jointe (la facture)
    with open(attachment_path, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name="facture.pdf")
    part['Content-Disposition'] = f'attachment; filename="{attachment_path}"'
    msg.attach(part)

    # Se connecter au serveur SMTP et envoyer l'e-mail
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("E-mail envoyé avec succès.")
    except Exception as e:
        print("Erreur lors de l'envoi de l'e-mail:", str(e))
    finally:
        server.quit()
