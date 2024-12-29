#   Import universal scripts
import Globals
import MessageContainer

#   Import full supporting scripts
import ClassContainer
import DataInit
import TrainPathing
import UserInput
import DataValidate

#   Import partial supporting scripts

#   Import Python modules
import json

# --------------------------------------- #


DEMO_MODE = True


def TrackController():
    #   Create track object and begin transforming list into a native enviornment
    trackLayout = ClassContainer.LayoutMaster()
    trackLayout.CreateTrackComp()
    trackLayout.trackInverseDir = trackLayout.DuplicateListStructure(trackLayout.trackConnections)
    trackLayout.switchInverseDir = trackLayout.DuplicateListStructure(trackLayout.switchConnection)

    if Globals.DEBUG_FULL == True:
        json_str = json.dumps(trackLayout.switchConnection)

        with open('ZZ_DEBUG_SwitchConnection.json', 'w') as f:
            json.dump(json_str, f)

        f.close()

    #   Configure vector inverse points
    DataInit.ConfigTrackConnectionInverse(trackLayout)
    DataInit.ConfigSwitchConnectionInverse(trackLayout)

    if DEMO_MODE == True:
        coolDemo(trackLayout)
    
    else:
        #   Call Pathing Agent Creator and define goals
        start = [0, 2]
        end = [9, 1]
        path = TrainPathing.TrainPathMain(trackLayout, start, end)

    pass


def coolDemo(trackLayout):
    MessageContainer.ProgramInfo(0)

    MessageContainer.UserMsg(0)

    while(True):
        while True:
            MessageContainer.UserMsg(1)
            userChoice = UserInput.GetUserInt(0)
            if DataValidate.ValidRangeInt(userChoice, -1, 1, True) == True:
                break
            else:
                MessageContainer.ErrorMsg(3, "Inclusive", -1, 1)
            
        if userChoice == -1:
            break
        elif userChoice == 1:
            MessageContainer.UserMsg(3)
        else:
            MessageContainer.UserMsg(4)
            while True:
                startGroup = UserInput.GetUserInt(1)
                if DataValidate.ValidRangeInt(startGroup, 0, 999, True) == True:
                    break
                else:
                    MessageContainer.ErrorMsg(3, "Inclusive", 0, "inf or 999")
            while True:
                startIndex = UserInput.GetUserInt(2)
                if DataValidate.ValidRangeInt(startIndex, 0, 999, True) == True:
                    break
                else:
                    MessageContainer.ErrorMsg(3, "Inclusive", 0, "inf or 999")
            while True:
                targetGroup = UserInput.GetUserInt(3)
                if DataValidate.ValidRangeInt(targetGroup, 0, 999, True) == True:
                    break
                else:
                    MessageContainer.ErrorMsg(3, "Inclusive", 0, "inf or 999")
            while True:
                targetIndex = UserInput.GetUserInt(4)
                if DataValidate.ValidRangeInt(targetGroup, 0, 999, True) == True:
                    break
                else:
                    MessageContainer.ErrorMsg(3, "Inclusive", 0, "inf or 999")
            
            start = [startGroup, startIndex]
            end = [targetGroup, targetIndex]

            MessageContainer.DebugMsg(3, startGroup, startIndex, targetGroup, targetIndex)

            path = TrainPathing.TrainPathMain(trackLayout, start, end)

            MessageContainer.UserMsg(5, path[0].trackGroup, path[0].trackIndex)
    
    MessageContainer.UserMsg(2)



TrackController()