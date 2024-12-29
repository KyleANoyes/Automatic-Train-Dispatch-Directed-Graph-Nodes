#   Import universal scripts
import Globals
import MessageContainer

#   Import full supporting scripts

#   Import partial supporting scripts

#   Import Python modules
import regex as re  #   pip install regex
import ast
import copy

# --------------------------------------- #


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