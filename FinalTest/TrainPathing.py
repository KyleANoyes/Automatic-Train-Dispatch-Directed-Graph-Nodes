#   Import full supporting scripts
import Globals
import StepHandler
import GeneralAction
import DataCheck

#   Import specific parts of modules
from ClassContainer import TrainPath

#   Import Python modules
import copy

# --------------------------------------- #


def TrainPathMain(trackLayout):
    #   Config creation
    pointForwards = 1
    pointBackwards = 5
    pointReverse = 10
    maxCycle = 150

    #   Set location and target
    start = [9, 1]
    #   Real target
    ziel = [0, 0]
    #   Fake target to force inifinite search
    #ziel = [1, 99]

    #   Package config
    config = [pointForwards, pointBackwards, pointReverse, maxCycle]
    target = [start, ziel]

    #   Create path container and begin search
    path = [[], []]
    successfulPath = CreateTrainPath(path, trackLayout, target, config)

    pass


def CreateTrainPath(path, trackLayout, target, config):
    #   Counters / config
    cycle = 0
    cylceMax = config[3]
    stopSerch = False
    searchSucces = False

    #   Initiate start and end point
    start = target[0]
    ziel = target[1]

    #   Create path objects and initialize two starts
    path[0].append(TrainPath('+', start[0], start[1]))
    path[1].append(TrainPath('-', start[0], start[1]))

    #   Container for successful paths
    successfulPath = []

    while (stopSerch != True):
        cycle += 1

        #   Break from while 
        for directionGroup in range(len(path)):
            if stopSerch == True:
                stopSerch = True
                searchSucces = True
                break

            if cycle == cylceMax:
                stopSerch = True
                searchSucces = False
                break

            for subGroup in range(len(path[directionGroup])):
                currentPath = path[directionGroup][subGroup]
                print(F"{directionGroup}, {subGroup} -- trackGroup = {currentPath.trackGroup[-1]}, trackIndex = {currentPath.trackIndex[-1]}")

                #   Check if the goal was reached
                if currentPath.trackGroup[-1] == ziel[0] and currentPath.trackIndex[-1] == ziel[1]:
                    #   Record successfuly path
                    successfulPath.append(copy.deepcopy(currentPath))

                    stopSerch = True
                    break
                
                if directionGroup == 0 and subGroup == 23:
                    pass
                #   Check if we are at an end point
                DataCheck.CheckTrackEndLite(trackLayout, path, currentPath, directionGroup, subGroup)

                #   If not end, proceed with program
                if currentPath.pathEnd == False:
                    # ------------------------ Find and record next positon ------------------------
                    # ------------------------------------------------------------------------------
                    #   If last step was not a switch and path not on a cooldown
                    if currentPath.switchSequence == False:
                        currentPath = StepHandler.IncramentStepFull(trackLayout, currentPath, config)

                    # ------------------ Find and record next positon from switch ------------------
                    # ------------------------------------------------------------------------------
                    
                    elif currentPath.vectorAlligned == True:
                        StepHandler.IncramentStepSwitch(path, currentPath, trackLayout, directionGroup)

                    # ----------------- Process forward movement before reversing ------------------
                    # ------------------------------------------------------------------------------
                    elif currentPath.vectorAlligned == False:
                        currentPath = StepHandler.IncramentStepFull(trackLayout, currentPath, config)

                        #   Adjust switch step wait
                        if currentPath.switchStepWait == 0 and currentPath.reverseNeeded == True:
                            #   Flip direction then flag reverse needed as false
                            currentPath = GeneralAction.InverseDirection(currentPath)

                            currentPath.reverseNeeded = False

                        elif currentPath.switchStepWait > 0:
                            currentPath.switchStepWait = currentPath.switchStepWait - 1
                        
                        #   Adjust cooldown, but if it's zero, allow new switch catch
                        if currentPath.cooldown > 0:
                            currentPath.cooldown = currentPath.cooldown - 1
                        else:
                            # Add incramnet here so that we aren't behind the choo choo. Kinda odd, but it works
                            currentPath = StepHandler.IncramentStepFull(trackLayout, currentPath, config)
                            currentPath.vectorAlligned = True
                        
                        pass
                    else:
                        print("ERROR: Impossible state reached")

                    #   Check if current position is on a switch
                    correctVector = DataCheck.CheckSwitch(currentPath, trackLayout)

                    #   This creates a more serious new spawn compared to the other spawn
                    StepHandler.SpawnPathCopyFull(correctVector, path, directionGroup, currentPath)

    return successfulPath