from tkinter import *
from tkinter import messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageFilter
from sqlite3 import *


def main():

    def on_entry_click(event, entry, default_text):
        if entry.get() == default_text:
            entry.delete(0, END)
            entry.config(fg='black')

    def on_entry_leave(event, entry, default_text):
        if entry.get() == "":
            entry.insert(2, default_text)
            entry.config(fg='grey')
    

    def animate_button(button):
        button.config(relief=SUNKEN)
        button.after(100, lambda: button.config(relief=RAISED))

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
    # Création de la fenêtre principale
    Fenetre_connexion = Tk()
    Fenetre_connexion.title("SpeedyCart")
    Fenetre_connexion.resizable(False, False)



    # Obtenir la taille de l'écran
    screen_x = Fenetre_connexion.winfo_screenwidth()
    screen_y = Fenetre_connexion.winfo_screenheight()

    # Taille de la fenêtre
    window_x = 1000
    window_y = 570

    # Calcul de la position pour centrer la fenêtre
    posX = (screen_x - window_x) // 2
    posY = (screen_y - window_y) // 2

    # Géométrie de la fenêtre
    geo = "{}x{}+{}+{}".format(window_x, window_y, posX, posY)
    Fenetre_connexion.geometry(geo)

    #Declaration des champs
    Var_nom = StringVar()
    Var_mail = StringVar()
    Var_adr = StringVar()
    Var_pass = StringVar()
    Var_num = IntVar()

    Name_Entry = Entry()
    Mail_Entry = Entry()
    Number_Entry = Entry()
    Adress_Entry = Entry()
    pass_Entry = Entry()


    # Image d'arrière-plan
    try:
        background_image = Image.open("Ajouter un titre.png")
        background_image = background_image.resize((600, 570))
        
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = Label(Fenetre_connexion, image=background_photo)
        background_label.place(x=0, y=0)
    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")


    # Cadre parent pour les widgets
    frame = Frame(Fenetre_connexion, width=580, height=650, bg='#f0f0f0', borderwidth=0)
    frame.place(x = 300, y = 0)
    # Police de caractères
    label_font = tkfont.Font(family='Helvetica', size=14)
    button_font = tkfont.Font(family='Arial', size=11, weight='bold')
    saisie_font = tkfont.Font(family = 'Arial', size = 11)

    # Image cercle gauche
    
    try:
        background_image1 = Image.open("log_in_page_4x-removebg-preview1.png")
        background_image1 = background_image1.resize((99, 163))
        
        background_photo1 = ImageTk.PhotoImage(background_image1)
        background_label1 = Label(Fenetre_connexion, image=background_photo1)
        background_label1.place(x=510, y=388)
    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")


    # Image cercle droite
    
    try:
        background_image2 = Image.open("log_in_page_4x-removebg-preview2.png")
        background_image2 = background_image2.resize((158, 160))
        
        background_photo2 = ImageTk.PhotoImage(background_image2)
        background_label2 = Label(Fenetre_connexion, image=background_photo2)
        background_label2.place(x=840, y=0)
    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    # Créer un Canvas pour afficher le texte transparent : Log In
    canvas = Canvas(frame, width=115, height=150, bd=0, highlightthickness=0)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    # Ajouter le texte transparent "Login" sur le Canvas
    text_login = canvas.create_text(115, 150, text="Log In", font=("Arial", 26), fill='#c64494')


    # Image Register_Login
    
    try:
        background_image4 = Image.open("log_in_page_4x (1).jpg")
        background_image4 = background_image4.resize((105, 28))
            
        background_photo4 = ImageTk.PhotoImage(background_image4)
        background_label4 = Label(Fenetre_connexion, image=background_photo4)
        background_label4.place(x=577, y=40)
    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")


    # Image user
        
    try:
        background_image5 = Image.open("user-removebg-preview.png")
        background_image5 = background_image5.resize((38, 35))
            
        background_photo5 = ImageTk.PhotoImage(background_image5)
        background_label5 = Label(Fenetre_connexion, image=background_photo5, borderwidth=0)
        background_label5.place(x=820, y=166)
    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    # Image pass
            
    try:
        background_image6 = Image.open("pass-removebg-preview.png")
        background_image6 = background_image6.resize((38, 35))
            
        background_photo6 = ImageTk.PhotoImage(background_image6)
        background_label6 = Label(Fenetre_connexion, image=background_photo6, borderwidth=0)
        background_label6.place(x=821, y=225)
    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    # Image fleche
            
    try:
        background_image7 = Image.open("fleche_preview_rev_1.jpeg")
        background_image7 = background_image7.resize((30, 35))
            
        background_photo7 = ImageTk.PhotoImage(background_image7)
        background_label7 = Label(frame, image=background_photo7)
        background_label7.place(x=300, y=559)
    except FileNotFoundError:
        print("Image non trouvée. Assurez-vous que le chemin est correct.")

    Mail_default = "E-mail"
    password_default = "password"

    Email_entry = Entry(frame, width=35, font=saisie_font, bg='#d9d9d9', fg='grey', borderwidth = 0)
    Email_entry.insert(0, Mail_default)
    Email_entry.bind("<FocusIn>", lambda event: on_entry_click(event, Email_entry, Mail_default))
    Email_entry.bind("<FocusOut>", lambda event: on_entry_leave(event, Email_entry, Mail_default))
    Email_entry.place(x=70, y=206, height=35)

    password_entry = Entry(frame, show='*', width=35, font=saisie_font, bg='#d9d9d9', fg='grey', relief='ridge', borderwidth=0)
    password_entry.config(show='')
    password_entry.insert(0, password_default)
    password_entry.bind("<FocusIn>", lambda event: on_password_entry_click(event, password_entry))
    password_entry.bind("<FocusOut>", lambda event: on_password_entry_leave(event, password_entry))
    password_entry.place(x=70, y=265, height=35)


    # Bouton de connexion

    login_button = Button(frame, text="Log In", command=login, height=2, width=13, font=button_font, bg='#ba4395', fg='#FFFFFF', relief="solid", borderwidth=0)
    login_button.place(x=160, y=320)
    login_button.bind("<Enter>", lambda event: animate_button(login_button))


    # Texte cliquable pour l'inscription
    sign_button = Label(frame, text="Create Your Account", font=('Arial', 12), bg='#f0f0f0', fg='#8c8c8c', cursor="hand2")
    sign_button.place(x = 150, y = 565)
    sign_button.bind("<Button-1>", Sign_in)  

    """
    # Texte cliquable pour la restauration
    forgot_pass_button = Label(frame, text="Forgot password ?", font=('Arial', 12), bg='#f0f0f0', fg='#8c8c8c', cursor="hand2")
    forgot_pass_button.place(x = 160, y = 378)
    forgot_pass_button.bind("<Button-1>", forgot)  
    """
    # Placement du cadre dans la fenêtre
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Lancement de la boucle principale
    Fenetre_connexion.mainloop()

main()