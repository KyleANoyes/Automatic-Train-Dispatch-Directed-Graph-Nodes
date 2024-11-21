import copy

STEPS_AFTER_SWITCH = 2


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
        self.trackGroup = [
            # MainPax - 00
            [[0, 1, 2, 3, 4, 5, 6, 7], 0],
            # MainFreight - 01
            [[8, 9, 10, 11, 12, 13, 14, 15], 1],
            # Branchmain - 02
            [[20, 21, 22, 23, 24], 2],
            # InnerWest - 03
            [[26, 27, 28], 3],
            # InnerEast - 04
            [[29, 30, 31], 4],
            # Yard - 05
            [[32, 37, 33, 34, 35, 36, 25], 5],
            # Turntable - 06
            [[38, 39, 40, 41, 42], 6],
            # UpperAux - 07
            [[16, 17, 18, 19], 7],
            # BranchLower - 08
            [[43, 44, 45, 46], 8],
            # RevLoop - 09
            [[48, 49, 50], 9],
            # LowerAux - 10
            [[47], 10]
        ]

        self.switchPoints = [
            #00
            [[5, '-'], [7, '+']],
            #01
            [[0, '*'], [4, '*']],
            #02
            [[0, '-'], [2, '+'], [3, '+'], [4, '+']],
            #03
            [[2, '+']],
            #04
            [[0, '+']],
            #05
            [0, 1],
            #06
            [],
            #07
            [2],
            #08
            [4],
            #09
            [],
            #10
            []
        ]

        self.switchConnections = [
            ## -- Negative direction, positive direction
            #00
            [[[1, 4], [1, 0]], [[1, 4], [1, 0]]],
            #01a, 01b
            [[[0, 7], [2, 0], [0, 5]], [[0, 7], [2, 0], [0, 5]]],
            #02
            [[[1, 0], [7, 0], [8, 0], [5, 0], [3, 0], [5, 6]], [[1, 0], [7, 0], [8, 0], [5, 0], [3, 0], [5, 6]]],
            #03
            [[[3, 4], [4, 0]], [[3, 4], [4, 0]]],
            #04
            [[[3, 0]], [[3, 0]]],
            #05
            [[[2, 3], [2, 5]], [[2, 3], [2, 5]]],
            #06
            [[[5, 6]], [[5, 6]]],
            #07a, 07b
            [[[2, 0], [1, 4]], [[2, 0], [1, 4]]],
            #08
            [[[2, 2], [9, 0], [9, 2], [10, 0], [2, 2], [9, 0], [9, 2], [10, 0]]],
            #09
            [[[8, 3], [8, 3]], [[8, 3], [8, 3]]],
            #10
            [[[8, 3]], [[8, 3]]]
        ]

        self.trackConnections = [
            #00
            [],
            #01
            [],
            #02
            [[1, 0], [3, 0]],
            #03
            [[2, -1], [3, 0]],
            #04
            [[3, 0]],
            #05
            [],
            #06
            [],
            #07
            [],
            #08
            [],
            #09
            [],
            #10
            []
        ]

        self.trackEnd = [
            #00
            [],
            #01
            [],
            #02
            [],
            #03
            [1, 2],
            #04
            [1, 2],
            #05
            [1, 2, 3, 4, 5],
            #06
            [0, 1, 2, 3, 4],
            #07
            [0, 1, 3],
            #08
            [],
            #09
            [],
            #10
            []
        ]


class TrainPath:
    # Copy location, add direction marker, and record steps
    #   0 = Group of track
    #   1 = Index on group
    #   2 = Direction of travel
    #   3 = End of track
    #   4 = Switch Point
    #   5 = Number of Reverses
    #   6 = Switch Step Wait
    #   7 = Reverse Step Wait
    def __init__(self, direction, group, index):
        self.trackGroup = []
        self.trackIndex = []
        self.direction = []
        self.pathEnd = False
        self.switchPoint = False
        self.sumReverse = 0
        self.switchStepWait = 0
        self.ReverseStepWait = 0
        self.points = 0
        self.sumSteps = 0



trackLayout = LayoutMaster()

# Config
pointForwards = 1
pointBackwards = 5
pointReverse = 10

# State checks
isSwitch = False
allowedVector = False

# Container for the path
    # Create two list: [0] = forwards, [1] backwards
    # Count up/down the list
path = [[[]], [[]]]

# Set location and target
location = [0, 2]
target = [7, 17]

path[0][0].append(TrainPath('+', location[0], location[1]))
path[1][0].append(TrainPath('-', location[0], location[1]))

# Begin main routing
cycle = 0
while (cycle < 250):
    for directionGroup in range(len(path)):
        for subGroup in range(len(path[directionGroup])):
            print(F"{directionGroup}, {subGroup}")
            zz_directionGroup = directionGroup
            zz_subGroup = subGroup
            recordCheck = path[directionGroup][subGroup]
            # Get the current object group and position
            currentGroupNum = trackLayout.trackGroup[recordCheck.trackGroup[-1]][1]
            currentTrackPos = recordCheck.trackIndex[-1]
            direction = recordCheck.direction[-1]
            isEnd = recordCheck.pathEnd
            isSwitch = recordCheck
            countDirectionSwitch = recordCheck[5]
            stepCoolDown = recordCheck[6]
            reverseCoolDown = recordCheck[7]

            # debug point
            if stepCoolDown != 0:
                pass

            # If not end, proceed with program
            if isEnd == False:
                groupLength = len(trackLayout.trackGroup[currentGroupNum][0])
                # Get index of current position
                for posIndex in range(groupLength):
                    groupIndexPos = trackLayout.trackGroup[currentGroupNum][0][posIndex]
                    if groupIndexPos == currentTrackPos:
                        groupIndexPos = posIndex
                        break

                # ------------------------ Find and record next positon ------------------------
                # ------------------------------------------------------------------------------
                # If last was not a switch and not on cooldown
                if isSwitch == False or stepCoolDown != 0 or reverseCoolDown != 0:
                    trackGroup = trackLayout.trackGroup[currentGroupNum][0]
                    # Check if direction indicates positive
                    if direction == '+':
                        groupLength = len(trackGroup) - 1
                        # Check if end of list
                        if groupIndexPos < groupLength:
                            # If less, then incrament
                            nextGroupNum = currentGroupNum
                            nextTrackPos = trackGroup[groupIndexPos + 1]
                        else:
                            # Else, start back at front of the list
                            if len(trackLayout.trackConnections[currentGroupNum]) == 0:
                                nextGroupNum = currentGroupNum
                                nextTrackPos = trackGroup[0]
                        
                        # Add points and steps
                        pathScore[directionGroup][subGroup][0] += pointForwards
                        pathScore[directionGroup][subGroup][1] += 1
                    
                    # Check if direction indicates negative
                    else:
                        # Check if start of list
                        if groupIndexPos != 0:
                            # If so, loop to negative index
                            nextGroupNum = currentGroupNum
                            nextTrackPos = trackGroup[currentTrackPos - 1]
                        else:
                            if len(trackLayout.trackConnections[currentGroupNum]) == 0:
                                nextGroupNum = currentGroupNum
                                nextTrackPos = trackGroup[-1]

                        # Add points
                        pathScore[directionGroup][subGroup][0] += pointBackwards
                        pathScore[directionGroup][subGroup][1] += 1


                    # Decrease reverse step wait if > 0
                    if reverseCoolDown != 0:
                        reverseCoolDown = reverseCoolDown - 1
                    
                    # Decrease switch step wait if > 0
                    if stepCoolDown != 0:
                        stepCoolDown = stepCoolDown - 1
                        if stepCoolDown == 0:
                            # Reverse direction
                            if direction == '+':
                                direction = '-'
                                isSwitch = '+' + isSwitch[1]
                            else:
                                direction = '+'
                                isSwitch = '-' + isSwitch[1]

                            reverseCoolDown = STEPS_AFTER_SWITCH
                            countDirectionSwitch = countDirectionSwitch + 1


                    path[directionGroup][subGroup].append([nextGroupNum, nextTrackPos, direction, False, isSwitch, countDirectionSwitch, stepCoolDown, reverseCoolDown])

                # If last was switch with incorrect vector, process one more step and then reverse direction
                elif isSwitch[0] == '-':
                    # Check if direction indicates positive
                    if direction == '+':
                        # Check if end of list
                        if groupIndexPos < (len(trackLayout.trackGroup[currentGroupNum][0]) - 1):
                            # If less, then incrament
                            nextGroupNum = currentGroupNum
                            nextTrackPos = trackLayout.trackGroup[nextGroupNum][0][currentTrackPos + 1]
                        else:
                            if len(trackLayout.trackConnections[currentGroupNum]) == 0:
                                nextGroupNum = currentGroupNum
                                nextTrackPos = trackLayout.trackGroup[nextGroupNum][0][0]
                        
                        # Add points and steps
                        pathScore[directionGroup][subGroup][0] += pointForwards
                        pathScore[directionGroup][subGroup][1] += 1
                    
                    # Check if direction indicates negative
                    else:
                        # Check if start of list
                        if groupIndexPos != 0:
                            # If so, loop to negative index
                            nextGroupNum = currentGroupNum
                            nextTrackPos = trackLayout.trackGroup[nextGroupNum][0][currentTrackPos - 1]
                        else:
                            if len(trackLayout.trackConnections[currentGroupNum]) == 0:
                                nextGroupNum = currentGroupNum
                                nextTrackPos = trackLayout.trackGroup[nextGroupNum][0][-1]

                        # Add points
                        pathScore[directionGroup][subGroup][0] += pointBackwards
                        pathScore[directionGroup][subGroup][0] += pointReverse
                        pathScore[directionGroup][subGroup][1] += 1

                    path[directionGroup][subGroup].append([nextGroupNum, nextTrackPos, direction, False, isSwitch, countDirectionSwitch, stepCoolDown, reverseCoolDown])
                    pass

                # If last was switch with incorrect vector, process one more step and then reverse direction
                elif isSwitch[0] == '+':
                    # Reassign switch to int
                    isSwitch = int(isSwitch[1])

                    # Collect connection list
                    connectionVector = path[directionGroup][subGroup][-1][2]
                    if connectionVector == '-':
                        connectionList = trackLayout.switchConnections[path[directionGroup][subGroup][-1][5]][0]
                    else:
                        connectionList = trackLayout.switchConnections[path[directionGroup][subGroup][-1][5]][1]
                    
                    # Get connection from switch index
                    connectionIndex = connectionList[isSwitch]

                    # Begin incrament
                    nextGroupNum = connectionIndex[0]
                    nextTrackPos = trackLayout.trackGroup[connectionIndex[0]][0][connectionIndex[1]]

                    if direction == '+':
                        # Add points and steps
                        pathScore[directionGroup][subGroup][0] += pointForwards
                        pathScore[directionGroup][subGroup][1] += 1
                    
                    # Check if direction indicates negative
                    else:
                        # Add points
                        pathScore[directionGroup][subGroup][0] += pointBackwards
                        pathScore[directionGroup][subGroup][1] += 1

                    
                    path[directionGroup][subGroup].append([nextGroupNum, nextTrackPos, direction, False, isSwitch, countDirectionSwitch,  stepCoolDown, reverseCoolDown])
                    pass
                
                else:
                    print("ERROR")
                
                
                # Check if at track end      
                if len(trackLayout.trackEnd[nextGroupNum]) > 0:
                    for i in range(len(trackLayout.trackEnd[nextGroupNum])):
                        if trackLayout.trackEnd[i] == path[directionGroup][subGroup][-1][1]:
                            path[directionGroup][subGroup][-1][3] = True

            # ------------------------ Check if next point is a swtich ------------------------
            # ---------------------------------------------------------------------------------
            
            if isEnd == False:
                # Check if next point is a switch
                correctVector = 0

                # Copy over path and switch container
                pathContainer = path[directionGroup][subGroup][-1]
                switchContainer = trackLayout.switchPoints[path[directionGroup][subGroup][-1][0]]
                # Break path into components
                pathGroup = pathContainer[0]
                pathPos = pathContainer[1]
                pathVector = pathContainer[2]
                pathSwitch = pathContainer[4]
                pathStepWait = pathContainer[6]

                # If switch and not on cooldown
                if pathStepWait == 0 and pathSwitch == False:
                    # Check if we get a matching index num
                    for i in range(len(switchContainer)):
                        # Break switch into components for index
                        switchPos = switchContainer[i][0]
                        switchVector = switchContainer[i][1]
                        # Check if path & switch pos match
                        if pathPos == switchPos:
                            # Check if duplication was already performed
                            if pathSwitch == False:
                                if pathVector == switchVector or pathVector == '*':
                                    correctVector = 1
                                else:
                                    correctVector = 2
                                switchIndex = i
                                break

                # Based on vector, record state
                if correctVector == 1:
                    newListExist = True
                    # Check if operation has already been performed
                    try:
                        # If exist, terminate search on current subGroup
                        path[directionGroup][subGroup + 1]
                        path[directionGroup][subGroup][-1][3] = True
                    except:
                        newListExist = False

                    if newListExist == False:
                        # Create new subGroup list; deepcopy previous subGroup to new subGroup
                        copyPath = path[directionGroup][subGroup]
                        path[directionGroup].append([])
                        path[directionGroup][subGroup + 1] = copy.deepcopy(copyPath)

                        # Create new pathScore list; deepcopy previous pathScore to new pathScore
                        copyPathScore = pathScore[directionGroup][subGroup]
                        pathScore[directionGroup].append([])
                        pathScore[directionGroup][subGroup + 1] = copy.deepcopy(copyPathScore)

                        # Temp hold of new path
                        newPath = path[directionGroup][subGroup + 1]
                        # Flag the switch as negative int to process split
                        newPath[-1][4] = ("-" + str(switchIndex))
                        # Create step counter
                        newPath[-1][6] = STEPS_AFTER_SWITCH

                    
                if correctVector == 2:
                    newListExist = True
                    # Check if operation has already been performed
                    try:
                        # If exist, terminate search on current subGroup
                        path[directionGroup][subGroup + 1]
                        path[directionGroup][subGroup][-1][3] = True
                    except:
                        newListExist = False

                    if newListExist == False:
                        # Create new subGroup list; deepcopy previous subGroup to new subGroup
                        copyPath = path[directionGroup][subGroup]
                        path[directionGroup].append([])
                        path[directionGroup][subGroup + 1] = copy.deepcopy(copyPath)

                        # Create new pathScore list; deepcopy previous pathScore to new pathScore
                        copyPathScore = pathScore[directionGroup][subGroup]
                        pathScore[directionGroup].append([])
                        pathScore[directionGroup][subGroup + 1] = copy.deepcopy(copyPathScore)

                        # Temp hold of new path
                        newPath = path[directionGroup][subGroup + 1]
                        # Flag the switch as negative int to process split
                        newPath[-1][4] = ("-" + str(switchIndex))
                        # Create step counter
                        newPath[-1][6] = STEPS_AFTER_SWITCH

                        pass