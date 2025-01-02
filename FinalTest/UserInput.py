#   Import universal scripts
import Globals
import MessageContainer

#   Import full supporting scripts

#   Import partial supporting scripts

#   Import Python modules

# --------------------------------------- #


def GetUserInt(code):
    while True:
        try:
            userNum = int(input(MessageContainer.UserInstruction(code)))
            return userNum
        except:
            MessageContainer.ErrorMsg(2)