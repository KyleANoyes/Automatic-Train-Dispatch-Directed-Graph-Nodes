#   Import universal scripts
import Globals
import MessageContainer

#   Import full supporting scripts
import GeneralAction
import DataCollect
import GeneralAction

#   Import partial supporting scripts

#   Import Python modules
import copy

# --------------------------------------- #


def IncramentStepLite(trackLayout, currentPath, initMode=False):
    # Check if direction indicates positive
    if currentPath.direction[-1] == '+':
        currentPath = StepForwards(trackLayout, currentPath, initMode)

    else:
        currentPath = StepBackwards(trackLayout, currentPath, initMode)

    #   Incrament direction
    currentPath.direction.append(currentPath.direction[-1])

    return currentPath


def IncramentStepFull(trackLayout, currentPath, config, initMode=False):
    pointForwards = config[0]
    pointBackwards = config[1]
    pointReverse = config[2]

    # Check if direction indicates positive
    if currentPath.direction[-1] == '+':
        currentPath = StepForwards(trackLayout, currentPath, initMode)

        # Add points and steps
        currentPath.sumPoints += pointForwards
        currentPath.sumSteps += 1
    else:
        currentPath = StepBackwards(trackLayout, currentPath, initMode)

        #   Add points
        currentPath.sumPoints += pointBackwards
        currentPath.sumSteps += 1

    #   Incrament direction
    currentPath.direction.append(currentPath.direction[-1])

    if currentPath.inverseDirection == True:
        GeneralAction.InverseDirection(currentPath)
        currentPath.inverseDirection = False

    return currentPath


def StepForwards(trackLayout, currentPath, initMode):
    trackGroup = trackLayout.trackGroupComp[currentPath.trackGroup[-1]][0]
    groupLength = len(trackGroup) - 1
    # Check if end of list
    if currentPath.trackIndex[-1] < groupLength:
        # If less, then incrament
        currentPath.trackGroup.append(currentPath.trackGroup[-1])
        currentPath.trackIndex.append(trackGroup[currentPath.trackIndex[-1] + 1])
    else:
        # Else, start back at front of the list
        if len(trackLayout.trackConnections[currentPath.trackGroup[-1]]) == 0:
            currentPath.trackGroup.append(currentPath.trackGroup[-1])
            currentPath.trackIndex.append(trackGroup[0])
        else:
            connection = trackLayout.trackConnections[currentPath.trackGroup[-1]][1]
            baseGroup = trackLayout.trackGroupComp[connection[0]][0]
            currentPath.trackGroup.append(connection[0])
            currentPath.trackIndex.append(baseGroup[connection[1]])

            if initMode == False:
                CheckInverseNeed(currentPath, trackLayout)

    return currentPath


def StepBackwards(trackLayout, currentPath, initMode):
    trackGroup = trackLayout.trackGroupComp[currentPath.trackGroup[-1]][0]
    #   Check if start of list
    if currentPath.trackIndex[-1] != 0:
        #   If so, loop to negative index
        currentPath.trackGroup.append(currentPath.trackGroup[-1])
        currentPath.trackIndex.append(trackGroup[currentPath.trackIndex[-1] - 1])
    else:
        if len(trackLayout.trackConnections[currentPath.trackGroup[-1]]) == 0:
            currentPath.trackGroup.append(currentPath.trackGroup[-1])
            currentPath.trackIndex.append(trackGroup[-1])
        else:
            connection = trackLayout.trackConnections[currentPath.trackGroup[-1]][0]
            baseGroup = trackLayout.trackGroupComp[connection[0]][0]
            currentPath.trackGroup.append(connection[0])
            currentPath.trackIndex.append(baseGroup[connection[1]])

            if initMode == False:
                CheckInverseNeed(currentPath, trackLayout)

    return currentPath


def CheckInverseNeed(currentPath, trackLayout):
    priorStepGroup = currentPath.trackGroup[-2]
    vectorNum = DataCollect.GetVectorNum(currentPath)

    if trackLayout.trackInverseDir[priorStepGroup][vectorNum] == True:
        currentPath.inverseDirection = True


def IncramentStepSwitch(path, currentPath, trackLayout, directionGroup, initMode=False):
    #   First get the switch group container identifier
    if currentPath.direction[-1] == '+':
        indexSearch = 1
        initialDirection = '+'
    else:
        indexSearch = 0
        initialDirection = '-'

    #   Call specified container from direction
    switchConnection = trackLayout.switchConnection[currentPath.trackGroup[-1]][indexSearch]
    switchPosition = trackLayout.switchPosition[currentPath.trackGroup[-1]][indexSearch]
    switchInverseList = trackLayout.switchInverseDir[currentPath.trackGroup[-1]][indexSearch]

    #   Funny debug flag; make grug happy not mad - https://grugbrain.dev/
    grugHappy = False

    for i in range(len(switchPosition)):
        pathPos = [currentPath.trackGroup[-1], currentPath.trackIndex[-1]]
        
        if switchPosition[i] == pathPos:
            switchThrowList = switchConnection[i]
            switchInverseList = switchInverseList[i]
            grugHappy = True
            break

    #   If we hit this, This means that we tried calling the switch function when we were 
    #       not at a switch. This makes grug unhappy
    if grugHappy == False:
        MessageContainer.ErrorMsg(0)

    # Log a common base point for all future child spawns
    basePath = copy.deepcopy(currentPath)

    for switchThrow in range(len(switchThrowList)):
        if switchThrow == 0:
            #   Step forward
            currentPath.trackGroup.append(switchThrowList[switchThrow][0])
            currentPath.trackIndex.append(switchThrowList[switchThrow][1])
                
            #   Reset switchSequence
            currentPath.switchSequence = False

            #   Add direction
            currentPath.direction.append(initialDirection)
            
            #   Check if inverse is needed
            if initMode == False:
                CheckInverseNeed(currentPath, trackLayout)
                
                if currentPath.inverseDirection == True:
                    GeneralAction.InverseDirection(currentPath)

        else:
            #   Spawn a new child path
            SpawnPathCopyLite(path, directionGroup, basePath)

            #   Step forward with the new child
            path[directionGroup][-1].trackGroup.append(switchThrowList[switchThrow][0])
            path[directionGroup][-1].trackIndex.append(switchThrowList[switchThrow][1])

            # Reset switchSequence
            path[directionGroup][-1].switchSequence = False

            #   Add direction
            path[directionGroup][-1].direction.append(initialDirection)
        
            #   Check if inverse is needed
            if initMode == False:
                CheckInverseNeed(path[directionGroup][-1], trackLayout)
                
                if path[directionGroup][-1].inverseDirection == True:
                    GeneralAction.InverseDirection(path[directionGroup][-1])


def SpawnPathCopyLite(path, directionGroup, currentPath):
    path[directionGroup].append([])
    path[directionGroup][-1] = copy.deepcopy(currentPath)


def SpawnPathCopyFull(correctVector, path, directionGroup, currentPath):
    #   Based on vector, record state
    if correctVector == 1 or correctVector == 2:
        # Create new subGroup list; deepcopy previous subGroup to new subGroup
        SpawnPathCopyLite(path, directionGroup, currentPath)

        # Switch and direction vectors are alligned, flag as positive
        path[directionGroup][-1].vectorAlligned = True
        path[directionGroup][-1].switchSequence = True

        
    if correctVector == 3 or correctVector == 2:
        #   Create new subGroup list; deepcopy previous subGroup to new subGroup
        SpawnPathCopyLite(path, directionGroup, currentPath)

        #   Switch and direction vectors are NOT alligned, flag as negative for reverse action processing
        path[directionGroup][-1].vectorAlligned = False
        path[directionGroup][-1].switchSequence = True
        path[directionGroup][-1].switchStepWait = Globals.STEPS_AFTER_SWITCH
        path[directionGroup][-1].cooldown = Globals.COOLDOWN_REVERSE
        path[directionGroup][-1].reverseNeeded = True


def SwapLastDirection(currentPath):
    if currentPath.direction[-1] == '+':
        currentPath.direction[-1] = '-'
    else:
        currentPath.direction[-1] = '+'
    
    return currentPath