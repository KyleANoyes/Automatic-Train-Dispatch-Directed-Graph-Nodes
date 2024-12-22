# Current build date: Dec 19 2024

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
            [[1, '-'], [2, '+'], [3, '+'], [4, '+'], [5, '*']],
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
            #       The list has way too many nested components, it should
            #           probably be broken up into one for positive and
            #           nagative vectors, but leaving it for now as a low
            #           priority item
            ## -- Negative direction, positive direction
            #
            # This is the template to use [Switch[Direction[ConnectionGroup[TrackConnection]]] = [[[[]]], [[[]]]]
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


def TrainPathMain():
    # Config
    # pointForwards = 1
    # pointBackwards = 5
    # pointReverse = 10
    # maxCycle

    config = [1, 5, 10, 150]

    # Container for the path
        # Create two list: [0] = forwards, [1] backwards
        # Count up/down the list
    path = [[], []]

    # Set location and target
    start = [0, 2]
    #ziel = [7, 1]
    ziel = [1, 99]

    target = [start, ziel]

    #   Create track object, then translate human list into computer friendly list
    trackLayout = LayoutMaster()
    trackLayout.CreateTrackComp()

    successfulPath = CreateTrainPath(path, trackLayout, target, config)

    pass


def IncramentStep(trackLayout, currentPath, config, groupIndexPos):
    pointForwards = config[0]
    pointBackwards = config[1]
    pointReverse = config[2]

    trackGroup = trackLayout.trackGroupComp[currentPath.trackGroup[-1]][0]
    # Check if direction indicates positive
    if currentPath.direction[-1] == '+':
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
                pass
        
        # Add points and steps
        currentPath.sumPoints += pointForwards
        currentPath.sumSteps += 1
    
    # Check if direction indicates negative
    else:
        # Check if start of list
        if groupIndexPos != 0:
            # If so, loop to negative index
            currentPath.trackGroup.append(currentPath.trackGroup[-1])
            currentPath.trackIndex.append(trackGroup[currentPath.trackIndex[-1] - 1])
        else:
            if len(trackLayout.trackConnections[currentPath.trackGroup[-1]]) == 0:
                currentPath.trackGroup.append(currentPath.trackGroup[-1])
                currentPath.trackIndex.append(trackGroup[-1])
            else:
                pass

        # Add points
        currentPath.sumPoints += pointBackwards
        currentPath.sumSteps += 1

    # Incrament direction
    currentPath.direction.append(currentPath.direction[-1])

    return currentPath



def IncramentStepSwitch(path, currentPath, trackLayout, directionGroup):
    #   IMPORTANT: Use currentPath.trackGroup[-2] after incramenting the group for index
    #       This is critical as it maintains the path line prior to the switch
    #
    # TODO: Add a for loop to incrament through the last list index so we can implament
    #           infanite throw switches. Critical for 3-way and greater.
    #
    #           Arguable if this should even be allowed behavior, but I guess design
    #           against it for wider compatability

    #   First get the switch group container
    if currentPath.direction[-1] == '+':
        switchConnection = trackLayout.switchConnection[currentPath.trackGroup[-1]][1]
        switchPosition = trackLayout.switchPosition[currentPath.trackGroup[-1]][1]
    else:
        switchConnection = trackLayout.switchConnection[currentPath.trackGroup[-1]][0]
        switchPosition = trackLayout.switchPosition[currentPath.trackGroup[-1]][0]


    for i in range(len(switchPosition)):
        pathPos = [currentPath.trackGroup[-1], currentPath.trackIndex[-1]]
        
        if switchPosition[i] == pathPos:
            switchThrow = switchPosition[i]
            break

    #   TODO: We now know what throws we can use, time to act on it :D

    #   Now that we have the container, begin the pathing
    for switchThrow in range(len(switchPosition)):
        basePath = copy.deepcopy(currentPath)
        
        if switchThrow == 0:
            currentPath.trackGroup.append(switchThrow[switchThrow][0])
            currentPath.trackIndex.append(switchThrow[switchThrow][1])
                
            # Reset switchSequence
            currentPath.switchSequence = False

        else:
            SpawnPathCopy(path, directionGroup, basePath)
            path[directionGroup][-1].trackGroup.append(switchThrow[switchThrow][0])
            path[directionGroup][-1].trackIndex.append(switchThrow[switchThrow][1])

            # Reset switchSequence
            path[directionGroup][-1].switchSequence = False


    return currentPath



def SpawnPathCopy(path, directionGroup, currentPath):
    path[directionGroup].append([])
    path[directionGroup][-1] = copy.deepcopy(currentPath)


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

                #   If not end, proceed with program
                if currentPath.pathEnd == False:
                    groupLength = len(trackLayout.trackGroupComp[currentPath.trackGroup[-1]][0])
                    # Get index of current position
                    for posIndex in range(groupLength):
                        groupIndexPos = trackLayout.trackGroupComp[currentPath.trackGroup[-1]][0][posIndex]
                        if groupIndexPos == currentPath.trackIndex[-1]:
                            groupIndexPos = posIndex
                            break

                    # ------------------------ Find and record next positon ------------------------
                    # ------------------------------------------------------------------------------
                    #   If last step was not a switch and path not on a cooldown
                    if currentPath.switchSequence == False:
                        currentPath = IncramentStep(trackLayout, currentPath, config, groupIndexPos)

                    # ------------------ Find and record next positon from switch ------------------
                    # ------------------------------------------------------------------------------
                    
                    elif currentPath.vectorAlligned == True:
                        currentPath = IncramentStepSwitch(path, currentPath, trackLayout, directionGroup)

                    # ----------------- Process forward movement before reversing ------------------
                    # ------------------------------------------------------------------------------
                    elif currentPath.vectorAlligned == False:
                        currentPath = IncramentStep(trackLayout, currentPath, config, groupIndexPos)

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
                            currentPath = IncramentStep(trackLayout, currentPath, config, groupIndexPos)
                            currentPath.vectorAlligned = True
                        
                        pass
                    else:
                        print("ERROR: Impossible state reached")

                    #   Check if at track end      
                    if len(trackLayout.trackEnd[currentPath.trackGroup[-1]]) > 0:
                        for i in range(len(trackLayout.trackEnd[currentPath.trackGroup[-1]])):
                            if trackLayout.trackEnd[i] == currentPath.trackIndex:
                                path[directionGroup][subGroup][-1][3] = True


                    #   Check if current position is on a switch
                    correctVector = CheckSwitch(currentPath, trackLayout)

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

    return successfulPath


TrainPathMain()