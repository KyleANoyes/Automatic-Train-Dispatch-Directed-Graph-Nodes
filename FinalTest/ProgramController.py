#   Import supporting scripts
import ClassContainer
import DataInit
import TrainPathing
import Globals

#   Import specific parts of modules

#   Import Python modules
import json

# --------------------------------------- #


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

    #   Call Pathing Agent Creator
    TrainPathing.TrainPathMain(trackLayout)


TrackController()