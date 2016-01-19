#!/usr/bin/python3


from tkinter import *
from tkinter.ttk import *
from database import edb, idb
import requests


class programm():

    def __init__(self, name):
        self.root = Tk()
        self.root.geometry("800x600+300+300")
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
        function = lambda:self.setFrame(frameFunction)
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

    # Add the textbox frame
    fRequest = Frame(app)
    fRequest.style = Style()
    fRequest.style.theme_use("clam")
    fRequest.pack(fill=BOTH, expand=1)

    area = Text(fRequest)
    area.pack(fill=BOTH, expand=1)

    area.insert("1.0", "EXEMPLE\n001770 000000\n00981355")
    #area.insert("1.0", "80984252")

    # Request parsing and performing
    def getText(area):
        # Get the content, slice it and remove empty lines
        areaContent = area.get("1.0", "end")
        areaLines = areaContent.split('\n')
        while '' in areaLines: areaLines.remove('')

        # Perform the request
        result, success, error = requests.requestPlanList(areaLines)

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

    fun = lambda: area.replace("1.0", "end", getText(area));

    # Add the button
    researsh = Button(app, text="Rechercher les plans", command=fun)
    researsh.pack(fill=BOTH, expand=1)

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











