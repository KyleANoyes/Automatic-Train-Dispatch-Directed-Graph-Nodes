# Current build date: Dec 29 2024

#   Used for spawning new paths
import copy
#   Used for string parsing and vchar removal.
#       Required: pip install regex
import regex as re
#   Converts a literal string list representation back into mutable list
import ast
#   Convert to JSON for debugging
import json


DEBUG_FULL = False
DEBUG_LITE = True
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
            [[0, '+']],
            #05
            [[0, '+'], [5, '+']],
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
            #       [Switch=Single[Direction=2x[ConnectionGroup=1x[TrackConnection=INFx]]] = [[[[]]], [[[]]]]
            #
        self.switchConnection = [
            #00
            [[[[1, 4]]], [[[1, 0]]]],
            #01
            [[[[0, 7]], [[7, 1]]], [[[2, 0]], [[7, 1], [0, 5]]]],
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
            [[[]], [[[9, 0], [9, 2]]]],
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
            [[], [[8, 3]]],
            #09
            [[[]], [[]]],
            #10
            [[[]], [[]]]
        ]
        self.switchInverseDir = []

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
            [[2, -1], []],
            #05
            [],
            #06
            [],
            #07
            [],
            #08
            [[2, 3], []],
            #09
            [[8, 3], [8, 3]],
            #10
            [[8, 3], [8, 3]]
        ]

        self.trackInverseDir = []

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
    

    def DuplicateListStructure(self, sourceList):
        purgedList = copy.deepcopy(sourceList)

        purgedList = self.PurgeAllListData(purgedList)

        return purgedList

        
    #   This is a really dangerous and badly written function reliant on whacky
    #       regex statements. This absolutely needs to be changed asap, but it 
    #       works so we are going to quietly ignore it for now in favor of
    #       completing this project... this is going to haunt my dreams later
    def PurgeAllListData(self, listPurge):
        strList = str(listPurge)

        #   Regex remove every alphanumeric charactes
        try:
            strList = re.sub(r'\w', '', strList)
        except:
            pass

        #   Regex destroy any spaces that may exist
        try:
            strList = re.sub(' ', '', strList)
        except:
            pass

        #   Regex destroy any negative, plus, or wildcard signs still alive
        try:
            strList = re.sub('-', '', strList)
        except:
            pass
        try:
            strList = re.sub('+', '', strList)
        except:
            pass
        try:
            strList = re.sub('*', '', strList)
        except:
            pass

        #   Regex destroy any commas that may exist within brackets
        try:
            strList = re.sub(r'\[,\]', '[]', strList)
        except:
            pass

        #   All expected data I can think of has been destroyed, all that
        #       is left to do now is convert this string literal back into
        #       a Python list and hope we have not made God cry
        listPurge = ast.literal_eval(strList)

        return listPurge
    

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


def TrackController():
    #   Create track object and begin transforming list into a native enviornment
    trackLayout = LayoutMaster()
    trackLayout.CreateTrackComp()
    trackLayout.trackInverseDir = trackLayout.DuplicateListStructure(trackLayout.trackConnections)
    trackLayout.switchInverseDir = trackLayout.DuplicateListStructure(trackLayout.switchConnection)

    if DEBUG_FULL == True:
        json_str = json.dumps(trackLayout.switchConnection)

        with open('ZZ_DEBUG_SwitchConnection.json', 'w') as f:
            json.dump(json_str, f)

        f.close()

    #   Configure vector inverse points
    ConfigTrackConnectionInverse(trackLayout)
    ConfigSwitchConnectionInverse(trackLayout)

    #   Call Pathing Agent Creator
    TrainPathMain(trackLayout)


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
        InverseDirection(currentPath)
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
    vectorNum = GetVectorNum(currentPath)

    if trackLayout.trackInverseDir[priorStepGroup][vectorNum] == True:
        currentPath.inverseDirection = True


def GetVectorNum(currentPath):
    if currentPath.direction[-1] == "-":
        return 0
    else:
        return 1


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
        print("grug find Shaman or grug find Complexity. This make grug unhappy >:(")
        print("Grug now yell at big brain programmer use smol brain")
        pass

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
                    InverseDirection(currentPath)

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
                    InverseDirection(path[directionGroup][-1])


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
        path[directionGroup][-1].switchStepWait = STEPS_AFTER_SWITCH
        path[directionGroup][-1].cooldown = COOLDOWN_REVERSE
        path[directionGroup][-1].reverseNeeded = True


def SwapLastDirection(currentPath):
    if currentPath.direction[-1] == '+':
        currentPath.direction[-1] = '-'
    else:
        currentPath.direction[-1] = '+'
    
    return currentPath


def CheckTrackEndLite(trackLayout, path, currentPath, directionGroup, subGroup):
    if len(trackLayout.trackEnd[currentPath.trackGroup[-1]]) > 0:
        trackEndPoints = trackLayout.trackEnd[currentPath.trackGroup[-1]]
        for i in range(len(trackEndPoints)):
            if trackEndPoints[i] == currentPath.trackIndex[-1]:
                path[directionGroup][subGroup].pathEnd = True


def CheckSwitch(currentPath, trackLayout):    
    if currentPath.pathEnd == False:
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


def CheckInitPositionOverlapFull(agent):
    inverseFlag = False

    #   Check if any of our incramented steps repeat the original step
    for i in range(len(agent)):
        agentPosG0 = agent[0].trackGroup[0]
        agentPosI0 = agent[0].trackIndex[0]
        agentPosG1 = agent[i].trackGroup[2]
        agentPosI1 = agent[i].trackIndex[2]

        #   Check if we have a matching position, if we do, then we read
        #       over ourselves and know an inverse is required
        if agentPosG0 == agentPosG1:
            if agentPosI0 == agentPosI1:
                inverseFlag = True
                break
    
    return inverseFlag


def CheckInitPositionOverlapLite(agent):
    inverseFlag = False

    #   Check if any of our incramented steps repeat the original step
    agentPosG0 = agent.trackGroup[0]
    agentPosI0 = agent.trackIndex[0]
    agentPosG1 = agent.trackGroup[2]
    agentPosI1 = agent.trackIndex[2]

    #   Check if we have a matching position, if we do, then we read
    #       over ourselves and know an inverse is required
    if agentPosG0 == agentPosG1:
        if agentPosI0 == agentPosI1:
            inverseFlag = True
    
    return inverseFlag


def ConfigTrackConnectionInverse(trackLayout):
    for yAxis in range(len(trackLayout.trackConnections)):
        if DEBUG_LITE == True:
            print(F"ConfigTrackConnectionInverse yAxis = {yAxis}")

        #   Agent container / reset point
        agent = [[], []]

        if len(trackLayout.trackConnections[yAxis]) != 0:
            #   Create agents and initialize two starts to each end of track
            agent[0].append(TrainPath('-', yAxis, trackLayout.trackGroupComp[yAxis][0][0]))
            agent[1].append(TrainPath('+', yAxis, trackLayout.trackGroupComp[yAxis][0][-1]))

            #   Gather negative connection data if applicable
            if len(trackLayout.trackConnections[yAxis][0]) != 0:
                agent[0][0] = IncramentStepLite(trackLayout, agent[0][0], True)

                #   Check if the step was at a switch
                switchCheck = CheckSwitch(agent[0][0], trackLayout)

                if switchCheck == 0 or switchCheck == 3:
                    #   Normal step incrament
                    agent[0][0] = IncramentStepLite(trackLayout, agent[0][0], True)
                    
                else:
                    #   Call the step incrament function, only one cycle is needed
                    IncramentStepSwitch(agent, agent[0][0], trackLayout, 0, True)
                    
                inverseFlag = CheckInitPositionOverlapFull(agent[0])
                
                trackLayout.trackInverseDir[yAxis][0] = inverseFlag

            #   Gather positive connection data if applicable
            if len(trackLayout.trackConnections[yAxis][1]) != 0:
                inverseFlag = False

                agent[1][0] = IncramentStepLite(trackLayout, agent[1][0], True)

                #   Check if the step was at a switch
                switchCheck = CheckSwitch(agent[1][0], trackLayout)

                #   Incrament appropriate step
                if switchCheck == 0 or switchCheck == 3:
                    #   Normal step incrament
                    agent[1][0] = IncramentStepLite(trackLayout, agent[1][0], True)
                else:
                    #   Call the step incrament function, only one cycle is needed
                    IncramentStepSwitch(agent, agent[1][0], trackLayout, 1, True)

                inverseFlag = CheckInitPositionOverlapFull(agent[1])

                trackLayout.trackInverseDir[yAxis][1] = inverseFlag
        else:
            trackLayout.trackInverseDir[yAxis].append(False)
            trackLayout.trackInverseDir[yAxis].append(False)


def ConfigSwitchConnectionInverse(trackLayout):
    for yAxis in range(len(trackLayout.switchPosition)):
        #   Split list into positive and negative base
        switchListNeg = trackLayout.switchPosition[yAxis][0]
        switchListPos = trackLayout.switchPosition[yAxis][1]

        #   Test negative switches first
        for xAxis in range(len(switchListNeg)):
            dirIndex = 0

            ConfigTrackSwitchTester(trackLayout, yAxis, xAxis, dirIndex)

        #   Test positive switches next
        for xAxis in range(len(switchListPos)):
            dirIndex = 1

            ConfigTrackSwitchTester(trackLayout, yAxis, xAxis, dirIndex)

    
    pass


def ConfigTrackSwitchTester(trackLayout, yAxis, xAxis, dirIndex):
    if DEBUG_LITE == True:
        print(F"ConfigTrackSwitchInverse yAxis = {yAxis}, xAxis = {xAxis}, dirVector = {dirIndex}")

    if dirIndex == 0:
        vector = "-"
    else:
        vector = "+"

    inverseFlag = False

    try:
        trackLayout.switchPosition[yAxis][dirIndex][xAxis][0]
        trackLayout.switchPosition[yAxis][dirIndex][xAxis][1]
        runState = 0
    except:
        runState = 1

    if runState == 0:
        #   Agent container. Even though this doesn't actually need both of the lists, other
        #       functions called do require it so we are just going to mimick it rather
        #       then do a major overhaul that honestly won't result in anything better
        agent = [[], []]

        #   Since the rest of this program uses nested track paths, we are going to do the same.
        #       Functionally this makes no difference
        agent[dirIndex].append(TrainPath(vector, trackLayout.switchPosition[yAxis][dirIndex][xAxis][0], trackLayout.switchPosition[yAxis][dirIndex][xAxis][1]))

        #   Gather switch position and check if it's in our vector list
        switchPosition = trackLayout.switchPosition[agent[dirIndex][0].trackGroup[-1]][dirIndex]
        grugCheck = [agent[dirIndex][0].trackGroup[0], agent[dirIndex][0].trackIndex[0]]

        grugHappy = False

        for i in range(len(switchPosition)):
            if grugCheck == switchPosition[i]:
                grugHappy = True
                break

        if grugHappy == True:
            #   Step through the switch
            IncramentStepSwitch(agent, agent[dirIndex][0], trackLayout, dirIndex, True)

            #   Check if the step was at a switch
            for switchCopy in range(len(agent[dirIndex])):
                switchCheck = CheckSwitch(agent[dirIndex][switchCopy], trackLayout)

                if switchCheck == 0 or switchCheck == 3:
                    #   Normal step incrament
                    try:
                        IncramentStepLite(trackLayout, agent[dirIndex][switchCopy], True)

                    #   If the incrament fails, assume we have a bound limit. This should
                    #       be replaced at some point with a more thorough end-of-line check
                    #   TODO: Replace with check for end of line instead of defaulting to -1
                    except:
                        agent[dirIndex][switchCopy].trackGroup.append(-1)
                        agent[dirIndex][switchCopy].trackIndex.append(-1)
                    
                else:
                    #   Call the step incrament function, only one cycle is needed
                    IncramentStepSwitch(agent, agent[dirIndex][switchCopy], trackLayout, dirIndex, True)
                
                #   Get the invrse flag result, but check each 
                inverseFlag = CheckInitPositionOverlapLite(agent[dirIndex][switchCopy])

                #   Record the inverse flag at the same depth that the SwitchDepth will use
                trackLayout.switchInverseDir[yAxis][dirIndex][xAxis][switchCopy].append(inverseFlag)


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
                        IncramentStepSwitch(path, currentPath, trackLayout, directionGroup)

                    # ----------------- Process forward movement before reversing ------------------
                    # ------------------------------------------------------------------------------
                    elif currentPath.vectorAlligned == False:
                        currentPath = IncramentStepFull(trackLayout, currentPath, config)

                        #   Adjust switch step wait
                        if currentPath.switchStepWait == 0 and currentPath.reverseNeeded == True:
                            #   Flip direction then flag reverse needed as false
                            currentPath = InverseDirection(currentPath)

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
                    SpawnPathCopyFull(correctVector, path, directionGroup, currentPath)

    return successfulPath


TrackController()