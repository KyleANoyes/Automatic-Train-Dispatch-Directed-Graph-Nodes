#   Import universal scripts
import Globals
import MessageContainer

#   Import full supporting scripts

#   Import partial supporting scripts

#   Import Python modules

# --------------------------------------- #


def GetVectorNum(currentPath):
    if currentPath.direction[-1] == "-":
        return 0
    else:
        return 1
    

def ListLenAboveMin(testList, min):
    if len(testList) >= min:
        return True
    else:
        return False