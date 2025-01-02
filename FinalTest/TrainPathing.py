#   Import universal scripts
import Globals
import MessageContainer

#   Import full supporting scripts
import StepHandler
import GeneralAction
import DataCheck
import DataInit

#   Import partial supporting scripts
from ClassContainer import TrainPath

#   Import Python modules
import copy

# --------------------------------------- #


def TrainPathMain(trackLayout, start, end):
    #   Config creation
    pointForwards = 1
    pointBackwards = 5
    pointReverse = 10
    maxCycle = 150

    #   Package config
    config = [pointForwards, pointBackwards, pointReverse, maxCycle]
    target = [start, end]

    #   Create path container and begin search
    path = [[], []]
    successfulPath = CreateTrainPath(path, trackLayout, target, config)

    return successfulPath


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

    #   Assigne unique ID to paths
    DataInit.GenerateNewID(path[0][0])
    DataInit.GenerateNewID(path[1][0])

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
                MessageContainer.DebugMsg(2, directionGroup, subGroup, currentPath.trackGroup[-1], currentPath.trackIndex[-1])

                #   Check if the goal was reached
                if currentPath.trackGroup[-1] == ziel[0] and currentPath.trackIndex[-1] == ziel[1]:
                    #   Record successfuly path
                    currentPath.targetReached == True
                    currentPath.endSearch == True
                    successfulPath.append(copy.deepcopy(currentPath))

                    stopSerch = True
                    break
                
                #   Check if we are at an end point
                DataCheck.CheckTrackEndLite(trackLayout, path, currentPath, directionGroup, subGroup)

                #   If we are starting a search at the end, lets try to force a step
                if currentPath.pathEnd == True and len(currentPath.trackGroup) == 1 and currentPath.endSearch == False:
                    #   Check if our path can incrament at all
                    DataInit.CheckStartingStep(trackLayout, path)
                    
                    #   If an incramnet was able to be made, flag the pathEnd as False.
                    #       This will allow a step to proceed even at the end of a track
                    if currentPath.pathEnd == True and len(currentPath.trackGroup) == 1 and currentPath.endSearch == False:
                        currentPath.pathEnd = False

                #   If not end, proceed with program
                if currentPath.pathEnd == False:
                    StepSearchForwards(trackLayout, path, currentPath, config, directionGroup, subGroup)

                    #   Check if current position is on a switch
                    correctVector = DataCheck.CheckSwitch(currentPath, trackLayout)

                    #   This creates a more serious new spawn compared to the other spawn
                    StepHandler.SpawnPathCopyFull(correctVector, path, directionGroup, currentPath)

    return successfulPath


def StepSearchForwards(trackLayout, path, currentPath, config, directionGroup, subGroup):
    # ------------------------ Find and record next positon ------------------------
    # ------------------------------------------------------------------------------
    #   If last step was not a switch and path not on a cooldown
    if currentPath.switchSequence == False:
        try:
            currentPath = StepHandler.IncramentStepFull(trackLayout, currentPath, config)
        except:
            MessageContainer.ErrorMsg(4, directionGroup, subGroup, currentPath.uniqueID)

    # ------------------ Find and record next positon from switch ------------------
    # ------------------------------------------------------------------------------
    
    elif currentPath.vectorAlligned == True:
        try:
            StepHandler.IncramentStepSwitch(path, currentPath, trackLayout, directionGroup)
        except:
            #   TODO: Figure out what is causing this exception. It's rare, but there is
            #           logic fault somewhere related to vector alligned == False reverse
            MessageContainer.ErrorMsg(5, directionGroup, subGroup, currentPath.uniqueID)

    # ----------------- Process forward movement before reversing ------------------
    # ------------------------------------------------------------------------------
    elif currentPath.vectorAlligned == False:
        currentPath = StepHandler.IncramentStepFull(trackLayout, currentPath, config)

        #   Adjust switch step wait
        if currentPath.switchStepWait == 0 and currentPath.reverseNeeded == True:
            #   Flip direction then flag reverse needed as false
            try:
                currentPath = GeneralAction.InverseDirection(currentPath)
                currentPath.reverseNeeded = False
            except:
                MessageContainer.ErrorMsg(6, directionGroup, subGroup, currentPath.uniqueID)

        elif currentPath.switchStepWait > 0:
            currentPath.switchStepWait = currentPath.switchStepWait - 1
        
        #   Adjust cooldown, but if it's zero, allow new switch catch
        if currentPath.cooldown > 0:
            currentPath.cooldown = currentPath.cooldown - 1
        else:
            # Add incramnet here so that we aren't behind the choo choo. Kinda odd, but it works
            try:
                currentPath = StepHandler.IncramentStepFull(trackLayout, currentPath, config)
                currentPath.vectorAlligned = True
            except:
                MessageContainer.ErrorMsg(4, directionGroup, subGroup, currentPath.uniqueID)
    else:
        MessageContainer.ErrorMsg(1)