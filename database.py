#!/usr/bin/python3

import os


# Constants for files names
databaseFileName = "database/items_database.csv"
ensFileName = "database/ens_database.csv"

class database:

    def __init__(self, fileName):
        # Open the database and read it.
        with open(fileName, 'r') as databaseFile:
            # Don't take the last character '\n'
            lines = [l[:len(l)-1] for l in databaseFile.readlines()]

            # Separate the index from the lines.
            header, lines = lines[0].split(';'), lines[1::]
            
            # Then parse both.
            self.index = {header[i]:i for i in range(len(header))}
            self.datas = [l.split(';') for l in lines]

            # Keep some values for updates saving.
            self.header = header
            self.fileName = fileName


    def __str__(self):
        return self.fileName + '\t' + " ".join(self.index.keys())

    def save(self):
        ''' Save the current database into csv format.
        Caution : this will erase the initial file. '''
        s = ';'.join(self.header) + '\n'
        l = [';'.join(l) for l in self.datas]
        s += '\n'.join(l)

        with open("test", "w") as f:
            f.write(s)


    def request(self, field, value):
        ''' Do a request on the items table to seach for
        an item which given field correspond to the given value. '''
        return self.entrysetRequest(self.datas, field, value)

    def entrysetRequest(self, entries, field, value):
        ''' Do a request on the given entry set
        which must be a subset of the database datas. '''
        i = self.index[field]
        l = [l for l in entries if value == l[i]]
        # We hope there is only one good result for the moment
        return l

    def getField(self, entry, field):
        ''' Get a specific field of an entry returned by
        a request on this table. '''
        return entry[self.index[field]]

    def getFields(self, entries, fields):
        l = [ [self.getField(i, j) for j in fields] for i in entries]
        return l

    def setField(self, entry, field, value):
        e = entry.copy()
        e[self.index[field]] = value
        return e



idb = database(databaseFileName)
edb = database(ensFileName)





if __name__ == '__main__':
    
    plan = input("Numéro de plan (plan/repere) : ")
    l = requestPlan(plan)

    v = ("SYMB_COMP", "DESIGN", "QTE")
    l = [ [edb.getField(i, j) for j in v] for i in l]
    l = [';'.join(i) for i in l]
    l = [';'.join(v)] + l
    l = '\n'.join(l)
    print(l, "\n\n")

    print("Nom du fichier dans lequel le résultat sera enregistré")
    print("(Attention, si le fichier existe déjà, il sera effacé)")
    fileName = input("Nom du fichier (sans extension)\n\tLaisser vide pour un nom automatique : ")

    if fileName == "":
        fileName = str(plan)

    fileName += ".csv"


    print("\nLe fichier crée peut être ouvert avec Excel mais ne sera pas correctement")
    print("interprété. Pour avoir les informations correctes, il vaut mieux l'ouvrir")
    print("avec un éditeur de texte. (bloc note)")
    print("Clic droit > Ouvrir avec > Bloc Note")

    with open(fileName, 'w') as f:
        f.write(l)


    print("\n\n")
    os.system("PAUSE")

    
    
