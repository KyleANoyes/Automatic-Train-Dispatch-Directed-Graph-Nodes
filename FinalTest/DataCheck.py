#   Import universal scripts
import Globals
import MessageContainer

#   Import full supporting scripts
import DataCollect
import GeneralAction

#   Import partial supporting scripts

#   Import Python modules

# --------------------------------------- #


def CheckTrackEndLite(trackLayout, path, currentPath, directionGroup, subGroup):
    if len(trackLayout.trackEnd[currentPath.trackGroup[-1]]) > 0:
        trackEndPoints = trackLayout.trackEnd[currentPath.trackGroup[-1]]
        for i in range(len(trackEndPoints)):
            if trackEndPoints[i] == currentPath.trackIndex[-1]:
                path[directionGroup][subGroup].pathEnd = True


def CheckSwitch(currentPath, trackLayout):    
    # Check if next point is a switch
    foundVector = 0

    # If switch and not on cooldown
    if currentPath.switchStepWait == 0 and currentPath.switchSequence == False and currentPath.cooldown == 0:
        switchModule = trackLayout.switchSequences[currentPath.trackGroup[-1]]

        # Check if we get a matching index num
        for i in range(len(switchModule)):
            # Break switch into components for index
            switchPos = switchModule[i][0]
            switchVector = switchModule[i][1]
            # Check if path & switch pos match
            if currentPath.trackIndex[-1] == switchPos:
                #   Check if we are already sequencing a switch action
                if currentPath.switchSequence == False:
                    #   Process the vector data
                    if currentPath.direction[-1] == switchVector:
                        foundVector = 1
                    elif switchVector == '*':
                        foundVector = 2
                    else:
                        foundVector = 3
                    break

    return foundVector


def GetVectorNum(currentPath):
    if currentPath.direction[-1] == "-":
        return 0
    else:
        return 1