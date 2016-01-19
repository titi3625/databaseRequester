#!/usr/bin/python3

from database import edb, idb

def checkSet(content):
    if not content or len(content) > 1:
        return None
    return content

def ensDataToItemData(data):
    symbol = edb.getField(data, "SYMB_COMP")
    return idb.request("SYMBOLE", symbol).pop()


def fusionFunc(a, b):
    t = a.copy()
    t[2] = str(int(a[2]) + int(b[2]))
    return t
        

def equalFunc(a, b):
    return a[0] == b[0]

    

def listFusion(itemList, fusion=fusionFunc, equal=equalFunc):

    l = []
    al = []
    for i in range(len(itemList)):
        item = itemList[i]
        if item in al: continue
        for j in itemList[i+1:]:
            if equal(item, j):
                item = fusion(item, j)
                al.append(j)
                
        l.append(item)
        
    return l
        
        


def getItemByPlan(plan, repere):
    """ Perform a request based on plan & repere numbers.
    """
    # Perform the request
    a = idb.request("PLAN", plan)
    a = idb.entrysetRequest(a, "REPERE", repere)

    # Check the values. Only one result should remain.
    if not checkSet(a):
        return None

    return a.pop()

def getItemById(symbol):
    """ Perform a request based on symbol identifier.
    """
    # Perform the request
    a = idb.request("SYMBOLE", symbol)

    # Check the values. Only one result should remain.
    if not checkSet(a):
        return None

    return a.pop()


def getComponentsOf(ensEntry, isEnsData=True):
    """ Get all the components of the piece,
    or the piece itself if it's a basic piece.
    """
    # Get the item entry from any type of entry.s
    entry = None
    if isEnsData:
        entry = ensDataToItemData(ensEntry)
    else:
        entry = ensEntry

    # Get the symbol
    symbol = idb.getField(entry, "SYMBOLE")

    # Get all the pieces of the plan
    components = edb.request("SYMB_ENS", symbol)

    # If there is no components for this plan,
    # then it's a basic piece.
    return components or None
    
    


def requestPlan(data):
    """ Perform a request to explode an item into basic parts.
    If the item is already basic, return itself.
    Otherwise, return each components exploded recursively.

    "data" must be a valid information : SYMBOLE or PLAN+REPERE separed
    by a blank space.
    """

    def getItemEntry(data):
        if len(data) == 8:
            return getItemById(data)
        elif len(data) == 6+6+1:
            a = data.split()
            return getItemByPlan(a[0], a[1])
        else:
            return None

    # Create the lists for keeping items.
    remainingItems = []
    basicItems = []

    # Get the first needed item we will explode.
    item = getItemEntry(data)
    if item is None:
        return item

    # The first item needs to be treated differently.
    components = getComponentsOf(item, isEnsData=False)
    if not components:
        # No components, then create a final entry and make it the only
        # basic item.
        symbol = idb.getField(item, "SYMBOLE")
        design = idb.getField(item, "DESIGN")
        qte = "1"
        falseEnsEntry = [None, symbol, None, design, qte]
        basicItem.append(falseEnsEntry)
    else:
        # Otherwise, there is some components, so add them into the
        # list of potentially exploded items.
        [remainingItems.append(t) for t in components]

    

    # While there is items to explode.
    while remainingItems:
        item = remainingItems.pop()

        # Get the components of the current item.
        components = getComponentsOf(item)

        # If no components for the item, it is a final item
        if not components:
            basicItems.append(item)

        # Otherwise, there is more items to explode
        else:
            [remainingItems.append(t) for t in components]

            
    for i in basicItems:print(i)
    # Then, get the interresting fields of the final result. (All the basic items)
    fields = ("SYMB_COMP", "DESIGN", "QTE")
    result = edb.getFields(basicItems, fields)

    # Merge the same items
    return listFusion(result)



def requestPlanList(plans):

    success = []
    error = []

    result = []
    
    for plan in plans:
        current = requestPlan(plan)
        if current:
            success.append(plan)
            result += current
        else:
            error.append(plan)

    return listFusion(result), success, error





