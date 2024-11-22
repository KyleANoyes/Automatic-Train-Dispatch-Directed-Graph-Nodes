# Current build date: Nov 21 2024

# TODO: Figure out why we can break out of the group 1 loop. It has something to do with vector using the * sign

import copy

STEPS_AFTER_SWITCH = 3
COOLDOWN_REVERSE = (STEPS_AFTER_SWITCH * 2)
COOLDOWN_NORMAL = 1
SELF_LOOP_MAX = 4

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

        self.trackGroupComp = []

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

    def CreateTrackComp(self):
        for yAxis in range(len(self.trackGroupHuman)):
            self.trackGroupComp.append([[], yAxis])
            for xAxis in range(len(self.trackGroupHuman[yAxis][0])):
                self.trackGroupComp[yAxis][0].append(xAxis)


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
        self.trackGroup = [group]
        self.trackIndex = [index]
        self.direction = [direction]
        self.pathEnd = [False]
        self.endReached = [False]
        self.switchPoint = [False]
        self.sumReverse = 0
        self.switchStepWait = 0
        self.cooldown = 0
        self.sumPoints = 0
        self.sumSteps = 0
        self.selfLoop = 0



# Config
pointForwards = 1
pointBackwards = 5
pointReverse = 10

# Container for the path
    # Create two list: [0] = forwards, [1] backwards
    # Count up/down the list
path = [[], []]

# Set location and target
location = [0, 2]
target = [7, 17]

#   Create track object, then translate human list into computer friendly list
trackLayout = LayoutMaster()
trackLayout.CreateTrackComp()

#   Create path objects and initialize two starts
path[0].append(TrainPath('+', location[0], location[1]))
path[1].append(TrainPath('-', location[0], location[1]))

# Begin main routing
cycle = 0
while (cycle < 250):
    for directionGroup in range(len(path)):
        for subGroup in range(len(path[directionGroup])):
            print(F"{directionGroup}, {subGroup}")
            zz_directionGroup = directionGroup
            zz_subGroup = subGroup
            
            #   Pass object members to local variables, process the changes needed
            #   and then save members back to the object. This will make it much
            #   easier to debug as well, and decrease the spaghetti
            currentGroupNum = trackLayout.trackGroupComp[path[directionGroup][subGroup].trackGroup[-1]][1]
            currentTrackPos = path[directionGroup][subGroup].trackIndex[-1]
            direction = path[directionGroup][subGroup].direction[-1]
            pathEnd = path[directionGroup][subGroup].pathEnd[-1]
            endReached = path[directionGroup][subGroup].endReached[-1]
            sumPoints = path[directionGroup][subGroup].sumPoints
            sumReverse = path[directionGroup][subGroup].sumReverse
            sumSteps = path[directionGroup][subGroup].sumSteps
            switchPoint = path[directionGroup][subGroup].switchPoint[-1]
            switchStepWait = path[directionGroup][subGroup].switchStepWait
            cooldown = path[directionGroup][subGroup].cooldown

            # debug point
            if zz_directionGroup == 0 and zz_subGroup == 1:
                print(F"Current group: {currentGroupNum}\nCurrent Pos: {currentTrackPos}")
                pass

            # If not end, proceed with program
            if pathEnd == False:
                groupLength = len(trackLayout.trackGroupComp[currentGroupNum][0])
                # Get index of current position
                for posIndex in range(groupLength):
                    groupIndexPos = trackLayout.trackGroupComp[currentGroupNum][0][posIndex]
                    if groupIndexPos == currentTrackPos:
                        groupIndexPos = posIndex
                        break

                # ------------------------ Find and record next positon ------------------------
                # ------------------------------------------------------------------------------
                # If last step was not a switch and path not on a cooldown
                if switchPoint == False and switchStepWait == 0:
                    trackGroup = trackLayout.trackGroupComp[currentGroupNum][0]
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
                        sumPoints += pointForwards
                        sumSteps += 1
                    
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
                        sumPoints += pointBackwards
                        sumSteps += 1

                # If last was switch with incorrect vector, process step cool down and then reverse direction
                elif switchPoint[0] == '-' or cooldown != 0:
                    # Check if direction indicates positive
                    if direction == '+':
                        # Check if end of list
                        if groupIndexPos < groupLength - 1:
                            # If less, then incrament
                            nextGroupNum = currentGroupNum
                            nextTrackPos = trackGroup[groupIndexPos + 1]
                        else:
                            # Else, start back at front of the list
                            if len(trackLayout.trackConnections[currentGroupNum]) == 0:
                                nextGroupNum = currentGroupNum
                                nextTrackPos = trackGroup[0]
                        
                        # Add points and steps
                        sumPoints += pointForwards
                        sumSteps += 1
                    
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
                        sumPoints += pointBackwards
                        sumPoints += pointReverse
                        sumSteps += 1

                    switchStepWait = switchStepWait - 1

                    if switchStepWait == 0:
                        if switchPoint[0] == '-':
                            switchPoint = "+" + switchPoint[1]
                        else:
                            switchPoint = '-' + switchPoint[1]

                        if direction == '+':
                            direction = '-'
                        else:
                            direction = '+'

                # If last was switch with incorrect vector, process one more step and then reverse direction
                elif switchPoint[0] == '+' and cooldown == 0:
                    # Reassign switch to int
                    switchPoint = int(switchPoint[1])

                    # Collect connection list
                    connectionVector = path[directionGroup][subGroup].direction[-1]
                    if connectionVector == '-':
                        connectionList = trackLayout.switchConnections[path[directionGroup][subGroup].trackGroup[-1]][0]
                    else:
                        connectionList = trackLayout.switchConnections[path[directionGroup][subGroup].trackGroup[-1]][1]
                    
                    # Get connection from switch index
                    connectionIndex = connectionList[switchPoint]

                    # Begin incrament
                    nextGroupNum = connectionIndex[0]
                    nextTrackPos = trackLayout.trackGroupComp[connectionIndex[0]][0][connectionIndex[1]]

                    if direction == '+':
                        # Add points and steps
                        sumPoints += pointForwards
                        sumSteps += 1
                    
                    # Check if direction indicates negative
                    else:
                        # Add points
                        sumPoints += pointBackwards
                        sumSteps += 1
                    
                    #   Reset vars used in flags to determine if a switch take / reverse is allowed
                    switchPoint = False
                    switchStepWait = 0
                    cooldown = COOLDOWN_NORMAL
                
                #   Decrease cooldown if needed
                if cooldown > 0:
                    cooldown = cooldown - 1

                # --------------------------------------- #
                #   Enter the data back into the host object
                path[directionGroup][subGroup].trackGroup.append(nextGroupNum)
                path[directionGroup][subGroup].trackIndex.append(nextTrackPos)
                path[directionGroup][subGroup].direction.append(direction)
                path[directionGroup][subGroup].pathEnd.append(False)
                path[directionGroup][subGroup].endReached.append(False)
                path[directionGroup][subGroup].sumPoints = sumPoints
                path[directionGroup][subGroup].sumReverse = sumReverse
                path[directionGroup][subGroup].sumSteps = sumSteps
                path[directionGroup][subGroup].switchPoint.append(switchPoint)
                path[directionGroup][subGroup].switchStepWait = switchStepWait
                path[directionGroup][subGroup].cooldown = cooldown


                #   Check if at track end      
                if len(trackLayout.trackEnd[nextGroupNum]) > 0:
                    for i in range(len(trackLayout.trackEnd[nextGroupNum])):
                        if trackLayout.trackEnd[i] == path[directionGroup][subGroup][-1][1]:
                            path[directionGroup][subGroup][-1][3] = True

                #   Check if we self looped over the max allowed
                for yAxis in range(len(path[directionGroup][subGroup].trackGroup)):
                    groupNum = path[directionGroup][subGroup].trackGroup[yAxis]
                    indexNum = path[directionGroup][subGroup].trackIndex[yAxis]
                    selfLoop = 0
                    for xAxis in range(len(path[directionGroup][subGroup].trackGroup)):
                        if groupNum == path[directionGroup][subGroup].trackGroup[xAxis] and indexNum == path[directionGroup][subGroup].trackIndex[xAxis]:
                            selfLoop += 1
                        if selfLoop == SELF_LOOP_MAX:
                            path[directionGroup][subGroup].pathEnd[-1] = True
                            break
                    if selfLoop == SELF_LOOP_MAX:
                        break

            # ------------------------ Check if next point is a swtich ------------------------
            # ---------------------------------------------------------------------------------

            currentGroupNum = trackLayout.trackGroupComp[path[directionGroup][subGroup].trackGroup[-1]][1]
            currentTrackPos = path[directionGroup][subGroup].trackIndex[-1]
            direction = path[directionGroup][subGroup].direction[-1]
            pathEnd = path[directionGroup][subGroup].pathEnd[-1]
            endReached = path[directionGroup][subGroup].endReached[-1]
            sumPoints = path[directionGroup][subGroup].sumPoints
            sumReverse = path[directionGroup][subGroup].sumReverse
            sumSteps = path[directionGroup][subGroup].sumSteps
            switchPoint = path[directionGroup][subGroup].switchPoint[-1]
            switchStepWait = path[directionGroup][subGroup].switchStepWait
            cooldown = path[directionGroup][subGroup].cooldown
            
            if pathEnd == False:
                # Check if next point is a switch
                correctVector = 0

                # Copy over path and switch container
                pathContainer = currentGroupNum
                switchContainer = trackLayout.switchPoints[currentGroupNum]

                # If switch and not on cooldown
                if switchStepWait == 0 and switchPoint == False and cooldown == 0:
                    # Check if we get a matching index num
                    for i in range(len(switchContainer)):
                        # Break switch into components for index
                        switchPos = switchContainer[i][0]
                        switchVector = switchContainer[i][1]
                        # Check if path & switch pos match
                        if currentTrackPos == switchPos:
                            # Check if duplication was already performed
                            if switchPoint == False:
                                if direction == switchVector:
                                    correctVector = 1
                                elif switchVector == '*':
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
                        #   If we can find a list length, then we know it exist. 
                        #   This is crude, but it does indeed work :)
                        if (len(path[directionGroup][subGroup + 1].direction) > 0):
                            newListExist = True
                    except:
                        newListExist = False

                    if newListExist == False:
                        # Create new subGroup list; deepcopy previous subGroup to new subGroup
                        path[directionGroup].append([])
                        path[directionGroup][subGroup + 1] = copy.deepcopy(path[directionGroup][subGroup])

                        # Switch and direction vectors are alligned, flag as positive
                        path[directionGroup][subGroup + 1].switchPoint.append("+" + str(switchIndex))
                        # Set wait steps
                        path[directionGroup][subGroup + 1].switchStepWait = STEPS_AFTER_SWITCH

                    
                if correctVector == 2:
                    newListExist = True
                    # Check if operation has already been performed
                    try:
                        #   If we can find a list length, then we know it exist. 
                        #   This is crude, but it does indeed work :)
                        if (len(path[directionGroup][subGroup + 1].direction) > 0):
                            newListExist = True
                    except:
                        newListExist = False

                    if newListExist == False:
                        # Create new subGroup list; deepcopy previous subGroup to new subGroup
                        path[directionGroup].append([])
                        path[directionGroup][subGroup + 1] = copy.deepcopy(path[directionGroup][subGroup])

                        # Switch and direction vectors are NOT alligned, flag as negative for reverse action processing
                        path[directionGroup][subGroup + 1].switchPoint.append("-" + str(switchIndex))
                        # Set wait steps
                        path[directionGroup][subGroup + 1].switchStepWait = STEPS_AFTER_SWITCH
                        path[directionGroup][subGroup + 1].cooldown = COOLDOWN_REVERSE