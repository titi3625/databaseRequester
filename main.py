#!/usr/bin/python3


from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from database import edb, idb
import requests


class programm():

    def __init__(self, name):
        self.root = Tk()
        center(self.root, 650, 480)
        self.root.title(name)

        # Initialize the frame
        self.app = Frame(self.root)

        # Initialize the current list
        self.current = []

    def loadMenu(self):
        self.menubar = Menu(self.root)

        function = self.setFrame(planRequestFrame)
        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Recherche de plan", command=function)
        self.menubar.add_cascade(label="Fonction", menu=self.menu1)

        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="Aide", command=infoCommand)
        self.menubar.add_cascade(label="A propos", menu=self.menu2)

        self.root.config(menu=self.menubar)


    def setFrame(self, creationFunction):
        """ Change the current main frame of the programm
        @param createFunction the main frame creation function. """
        self.app.destroy()
        self.app = creationFunction(self.root)

    def launch(self):
        self.root.mainloop()




def planRequestFrame(root):
    """ This frame contains a text-area and a button.
    When pressed, the content of the area is turned into a request,
    and then replaced by it's result. """
    
    app = Frame(root)
    app.pack(fill=BOTH, expand=1)

    # Ajout de la frame contenant les instruments de recherche
    searchFrame = Frame(app, width=800, height=100, borderwidth=0)
    searchFrame.pack(fill=BOTH)

    # Ajout du champ de recherche
    labelPlan = Label(searchFrame, text="Rechercher un plan : ")
    labelPlan.pack(side=LEFT, padx=10, pady=10)

    plan = StringVar()
    searchEntry = Entry(searchFrame, textvariable=plan, width=30)
    searchEntry.pack(side=LEFT, padx=10, pady=10)

    # Ajout de la frame contenant les résultats
    resultFrame = Frame(app, width=800, height=600, borderwidth=0)
    resultFrame.pack(fill=BOTH, padx=10, pady=10)

    textbox = Text(resultFrame)
    textbox.pack(side=BOTTOM, fill=BOTH)

    # Ajout de la frame de pied de page
    footFrame = Frame(app, width=800, height=100, borderwidth=0)
    footFrame.pack(fill=BOTH)

    quitButton = Button(footFrame, text="Quitter", command=root.quit)
    quitButton.pack(side=RIGHT, padx=10, pady=10)

    ## Request parsing and performing
    def getText(plan):
        # Get the content, slice it and remove empty lines
        if plan.get() != "":
            content = plan.get()

            # nattoyage et decoupe de la chaine
            content = content.replace(" ", "").split(',')

            # Perform the request
            result, success, error = requests.requestPlanList(content)

            # Format the output string
            result = [';'.join(t) for t in result]
            fs = ""
            if result:
                fs += "SYMB_COMP;DESIGN;QTE\n"
                fs += '\n'.join(result) + '\n\n'

            if success:
                fs += "Requêtes effectuées :\n"
                fs += '\n'.join(success) + '\n\n'

            if error:
                fs += "Requêtes echouées :\n"
                fs += '\n'.join(error) + '\n\n'
            
            return fs
        else:
            showerror("Erreur", "Vous devez saisir un numéro de plan")
            return False

    def fun():
        result = getText(plan)
        if result != False:
            textbox.insert(END, result);

    # Ajout du bouton de recherche
    searchButton = Button(searchFrame, text="Rechercher", command=fun)
    searchButton.pack(side=LEFT, padx=10, pady=10)

    return app


def listCommand(root):

    app = Frame(root)
    app.pack(fill=BOTH, expand=1)

    # Add the textbox frame
    fRequest = Frame(app)
    fRequest.style = Style()
    fRequest.style.theme_use("clam")
    fRequest.pack(fill=BOTH, expand=1)

	
def infoCommand():

    top = Toplevel()
    center(top, 400, 200)
    top.title("Informations")

    infoMessage = '''
    Gestion de base de donnée pour matériel SNCF.
    
        Quentin Campos © 2015
        quentin.campos@gmail.com
    '''

    msg = Label(top, text=infoMessage)
    msg.pack(fill=BOTH, side=TOP, expand=1)

    button = Button(top, text="Quitter", command=top.destroy)
    button.pack(fill=BOTH, expand=1)


def center(win, width, height):
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


if __name__ == "__main__":
    main = programm("Plan Requester v0.2")
    main.loadMenu()
    main.launch()











