# Current build date: Dec 24 2024

import copy

STEPS_AFTER_SWITCH = 3
COOLDOWN_REVERSE = (STEPS_AFTER_SWITCH * 2)
COOLDOWN_NORMAL = 1
SELF_LOOP_MAX = 3

class LayoutMaster():
    def __init__(self):
        self.trackName = [
            "MainPax",
            "MainFreight",
            "BranchMain",
            "InnerWest",
            "InnerEast",
            "Yard",
            "Turntable",
            "UpperAux",
            "BranchLower",
            "RevLoop",
            "LowerAux"
        ]

        # The actual int values do not matter,
        #   they are just here for better visualization
        self.trackGroupHuman = [
            # MainPax - 00
            [[0, 1, 2, 3, 4, 5, 6, 7], 0],
            # MainFreight - 01
            [[8, 9, 10, 11, 12, 13, 14, 15], 1],
            # Branchmain - 02
            [[16, 20, 21, 22, 23, 24, 26], 2],
            # InnerWest - 03
            [[27, 28], 3],
            # InnerEast - 04
            [[29, 30, 31], 4],
            # Yard - 05
            [[32, 37, 33, 34, 35, 36, 25], 5],
            # Turntable - 06
            [[38, 39, 40, 41, 42], 6],
            # UpperAux - 07
            [[17, 18, 19], 7],
            # BranchLower - 08
            [[43, 44, 45, 46], 8],
            # RevLoop - 09
            [[48, 49, 50], 9],
            # LowerAux - 10
            [[47], 10]
        ]

        self.trackGroupComp = []

        self.switchSequences = [
            #00
            [[5, '-'], [7, '+']],
            #01
            [[0, '*'], [4, '*']],
            #02
            [[1, '-'], [3, '+'], [4, '+'], [5, '+'], [6, '*']],
            #03
            [],
            #04
            [[0, '+'], [5, '-']],
            #05
            [[0, '-'], [1, '+']],
            #06
            [],
            #07
            [[1, '*']],
            #08
            [[3, '+']],
            #09
            [],
            #10
            []
        ]
            # TODO  Document this better, also further nest the list structure
            #
            #       This is the template to use:
            #       [Switch[Direction[ConnectionGroup[TrackConnection]]] = [[[[]]], [[[]]]]
            #
        self.switchConnection = [
            #00
            [[[[1, 4]]], [[[1, 0]]]],
            #01
            [[[[0, 7]], [[7, 2]]], [[[2, 0]], [[7, 0], [0, 5]]]],
            #02
            [[[[1, 0]], [[4, 0]]], [[[8, 0]], [[5, 0]], [[5, 6]], [[3, 1]]]],
            #03
            [[[]], [[]]],
            #04
            [[[]], [[[4, 2]]]],
            #05
            [[[[5, 6]]], [[[5, 1], [5, 2], [5, 3], [5, 4]]]],
            #06
            [[[]], [[]]],
            #07
            [[[[1, 4]]], [[[1, 4]]]],
            #08
            [[[[2, 3]]], [[[9, 0]]]],
            #09
            [[[]], [[]]],
            #10
            [[[]], [[]]]
        ]
        self.switchPosition = [
            #00
            [[[0, 5]], [[0, 7]]],
            #01
            [[[1, 0], [1, 4]], [[1, 0], [1, 4]]],
            #02
            [[[2, 1], [2, 6]], [[2, 3], [2, 4], [2, 5], [2, 6]]],
            #03
            [[[]], [[]]],
            #04
            [[[]], [[4, 0]]],
            #05
            [[[5, 5]], [[5, 0]]],
            #06
            [[[]], [[]]],
            #07
            [[[7, 1]], [[7, 1]]],
            #08
            [[[8, 0]], [[8, 3]]],
            #09
            [[[]], [[]]],
            #10
            [[[]], [[]]]
        ]
        self.switchInverseDir = [
            #00
            [[[]], [[[]]]],
            #01
            [[[], []], [[], []]],
            #02
            [[[], []], [[], [], [], []]],
            #03
            [[[]], [[]]],
            #04
            [[[]], [[]]],
            #05
            [[[]], [[]]],
            #06
            [[[]], [[]]],
            #07
            [[[]], [[]]],
            #08
            [[[]], [[]]],
            #09
            [[[]], [[]]],
            #10
            [[[]], [[]]]
        ]

        self.trackConnections = [
            #00
            [],
            #01
            [],
            #02
            [[], [3, 0]],
            #03
            [[2, -1], [2, -1]],
            #04
            [[], [2, -1]],
            #05
            [],
            #06
            [],
            #07
            [],
            #08
            [],
            #09
            [[8, 3], [8, 3]],
            #10
            [[8, 3], [8, 3]]
        ]

        self.trackInverseDir = [
            #00
            [],
            #01
            [],
            #02
            [[], []],
            #03
            [[], []],
            #04
            [[], []],
            #05
            [],
            #06
            [],
            #07
            [],
            #08
            [],
            #09
            [[], []],
            #10
            [[], []]
        ]

        self.trackEnd = [
            #00
            [],
            #01
            [],
            #02
            [0],
            #03
            [0, 1],
            #04
            [1, 2],
            #05
            [1, 2, 3, 4, 5],
            #06
            [0, 1, 2, 3, 4],
            #07
            [0, 2],
            #08
            [],
            #09
            [],
            #10
            []
        ]

    def CreateTrackComp(self):
        for yAxis in range(len(self.trackGroupHuman)):
            self.trackGroupComp.append([[], yAxis])
            for xAxis in range(len(self.trackGroupHuman[yAxis][0])):
                self.trackGroupComp[yAxis][0].append(xAxis)


class TrainPath:
    def __init__(self, direction, group, index):
        self.trackGroup = [group]
        self.trackIndex = [index]
        self.direction = [direction]
        self.pathEnd = False
        self.endReached = False
        self.switchSequence = False
        self.vectorAlligned = False
        self.reverseNeeded = False
        self.sumReverse = 0
        self.switchStepWait = 0
        self.cooldown = 0
        self.sumPoints = 0
        self.sumSteps = 0
        self.selfLoop = 0
        self.inverseDirection = False


def TrainPathMain():
    #   Config creation
    pointForwards = 1
    pointBackwards = 5
    pointReverse = 10
    maxCycle = 150

    #   Set location and target
    start = [0, 2]
    #   Real target
    #ziel = [7, 0]
    #   Fake target to force inifinite search
    ziel = [1, 99]

    #   Package config
    config = [pointForwards, pointBackwards, pointReverse, maxCycle]
    target = [start, ziel]

    #   Create track object
    trackLayout = LayoutMaster()
    trackLayout.CreateTrackComp()

    #   Configure vector inverse points
    ConfigTrackConnectionInverse(trackLayout)
    ConfigTrackSwitchInverse(trackLayout)


    #   Create path container and begin search
    path = [[], []]
    successfulPath = CreateTrainPath(path, trackLayout, target, config)

    pass


def IncramentStepLite(trackLayout, currentPath):
    # Check if direction indicates positive
    if currentPath.direction[-1] == '+':
        currentPath = StepForwards(trackLayout, currentPath)

    else:
        currentPath = StepBackwards(trackLayout, currentPath)

    #   Incrament direction
    currentPath.direction.append(currentPath.direction[-1])

    return currentPath


def IncramentStepFull(trackLayout, currentPath, config):
    pointForwards = config[0]
    pointBackwards = config[1]
    pointReverse = config[2]

    # Check if direction indicates positive
    if currentPath.direction[-1] == '+':
        currentPath = StepForwards(trackLayout, currentPath)

        # Add points and steps
        currentPath.sumPoints += pointForwards
        currentPath.sumSteps += 1
    else:
        currentPath = StepBackwards(trackLayout, currentPath)

        #   Add points
        currentPath.sumPoints += pointBackwards
        currentPath.sumSteps += 1

    #   Incrament direction
    currentPath.direction.append(currentPath.direction[-1])

    return currentPath


def StepForwards(trackLayout, currentPath):
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
            currentPath.trackGroup.append(connection[0])
            currentPath.trackIndex.append(connection[1])

    return currentPath


def StepBackwards(trackLayout, currentPath):
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
            currentPath.trackGroup.append(connection[0])
            currentPath.trackIndex.append(connection[1])

    return currentPath


def IncramentStepSwitch(path, currentPath, trackLayout, directionGroup):
    #   First get the switch group container
    if currentPath.direction[-1] == '+':
        switchConnection = trackLayout.switchConnection[currentPath.trackGroup[-1]][1]
        switchPosition = trackLayout.switchPosition[currentPath.trackGroup[-1]][1]
        switchInverseList = trackLayout.switchInverseDir[currentPath.trackGroup[-1]][1]
        initialDirection = '+'
    else:
        switchConnection = trackLayout.switchConnection[currentPath.trackGroup[-1]][0]
        switchPosition = trackLayout.switchPosition[currentPath.trackGroup[-1]][0]
        switchInverseList = trackLayout.switchInverseDir[currentPath.trackGroup[-1]][0]
        initialDirection = '-'


    switchThrowList = "Ooga booga grug mad"

    for i in range(len(switchPosition)):
        pathPos = [currentPath.trackGroup[-1], currentPath.trackIndex[-1]]
        
        if switchPosition[i] == pathPos:
            switchThrowList = switchConnection[i]
            switchInverseList = switchInverseList[i]
            break

    #   If we hit this, This means that we tried calling the switch function when we were 
    #       not at a switch. This makes grug unhappy
    if switchThrowList == "Ooga booga grug mad":
        pass

    #   TODO:   We need to add some flags to stop the children from being allowed to reverse
    #               immediately after completing a switch motion
    #
    #           This is due to an improper counting system where we use '+' and '-'.
    #               The logic is fine, but we need to inverse the direction when using
    #               a switch that is in a differnt list polarity               

    #   Now that we have the container, begin the pathing
    for switchThrow in range(len(switchThrowList)):
        basePath = copy.deepcopy(currentPath)
        
        if switchThrow == 0:
            #   Step forward
            currentPath.trackGroup.append(switchThrowList[switchThrow][0])
            currentPath.trackIndex.append(switchThrowList[switchThrow][1])
                
            #   Reset switchSequence
            currentPath.switchSequence = False

            #   Add direction
            currentPath.direction.append(initialDirection)

        else:
            #   Spawn a new child path
            SpawnPathCopy(path, directionGroup, basePath)

            #   Step forward with the new child
            path[directionGroup][-1].trackGroup.append(switchThrowList[switchThrow][0])
            path[directionGroup][-1].trackIndex.append(switchThrowList[switchThrow][1])

            # Reset switchSequence
            path[directionGroup][-1].switchSequence = False

            #   Add direction
            path[directionGroup][-1].direction.append(initialDirection)
        
        #   Inverse direction if needed
        #   This function is not ready yet
        #if switchInverseList[switchThrow][0] == True:
            #currentPath = InverseDirection(path[directionGroup][-1])

    return currentPath


def SpawnPathCopy(path, directionGroup, currentPath):
    path[directionGroup].append([])
    path[directionGroup][-1] = copy.deepcopy(currentPath)


def SpawnIndependantChild(correctVector, path, directionGroup, currentPath):
    #   Based on vector, record state
    if correctVector == 1 or correctVector == 2:
        # Create new subGroup list; deepcopy previous subGroup to new subGroup
        SpawnPathCopy(path, directionGroup, currentPath)

        # Switch and direction vectors are alligned, flag as positive
        path[directionGroup][-1].vectorAlligned = True
        path[directionGroup][-1].switchSequence = True

        
    if correctVector == 3 or correctVector == 2:
        #   Create new subGroup list; deepcopy previous subGroup to new subGroup
        SpawnPathCopy(path, directionGroup, currentPath)

        #   Switch and direction vectors are NOT alligned, flag as negative for reverse action processing
        path[directionGroup][-1].vectorAlligned = False
        path[directionGroup][-1].switchSequence = True
        path[directionGroup][-1].switchStepWait = STEPS_AFTER_SWITCH
        path[directionGroup][-1].cooldown = COOLDOWN_REVERSE
        path[directionGroup][-1].reverseNeeded = True


def SwapDirection(currentPath):
    if currentPath.direction[-1] == '+':
        currentPath.direction[-1] = '-'
    else:
        currentPath.direction[-1] = '+'
    
    return currentPath


def CheckSwitch(currentPath, trackLayout):
    # ------------------------ Check if next point is a swtich ------------------------
    # ---------------------------------------------------------------------------------
    
    if currentPath.pathEnd == False:
        # Check if next point is a switch
        correctVector = 0

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
                            correctVector = 1
                        elif switchVector == '*':
                            correctVector = 2
                        else:
                            correctVector = 3
                        break
    
    return correctVector


def CheckTrackEndLite(trackLayout, path, currentPath, directionGroup, subGroup):
    if len(trackLayout.trackEnd[currentPath.trackGroup[-1]]) > 0:
        trackEndPoints = trackLayout.trackEnd[currentPath.trackGroup[-1]]
        for i in range(len(trackEndPoints)):
            if trackEndPoints[i] == currentPath.trackIndex[-1]:
                path[directionGroup][subGroup].pathEnd = True


def ConfigTrackConnectionInverse(trackLayout):
    #   TODO: Need to fix this critical component. The functionality is there for
    #           creating steps, but now we need to use the found data correctly.
    #           This is really really good though, we are on the cusp of an
    #           having an insanely robust and modular tool for all JMRI 
    #           panels!!!



    #   Extract the needed data from the object for simplicity
    #   Agent container
    agent = [[], []]

    for yAxis in range(len(trackLayout.trackConnections)):
        if len(trackLayout.trackConnections[yAxis]) != 0:
            debug = trackLayout.trackConnections[yAxis]

            #   Create agents and initialize two starts to each end of track
            agent[0] = TrainPath('-', yAxis, trackLayout.trackGroupComp[yAxis][0][0])
            agent[1] = TrainPath('+', yAxis, trackLayout.trackGroupComp[yAxis][0][-1])

            #   Gather negative connection data if applicable
            if len(trackLayout.trackConnections[yAxis][0]) != 0:
                for i in range(2):
                    agent[0] = IncramentStepLite(trackLayout, agent[0])

                #   Critical debug point - need to check if data here makes sense before passing into my else-if
                debugA0 = agent[0].trackGroup[0]
                debugA1 = agent[0].trackGroup[2]
                debugA2 = agent[0].trackIndex[0]
                debugA3 = agent[0].trackIndex[2]

                #   Check if the track connection step resulted in an auto reverse
                if debugA0 == debugA1:
                    if debugA2 == debugA3:
                        pass

            #   Gather positive connection data if applicable
            if len(trackLayout.trackConnections[yAxis][1]) != 0:
                for i in range(2):
                    agent[1] = IncramentStepLite(trackLayout, agent[1])

                #   Critical debug point - need to check if data here makes sense before passing into my else-if
                debugB0 = agent[1].trackGroup[0]
                debugB1 = agent[1].trackGroup[2]
                debugB2 = agent[1].trackIndex[0]
                debugB3 = agent[1].trackIndex[2]

                #   Check if the track connection step resulted in an auto reverse
                if debugB0 == debugB1:
                    if debugB2 == debugB3:
                        pass


def ConfigTrackSwitchInverse(trackLayout):
    #   TODO: We can touch this function once the above one is working as expected
    #           Both share the same common logic, but this one is going to do a bit
    #           more nesting of the axis'
    #
    #           Welp, the above is now done! Now we need to fight the mess of using
    #           the same logic with nested switches. This is gonna be a bloddy mess
    pass


def InverseDirection(currentPath):
    if currentPath.direction[-1] == "-":
        currentPath.direction[-1] = "+"
    else:
        currentPath.direction[-1] = "-"
    
    return currentPath


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
                CheckTrackEndLite(trackLayout, path, currentPath, directionGroup, subGroup)

                #   If not end, proceed with program
                if currentPath.pathEnd == False:
                    # ------------------------ Find and record next positon ------------------------
                    # ------------------------------------------------------------------------------
                    #   If last step was not a switch and path not on a cooldown
                    if currentPath.switchSequence == False:
                        currentPath = IncramentStepFull(trackLayout, currentPath, config)

                    # ------------------ Find and record next positon from switch ------------------
                    # ------------------------------------------------------------------------------
                    
                    elif currentPath.vectorAlligned == True:
                        currentPath = IncramentStepSwitch(path, currentPath, trackLayout, directionGroup)

                    # ----------------- Process forward movement before reversing ------------------
                    # ------------------------------------------------------------------------------
                    elif currentPath.vectorAlligned == False:
                        currentPath = IncramentStepFull(trackLayout, currentPath, config)

                        #   Adjust switch step wait
                        if currentPath.switchStepWait == 0 and currentPath.reverseNeeded == True:
                            #   Flip direction then flag reverse needed as false
                            currentPath = SwapDirection(currentPath)

                            currentPath.reverseNeeded = False

                        elif currentPath.switchStepWait > 0:
                            currentPath.switchStepWait = currentPath.switchStepWait - 1
                        
                        #   Adjust cooldown, but if it's zero, allow new switch catch
                        if currentPath.cooldown > 0:
                            currentPath.cooldown = currentPath.cooldown - 1
                        else:
                            # Add incramnet here so that we aren't behind the choo choo. Kinda odd, but it works
                            currentPath = IncramentStepFull(trackLayout, currentPath, config)
                            currentPath.vectorAlligned = True
                        
                        pass
                    else:
                        print("ERROR: Impossible state reached")

                    #   Check if current position is on a switch
                    correctVector = CheckSwitch(currentPath, trackLayout)

                    #   This creates a more serious new spawn compared to the other spawn
                    SpawnIndependantChild(correctVector, path, directionGroup, currentPath)

    return successfulPath


TrainPathMain()