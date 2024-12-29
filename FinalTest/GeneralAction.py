#   Import supporting scripts

#   Import specific parts of modules

#   Import Python modules

# --------------------------------------- #


def InverseDirection(currentPath):
    if currentPath.direction[-1] == "-":
        currentPath.direction[-1] = "+"
    else:
        currentPath.direction[-1] = "-"
    
    return currentPath