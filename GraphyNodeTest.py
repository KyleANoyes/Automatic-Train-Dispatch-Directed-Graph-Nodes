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

        self.switchSequences = [
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
            [[1, 4], [1, 0]], [[1, 4], [1, 0]],
            #01a, 01b
            [[0, 7], [2, 0], [0, 5]], [[0, 7], [2, 0], [0, 5]],
            #02
            [[1, 0], [7, 0], [8, 0], [5, 0], [3, 0], [5, 6]], [[1, 0], [7, 0], [8, 0], [5, 0], [3, 0], [5, 6]],
            #03
            [[3, 4], [4, 0]], [[3, 4], [4, 0]],
            #04
            [[3, 0]], [[3, 0]],
            #05
            [[2, 3], [2, 5]], [[2, 3], [2, 5]],
            #06
            [[5, 6]], [[5, 6]],
            #07a, 07b
            [[2, 0], [1, 4]], [[2, 0], [1, 4]],
            #08
            [[2, 2], [9, 0], [9, 2], [10, 0], [2, 2], [9, 0], [9, 2], [10, 0]],
            #09
            [[8, 3], [8, 3]], [[8, 3], [8, 3]],
            #10
            [[8, 3]], [[8, 3]]
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



def IncramentStep(trackLayout, currentPath):
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

        # Add points
        currentPath.sumPoints += pointBackwards
        currentPath.sumSteps += 1

    # Incrament direction
    currentPath.direction.append(currentPath.direction[-1])

    return currentPath



# Begin main routing
cycle = 0
while (cycle < 250):
    for directionGroup in range(len(path)):
        for subGroup in range(len(path[directionGroup])):
            print(F"{directionGroup}, {subGroup}")
            zz_directionGroup = directionGroup
            zz_subGroup = subGroup

            currentPath = path[directionGroup][subGroup]

            # debug point
            if zz_subGroup == 1:
                print(F"Current group: {currentPath.trackGroup[-1]}\nCurrent Pos: {currentPath.trackIndex[-1]}")
                pass

            # If not end, proceed with program
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
                # If last step was not a switch and path not on a cooldown
                if currentPath.switchSequence == False:
                    currentPath = IncramentStep(trackLayout, currentPath)

                # ------------------------- Record next step if switch -------------------------
                # ------------------------------------------------------------------------------
                elif currentPath.vectorAlligned == True:
                    # 
                    if currentPath.direction[-1] == '+':
                        currentPath.trackGroup.append(trackLayout.switchConnections[currentPath.trackGroup[-1]][1][0])
                        currentPath.trackIndex.append(trackLayout.switchConnections[currentPath.trackGroup[-1]][1][1])
                        
                    else:
                        currentPath.trackGroup.append(trackLayout.switchConnections[currentPath.trackGroup[-1]][0][0])
                        currentPath.trackIndex.append(trackLayout.switchConnections[currentPath.trackGroup[-1]][0][1])

                    # Incrament direction
                    currentPath.direction.append(currentPath.direction[-1])
                    
                    # Reset switchSequence
                    currentPath.switchSequence = False

                # ----------------- Process forward movement before reversing ------------------
                # ------------------------------------------------------------------------------
                elif currentPath.vectorAlligned == False:
                    currentPath = IncramentStep(trackLayout, currentPath)

                    # Adjust switch step wait
                    if currentPath.switchStepWait > 0 and currentPath.reverseNeeded == True:
                        # Flip direction then flag reverse needed as false
                        if currentPath.direction[-1] == '+':
                            currentPath.direction[-1] = '-'
                        else:
                            currentPath.direction[-1] = '+'
                        
                        currentPath.reverseNeeded = False
                        currentPath.switchStepWait = currentPath.switchStepWait - 1
                    
                    # Adjust cooldown, but if it's zero, allow new switch catch
                    if currentPath.cooldown > 0:
                        currentPath.cooldown = currentPath.cooldown - 1
                    else:
                        currentPath.switchSequence = False
                        currentPath.vectorAlligned = True
                    
                    pass


                else:
                    print("ERROR: Impossible state reached")


                #   Check if at track end      
                if len(trackLayout.trackEnd[currentPath.trackGroup[-1]]) > 0:
                    for i in range(len(trackLayout.trackEnd[currentPath.trackGroup[-1]])):
                        if trackLayout.trackEnd[i] == path[directionGroup][subGroup][-1][1]:
                            path[directionGroup][subGroup][-1][3] = True


            # ------------------------ Check if next point is a swtich ------------------------
            # ---------------------------------------------------------------------------------
            
            if currentPath.pathEnd == False:
                # Check if next point is a switch
                correctVector = 0

                # If switch and not on cooldown
                if currentPath.switchStepWait == 0 and currentPath.switchSequence == False and currentPath.cooldown == 0:
                    # Check if we get a matching index num
                    for i in range(len(trackLayout.switchSequences[currentPath.trackGroup[-1]])):
                        # Break switch into components for index
                        switchPos = trackLayout.switchSequences[currentPath.trackGroup[-1]][i][0]
                        switchVector = trackLayout.switchSequences[currentPath.trackGroup[-1]][i][1]
                        # Check if path & switch pos match
                        if currentPath.trackIndex[-1] == switchPos:
                            #   Check if we are already sequencing a switch action
                            if currentPath.switchSequence == False:
                                if currentPath.direction[-1] == switchVector:
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
                        path[directionGroup][subGroup + 1] = copy.deepcopy(currentPath)

                        # Switch and direction vectors are alligned, flag as positive
                        path[directionGroup][subGroup + 1].vectorAlligned = True
                        path[directionGroup][subGroup + 1].switchSequence = True
                    
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
                        path[directionGroup][subGroup + 1] = copy.deepcopy(currentPath)

                        # Switch and direction vectors are NOT alligned, flag as negative for reverse action processing
                        path[directionGroup][subGroup + 1].vectorAlligned = False
                        path[directionGroup][subGroup + 1].switchSequence = True
                        path[directionGroup][subGroup + 1].switchStepWait = STEPS_AFTER_SWITCH
                        path[directionGroup][subGroup + 1].cooldown = COOLDOWN_REVERSE
                        path[directionGroup][subGroup + 1].reverseNeeded = True