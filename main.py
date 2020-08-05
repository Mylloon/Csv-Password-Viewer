from tkinter import Tk, filedialog, Button, Label, Entry
import tkinter.font as tkfont
import csv
import webbrowser
from tkinter.messagebox import showinfo

# Commandes

def select_file():
	path_file = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("Fichier csv", "*.csv"), ("Fichier json (non pris en charge)", "*.json")))
	openfile(path_file)

def openfile(path):
	global list_url, list_user, list_pass, curseur, line_count
	global affichage_url, affichage_user, affichage_pass, affichage_curseur
	global barre_de_recherche

	for item in root.grid_slaves():
		item.destroy()

	with open(path) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter = ',')
		line_count = 0
		list_url = []
		list_user = []
		list_pass = []
		for row in csv_reader:
			if line_count != 0:
				list_url.append(row[6])
				list_user.append(row[7])
				list_pass.append(row[8])
			line_count += 1
		line_count -= 1

		Label(root, text = f"Il y a {line_count} comptes.", font = tkfont.Font(size = 20)).place(x = 460, y = 30)
		Button(root, text = "<", font=tkfont.Font(size = 30), command = previous_account).place(x = 100, y = 500)
		Button(root, text = ">", font=tkfont.Font(size = 30), command = next_account).place(x = 970, y = 500)

		Label(root, text = "URL :", font = tkfont.Font(size = 10)).place(x = 150, y = 180)
		Label(root, text = "User :", font = tkfont.Font(size = 10)).place(x = 145, y = 250)
		Label(root, text = "Password :", font = tkfont.Font(size = 10)).place(x = 120, y = 320)


		curseur = 0

		affichage_url = Label(root, text = list_url[curseur], font = tkfont.Font(size = 40))
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

		barre_de_recherche.bind("<Key>", barre_de_recherche_recup)

def affichage():
	global affichage_url, affichage_user, affichage_pass, affichage_curseur
	affichage_url.destroy()
	affichage_user.destroy()
	affichage_pass.destroy()
	affichage_curseur.destroy()

	affichage_url = Label(root, text = list_url[curseur], font = tkfont.Font(size = 40))
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

Button(root, text = "Browser file", command = select_file).place(x = 1000, y = 10)


root.mainloop()