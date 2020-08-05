from tkinter import Tk, filedialog, Button, Label, Entry, PhotoImage
import tkinter.font as tkfont
import csv
import webbrowser
from tkinter.messagebox import showinfo

# Commandes

def select_file():
	path_file = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("Fichier csv", "*.csv"), ("Tous les fichiers (non supporté)", "*.*")))
	openfile(path_file)

def openfile(path):
	with open(path, "r") as file:
		premiere_ligne = file.readline()
	if premiere_ligne == "folder,favorite,type,name,notes,fields,login_uri,login_username,login_password,login_totp\n":
		openfile_bitwarden(path)
	elif premiere_ligne == '"url","username","password","httpRealm","formActionOrigin","guid","timeCreated","timeLastUsed","timePasswordChanged"\n':
		openfile_firefox(path)
	elif premiere_ligne == "name,url,username,password\n":
		openfile_chrome(path)
	else:
		showinfo("Erreur", "Ce format de fichier csv n'est pas reconnu.\nMerci d'utilisé Firefox ou Bitwarden.")

def openfile_chrome(path):
	global list_url, list_user, list_pass, line_count, liste_name

	for item in root.grid_slaves():
		item.destroy()

	with open(path) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter = ',')
		line_count = 0
		list_url = []
		list_user = []
		list_pass = []
		liste_name = []
		for row in csv_reader:
			if line_count != 0:
				liste_name.append(row[0])
				list_url.append(row[1])
				list_user.append(row[2])
				list_pass.append(row[3])
			line_count += 1
		line_count -= 1

	lancement()

def openfile_firefox(path):
	global list_url, list_user, list_pass, line_count, liste_name

	for item in root.grid_slaves():
		item.destroy()

	with open(path) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter = ',')
		line_count = 0
		list_url = []
		list_user = []
		list_pass = []
		liste_name = []
		for row in csv_reader:
			if line_count > 1:
				liste_name.append(row[0]) # pas de nom, alors ce sera l'URL
				list_url.append(row[0])
				list_user.append(row[1])
				list_pass.append(row[2])
			line_count += 1
		line_count -= 2

	lancement()

def openfile_bitwarden(path):
	global list_url, list_user, list_pass, line_count, liste_name

	for item in root.grid_slaves():
		item.destroy()

	with open(path) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter = ',')
		line_count = 0
		list_url = []
		list_user = []
		list_pass = []
		liste_name = []
		for row in csv_reader:
			if line_count != 0:
				liste_name.append(row[3])
				list_url.append(row[6])
				list_user.append(row[7])
				list_pass.append(row[8])
			line_count += 1
		line_count -= 1

	lancement()

def lancement():
	global lancement_affichage_ligne
	global barre_de_recherche
	global affichage_url, affichage_user, affichage_pass, affichage_curseur, curseur
	global root

	clear_second_lancement()

	lancement_affichage_ligne = Label(root, text = f"Il y a {line_count} comptes.", font = tkfont.Font(size = 20))
	lancement_affichage_ligne.place(x = 460, y = 30)
	Button(root, text = "<", font=tkfont.Font(size = 30), command = previous_account).place(x = 100, y = 500)
	Button(root, text = ">", font=tkfont.Font(size = 30), command = next_account).place(x = 970, y = 500)

	Label(root, text = "URL :", font = tkfont.Font(size = 10)).place(x = 150, y = 180)
	Label(root, text = "User :", font = tkfont.Font(size = 10)).place(x = 145, y = 250)
	Label(root, text = "Password :", font = tkfont.Font(size = 10)).place(x = 120, y = 320)


	curseur = 0

	affichage_url = Label(root, text = list_url[curseur], font = tkfont.Font(size = 40, underline = True), fg = "blue", cursor = "hand2")
	affichage_user = Entry(root, font = tkfont.Font(size = 40))
	affichage_pass = Entry(root, font = tkfont.Font(size = 40))

	affichage_user.insert(0, list_user[curseur])
	affichage_pass.insert(0, list_pass[curseur])
	
	affichage_url.bind("<Button-1>", callback)

	affichage_url.place(x = 200, y = 160)
	affichage_user.place(x = 200, y = 230)
	affichage_pass.place(x = 200, y = 300)

	affichage_curseur = Label(root, text = "Compte numéro 1", font = tkfont.Font(size = 15))
	affichage_curseur.place(x = 500, y = 500)

	barre_de_recherche = Entry(root, font = tkfont.Font(size = 15), width = len(str(line_count)))
	boutton_recherche = Button(root, text = "Rechercher", command = lambda:recherche(barre_de_recherche.get()))
	barre_de_recherche.place(x = 120, y = 10)
	boutton_recherche.place(x = 40, y = 10)

	
	root.title(f"CSV PASSWORD VIEWER - {liste_name[curseur]}")

	barre_de_recherche.bind("<Key>", barre_de_recherche_recup)

def affichage():
	global affichage_url, affichage_user, affichage_pass, affichage_curseur, root
	affichage_url.destroy()
	affichage_user.destroy()
	affichage_pass.destroy()
	affichage_curseur.destroy()

	affichage_url = Label(root, text = list_url[curseur], font = tkfont.Font(size = 40, underline = True), fg = "blue", cursor = "hand2")
	affichage_user = Entry(root, font = tkfont.Font(size = 40))
	affichage_pass = Entry(root, font = tkfont.Font(size = 40))

	affichage_user.insert(0, list_user[curseur])
	affichage_pass.insert(0, list_pass[curseur])
	
	affichage_url.bind("<Button-1>", callback)

	affichage_url.place(x = 200, y = 160)
	affichage_user.place(x = 200, y = 230)
	affichage_pass.place(x = 200, y = 300)

	affichage_curseur = Label(root, text = f"Compte numéro {curseur+1}", font = tkfont.Font(size = 15))
	affichage_curseur.place(x = 500, y = 500)

	
	root.title(f"CSV PASSWORD VIEWER - {liste_name[curseur]}")

def clear_second_lancement():
	global lancement_affichage_ligne, affichage_url, affichage_curseur, barre_de_recherche
	try:
		lancement_affichage_ligne.destroy()
		affichage_url.destroy()
		affichage_curseur.destroy()
		barre_de_recherche.destroy()
	except:
		pass

def previous_account():
	global curseur
	if curseur > 0:
		curseur -= 1
		affichage()
	else:
		showinfo("Erreur", "Il n'y a plus de compte.")

def next_account():
	global curseur
	__curseur__ = curseur
	__curseur__ += 1
	if line_count > __curseur__:
		curseur += 1
		affichage()
	else:
		showinfo("Erreur", "Il n'y a plus de compte.")

def callback(event):
    webbrowser.open_new(list_url[curseur])

def recherche(numero):
	global curseur
	try:
		numero = int(numero)
		numero -= 1
	except:
		return showinfo("Erreur", f"Veuillez renseigner un numéro.")
	if not line_count > numero or not numero >= 0:
		return showinfo("Erreur", f"Ce numéro de compte n'existe pas (max {line_count}).")
	curseur = numero
	affichage()

def barre_de_recherche_recup(event):
    touche = event.keysym
    if touche == "Return":
        recherche(barre_de_recherche.get())

# Affichage

root=Tk()
root.geometry("1100x600")
root.title("CSV PASSWORD VIEWER")
root.resizable(False, False)
root.iconphoto(False, PhotoImage(file='favicon.png'))

Button(root, text = "Browser file", command = select_file).place(x = 1000, y = 10)


root.mainloop()