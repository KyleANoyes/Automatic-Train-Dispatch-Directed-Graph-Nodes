#   Import universal scripts
import Globals
import MessageContainer

#   Import full supporting scripts
import StepHandler
import DataCheck
import uuid

#   Import partial supporting scripts
from ClassContainer import TrainPath

#   Import Python modules
import copy

# --------------------------------------- #


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
        if Globals.DEBUG_LITE == True:
            MessageContainer.DebugMsg(0, yAxis)

        #   Agent container / reset point
        agent = [[], []]

        if len(trackLayout.trackConnections[yAxis]) != 0:
            #   Create agents and initialize two starts to each end of track
            agent[0].append(TrainPath('-', yAxis, trackLayout.trackGroupComp[yAxis][0][0]))
            agent[1].append(TrainPath('+', yAxis, trackLayout.trackGroupComp[yAxis][0][-1]))

            #   Gather negative connection data if applicable
            if len(trackLayout.trackConnections[yAxis][0]) != 0:
                agent[0][0] = StepHandler.IncramentStepLite(trackLayout, agent[0][0], True)

                #   Check if the step was at a switch
                switchCheck = DataCheck.CheckSwitch(agent[0][0], trackLayout)

                if switchCheck == 0 or switchCheck == 3:
                    #   Normal step incrament
                    agent[0][0] = StepHandler.IncramentStepLite(trackLayout, agent[0][0], True)
                    
                else:
                    #   Call the step incrament function, only one cycle is needed
                    StepHandler.IncramentStepSwitch(agent, agent[0][0], trackLayout, 0, True)
                    
                inverseFlag = CheckInitPositionOverlapFull(agent[0])
                
                trackLayout.trackInverseDir[yAxis][0] = inverseFlag

            #   Gather positive connection data if applicable
            if len(trackLayout.trackConnections[yAxis][1]) != 0:
                inverseFlag = False

                agent[1][0] = StepHandler.IncramentStepLite(trackLayout, agent[1][0], True)

                #   Check if the step was at a switch
                switchCheck = DataCheck.CheckSwitch(agent[1][0], trackLayout)

                #   Incrament appropriate step
                if switchCheck == 0 or switchCheck == 3:
                    #   Normal step incrament
                    agent[1][0] = StepHandler.IncramentStepLite(trackLayout, agent[1][0], True)
                else:
                    #   Call the step incrament function, only one cycle is needed
                    StepHandler.IncramentStepSwitch(agent, agent[1][0], trackLayout, 1, True)

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

        validationAgent = [[], []]

        #   Test negative switches first
        for xAxis in range(len(switchListNeg)):
            dirIndex = 0

            validationAgent[0].append(ConfigTrackSwitchTester(trackLayout, yAxis, xAxis, dirIndex))

        #   Test positive switches next
        for xAxis in range(len(switchListPos)):
            dirIndex = 1

            validationAgent[1].append(ConfigTrackSwitchTester(trackLayout, yAxis, xAxis, dirIndex))

        if Globals.DEBUG_LITE == True:
            MessageContainer.DebugMsg(4, yAxis, trackLayout.switchConnection[yAxis], trackLayout.switchInverseDir[yAxis])

        #   TODO: Need to get this self revolving checker working, but it's not critical yet
        #DataValidate.CheckSelfRevolvingInverse(validationAgent)


def ConfigTrackSwitchTester(trackLayout, yAxis, xAxis, dirIndex):
    if Globals.DEBUG_LITE == True:
        MessageContainer.DebugMsg(1, yAxis, xAxis, dirIndex)

    if dirIndex == 0:
        vector = "-"
    else:
        vector = "+"

    inverseFlag = False

    #   Container for tests done below
    agent = [[], []]

    try:
        trackLayout.switchPosition[yAxis][dirIndex][xAxis][0]
        trackLayout.switchPosition[yAxis][dirIndex][xAxis][1]
        runState = 0
    except:
        runState = 1

    if runState == 0:
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
            StepHandler.IncramentStepSwitch(agent, agent[dirIndex][0], trackLayout, dirIndex, True)

            #   Check if the step was at a switch
            for switchCopy in range(len(agent[dirIndex])):
                switchCheck = DataCheck.CheckSwitch(agent[dirIndex][switchCopy], trackLayout)

                if switchCheck == 0 or switchCheck == 3:
                    #   Normal step incrament
                    try:
                        StepHandler.IncramentStepLite(trackLayout, agent[dirIndex][switchCopy], True)

                    #   If the incrament fails, assume we have a bound limit. This should
                    #       be replaced at some point with a more thorough end-of-line check
                    #   TODO: Replace with check for end of line instead of defaulting to -1
                    except:
                        agent[dirIndex][switchCopy].trackGroup.append(-1)
                        agent[dirIndex][switchCopy].trackIndex.append(-1)
                    
                else:
                    #   Call the step incrament function, only one cycle is needed
                    StepHandler.IncramentStepSwitch(agent, agent[dirIndex][switchCopy], trackLayout, dirIndex, True)
                
                #   Get the invrse flag result, but check each 
                inverseFlag = CheckInitPositionOverlapLite(agent[dirIndex][switchCopy])

                #   Record the inverse flag at the same depth that the SwitchDepth will use
                trackLayout.switchInverseDir[yAxis][dirIndex][xAxis][switchCopy].append(inverseFlag)
        
        return agent[dirIndex]


def CheckStartingStep(trackLayout, path):
    #   Positive check
    try:
        tempPath = copy.deepcopy(path[0][0])
        StepHandler.IncramentStepLite(trackLayout, tempPath)
    except:
        #   If we fail to move forward, then assume we are at a true end
        path[0][0].endSearch = True
        path[0][0].pathEnd = True

    #   Negative check
    try:
        tempPath = copy.deepcopy(path[1][0])
        StepHandler.IncramentStepLite(trackLayout, tempPath)
    except:
        #   If we fail to move forward, then assume we are at a true end
        path[1][0].endSearch = True
        path[1][0].pathEnd = True


def GenerateNewID(pathChild):
    while True:
        testID = str(uuid.uuid4())
        if testID not in Globals.UUID_ASSIGNED:
            Globals.UUID_ASSIGNED.append(testID)
            pathChild.uniqueID = testID
            break