#   Import universal scripts
import Globals
import MessageContainer

#   Import full supporting scripts
import StepHandler
import DataCheck

#   Import partial supporting scripts
from ClassContainer import SignalPath
from ClassContainer import SignalContainer

#   Import Python modules

# --------------------------------------- #

def SignalPathMain(trackLayout):
    signalList = []

    signalList.append(SignalContainer("S00", [9, 1], 2))

    for i in range(len(signalList)):
        CreateSignalPath(trackLayout, signalList[i])


def CreateSignalPath(trackLayout, singalInstance):
    #   Create path container and begin search
    path = [[], []]

    #   Create path objects and initialize two starts
    path[0].append(SignalPath('+', singalInstance.signalLocation[0], singalInstance.signalLocation[1]))
    path[1].append(SignalPath('-', singalInstance.signalLocation[0], singalInstance.signalLocation[1]))

    for distanceSearch in range(3):
        for directionGroup in range(len(path)):
            for subGroup in range(len(path[directionGroup])):
                #   Check if the signal is at the end point yet
                DataCheck.CheckTrackEndLite(trackLayout, path, path[directionGroup][subGroup], directionGroup, subGroup)

                if path[directionGroup][subGroup].endReached == False:
                    StepHandler.IncramentStepLite(trackLayout, path[directionGroup][subGroup])


    pass