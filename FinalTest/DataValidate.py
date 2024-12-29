#   Import universal scripts
import Globals
import MessageContainer

#   Import full supporting scripts

#   Import partial supporting scripts

#   Import Python modules

# --------------------------------------- #


def ValidRangeInt(numTest, num0, num1, inclusive):
    if inclusive == True:
        if numTest >= num0 and numTest <= num1:
            return True
        else:
            return False
    else:
        if numTest > num0 and numTest < num1:
            return True
        else:
            return False