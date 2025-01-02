#   Import universal scripts
import Globals
import MessageContainer

#   Import full supporting scripts
import DataCollect

#   Import partial supporting scripts

#   Import Python modules

# --------------------------------------- #


def ValidRangeInt(numTest, num0, num1, inclusive):
    if inclusive == True:
        if numTest >= num0 and numTest <= num1:
            return True
        else:
            return False
    else:
        if numTest > num0 and numTest < num1:
            return True
        else:
            return False
        


def CheckSelfRevolvingInverse(agent):
    inversePoint = [[], []]
    inverseNeeded = False

    for parentAgent in range(len(agent[0])):
        agent0 = agent[0][parentAgent]

        continueSearch = DataCollect.ListLenAboveMin(agent0.trackGroup, 3)

        if continueSearch == True:
            startPos0 = [agent0.trackGroup[0], agent0.trackIndex[0]]
            endPos0 = [agent0.trackGroup[2], agent0.trackIndex[2]]

            if startPos0 == endPos0:
                for childAgent in range(len(agent[1])):
                    agent1 = agent[1][childAgent]


                    if continueSearch == True:
                        startPos1 = [agent1.trackGroup[0], agent0.trackIndex[0]]
                        endPos1 = [agent1.trackGroup[2], agent0.trackIndex[2]]


                        if startPos0 == startPos1 and endPos0 == endPos1:
                            inverseNeeded = True
                            inversePoint[0].append(parentAgent)
                            break


    for parentAgent in range(len(agent[1])):
        agent0 = agent[1][parentAgent]

        continueSearch = DataCollect.ListLenAboveMin(agent0.trackGroup, 3)

        if continueSearch == True:
            startPos0 = [agent0.trackGroup[0], agent0.trackIndex[0]]
            endPos0 = [agent0.trackGroup[2], agent0.trackIndex[2]]

            if startPos0 == endPos0:
                for childAgent in range(len(agent[0])):
                    agent1 = agent[0][childAgent]

                    if continueSearch == True:
                        startPos1 = [agent1.trackGroup[0], agent0.trackIndex[0]]
                        endPos1 = [agent1.trackGroup[2], agent0.trackIndex[2]]

                        if startPos0 == startPos1 and endPos0 == endPos1:
                            inverseNeeded = True
                            inversePoint[1].append(parentAgent)
                            break


    return inverseNeeded, inversePoint