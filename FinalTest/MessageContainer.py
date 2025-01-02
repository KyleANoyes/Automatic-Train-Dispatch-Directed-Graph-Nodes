#   Import universal scripts
import Globals
import MessageContainer

#   Import full supporting scripts

#   Import partial supporting scripts

#   Import Python modules

# --------------------------------------- #


def UserMsg(code, context0="", context1="", context2="", context3=""):
    match code:
        case 0:
            print("Welcome to demo mode! Here we can rapidly test path solutions to")
            print("any part of the layout in a rapid and fun visual way\n")
            print("Please ensure that the global variable DEBUG_LITE is enabled\n")
        case 1:
            print("Select one of the following option numbers")
            print("\t 0. Automated Train Pathing")
            print("\t 1. Signal path placement/detection (INOP)")
            print("\t-1: Exit program")
        case 2:
            print("\nThank you for testing my pathing tool!!")
        case 3:
            print("\nSorry, but that feature is not ready yet as I still need to make it")
            print("It should be done soon as the pathing agent uses the same framework\n")
        case 4:
            print("\nPlease provide the following 4 inputs: ")
        case 5:
            #   Cleanup the output so it looks better visually
            context0Fixed, context1Fixed = StringCleanup(1, context0, context1)
            print(F"\nFound path - Group:   {context0Fixed}")
            print(F"Found path - Index:   {context1Fixed}\n")
        case _:
            print(F"ERROR: MessageContainer.UserMsg called with invalid code: {code}\n")

def ErrorMsg(code, context0="", context1="", context2="", context3=""):
    match code:
        case 0:
            print("grug find Shaman or grug find Complexity. This make grug unhappy >:(")
            print("grug now yell big brain programmer need smol brain program")
            print("https://grugbrain.dev/\n")
        case 1:
            print("ERROR: Impossible state reached. How did you manage this??\n")
        case 2:
            print("Invalid input: Only numbers are allowed\n")
        case 3:
            print(F"Input is out of range. {context0} range: {context1} to {context2}\n")
        case 4:
            print(F"A path was not discovered\n")
        case 5:
            print(F"Call to StepHandler.IncramentStepSwitch failed")
            print(F"Terminating path search for path: [{context0}, {context1}]")
            print(F"Child ID: {context2}\n")
        case 6:
            print(F"Call to StepHandler.IncramentStepFull failed")
            print(F"Terminating path search for path: [{context0}, {context1}]")
            print(F"Child ID: {context2}\n")
        case 6:
            print(F"Call to StepHandler.InverseDirection failed")
            print(F"Terminating path search for path: [{context0}, {context1}]")
            print(F"Child ID: {context2}\n")
        case _:
            print(F"ERROR: MessageContainer.ErrorMsg called with invalid code: {code}\n")

def DebugMsg(code, context0="", context1="", context2="", context3=""):
    match code:
        case 0:
            print(F"ConfigTrackConnectionInverse yAxis = {context0}")
        case 1:
            print(F"ConfigTrackSwitchInverse yAxis = {context0}, xAxis = {context1}, dirVector = {context2}")
        case 2:
            print(F"{context0}, {context1} -- trackGroup = {context2}, trackIndex = {context3}")
        case 3:
            print(F"\nStart:  [{context0}, {context1}]")
            print(F"Target: [{context2}, {context3}]\n")
        case 4:
            print(F"ConfigSwitchConnectionInverse Y-Axis: {context0} - Switch Connection list: {context1}")
            print(F"ConfigSwitchConnectionInverse Y-Axis: {context0} - Switch Direct. Inverse: {context2}")
        case _:
            print(F"ERROR: MessageContainer.DebugMsg called with invalid code: {code}\n")

def UserInstruction(code, context0=""):
    match code:
        case 0:
            return "Please enter number selection: "
        case 1:
            return "Enter starting track group: "
        case 2:
            return "Enter starting track index: "
        case 3:
            return "Enter target track group: "
        case 4:
            return "Enter target track index: "
        case _:
            print(F"ERROR: MessageContainer.DebugMsg called with invalid code: {code}\n")


def WarningMsg(code, context0="", context1="", context2="", context3=""):
    match code:
        case 0:
            print(F"Warning: A self revolving loop was identified at:")
            print(F"trackGroup: {context0} --- trackIndex: {context1}")
            print(F"Impact: This can result in a logic error realted to vector swapping when")
            print(F"    stepping into this switch/node. Pathing may not work as expected")
            print(F"Resolution: Split this switch into two seperate blocks")
        case _:
            print(F"ERROR: MessageContainer.WarningMsg called with invalid code: {code}\n")


def ProgramInfo(code):
    match code:
        case 0:
            print("# ------------------------------------------------------------- #")
            print("Program:         Automatic Layout Control")
            print("Developer:       Kyle Noyes")
            print("Contact:         https://github.com/KyleANoyes or https://www.linkedin.com/in/kyle-noyes-63a8691b2/")
            print("Version:         0.1")
            print("Build Date:      Jan 01, 2025")
            print("Known issues:    - Problem persists when interacting with '*' switches, but not sure where")
            print("TODO:            - Create a gnarly script to convert the JMRI panel .xml file into")
            print("                     an array of data components that this program can read")
            print("# ------------------------------------------------------------- #\n")
        case _:
            print(F"ERROR: MessageContainer.ProgramInfo called with invalid code: {code}\n")


def StringCleanup(code, context0="", context1="", context2="", context3=""):
    match code:
        case 1:
            #   Convert each list element into a string with a set digit size, then
            #       append that to a new string that'll be returned to the user
            context0Fixed = ""
            context1Fixed = ""
            for i in range(len(context0)):
                context0Fixed += str(context0[i]).zfill(Globals.DIGIT_PRINT_FORCE) + ", "
                context1Fixed += str(context1[i]).zfill(Globals.DIGIT_PRINT_FORCE) + ", "
            context0Fixed = context0Fixed[:-2]
            context1Fixed = context1Fixed[:-2]
        
            return context0Fixed, context1Fixed
        case _:
            print(F"ERROR: MessageContainer.StringCleanup called with invalid code: {code}\n")