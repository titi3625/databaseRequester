#!/usr/bin/python3


from tkinter import *
from tkinter.ttk import *
from database import edb, idb
import requests


class programm():

    def __init__(self, name):
        self.root = Tk()
        self.root.geometry("800x500+250+250")
        self.root.title(name)
        self.root.style = Style()
        self.root.style.theme_use("clam")

        # Initialize the menu
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)

        # Initialize the frame
        self.app = Frame(self.root)

        # Initialize the current list
        self.current = []

    def addMenu(self, label, function=None):
        self.menuItem = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label=label, menu=self.menuItem)
        self.menuItem.add_command(label=label, command=function)
        

    def addMenuFrame(self, label, frameFunction):
        function = self.setFrame(frameFunction)
        self.addMenu(label, function)

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
        content = plan.get()
        listPlan = [content]
        #while ' ' in content: content.remove(' ')

        # Perform the request
        result, success, error = requests.requestPlanList(listPlan)

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
        
        return  fs


    fun = lambda: textbox.insert(END, getText(plan));

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
    top.title("Informations")
    top.geometry("400x200+750+400")

    infoMessage = '''
    Gestion de base de donnée pour matériel SNCF.
    
        Quentin Campos © 2015
        quentin.campos@gmail.com
    '''

    msg = Label(top, text=infoMessage)
    msg.pack(fill=BOTH, side=TOP, expand=1)

    button = Button(top, text="Quitter", command=top.destroy)
    button.pack(fill=BOTH, expand=1)




if __name__ == "__main__":
    main = programm("Plan Requester v0.2")
    
    main.addMenuFrame("Rechercher des plans", planRequestFrame)
    main.addMenu("A propos", infoCommand)

    main.launch()











