from random import randrange, randomimport matplotlib.pyplot as pltfrom matplotlib import pyplotclass MockedInterface:    BUTTON = 1    TEXT = 2.0    EMPTY = 0.0#     [#     [MockedInterface.EMPTY, MockedInterface.EMPTY, MockedInterface.EMPTY, MockedInterface.EMPTY, MockedInterface.EMPTY,#      MockedInterface.EMPTY, MockedInterface.TEXT],#     [MockedInterface.EMPTY, MockedInterface.EMPTY, MockedInterface.TEXT, MockedInterface.EMPTY, MockedInterface.EMPTY,#      MockedInterface.EMPTY, MockedInterface.EMPTY],#    [ MockedInterface.BUTTON, MockedInterface.EMPTY, MockedInterface.EMPTY, MockedInterface.EMPTY, MockedInterface.BUTTON,#     MockedInterface.EMPTY, MockedInterface.EMPTY],#   [  MockedInterface.EMPTY, MockedInterface.EMPTY, MockedInterface.EMPTY, MockedInterface.EMPTY, MockedInterface.EMPTY,#     MockedInterface.EMPTY, MockedInterface.EMPTY],#    [ MockedInterface.EMPTY, MockedInterface.EMPTY, MockedInterface.BUTTON, MockedInterface.EMPTY, MockedInterface.EMPTY,#     MockedInterface.EMPTY, MockedInterface.EMPTY],#     [MockedInterface.EMPTY, MockedInterface.EMPTY, MockedInterface.EMPTY, MockedInterface.EMPTY, MockedInterface.EMPTY,#     MockedInterface.EMPTY, MockedInterface.EMPTY],#     [MockedInterface.EMPTY, MockedInterface.BUTTON, MockedInterface.EMPTY, MockedInterface.EMPTY, MockedInterface.EMPTY,#      MockedInterface.EMPTY, MockedInterface.EMPTY]# ]def constructMap(size):    map = []    for i in range(size):        row = []        for j in range(size):            n = randrange(3)            a = random()            if a <= 0.04:                row.append(MockedInterface.TEXT)            elif  a <= 0.24 and a > 0.1:                row.append(MockedInterface.BUTTON)            else:                row.append(MockedInterface.EMPTY)        map.append(row)    return mapinitialMap = constructMap(10)class InterfaceAgent:    def __init__(self):        self.isButton = False        self.isText = False        self.isEmpty = False        self.isTheCellNextClicked = False        self.isTheRowBellowAboveClicked = False        self.isTextZoomed = False    def see(self, perception):        if (perception.isCellButton()):            self.isButton = True            self.isTheCellNextClicked, self.new_y = perception.isTheCellNextClicked()            self.isTheRowBellowAboveClicked, self.new_x = perception.isTheRowAboveOrBellowClicked()        elif (perception.isCellText()):            self.isText = True            self.isTextZoomed = perception.isCellTextZoomed()        else:            self.isEmpty = True    def takeAction(self):       if(self.isText and self.isTextZoomed):           return IncreaseTextAction()       elif(self.isButton):           if self.isTheCellNextClicked:               return IncreaseButtonAction(self.new_y)           elif self.isTheRowBellowAboveClicked:               return MoveButtonAction(self.new_x)class InterfaceAgentPerception:    def __init__(self, state, agent):        self.state = state        self.agent = agent        self.agentX = state.agentX[-1]        self.agentY = state.agentY[-1]    def setClickedAndZoomedMap(self, map):        self.clicked_and_zoom_map = map    def isCellButton(self):        return self.state.isButton(self.agentX, self.agentY)    def isCellText(self):        return self.state.isText(self.agentX, self.agentY)    def isCellTextZoomed(self):        zoomedValue= self.clicked_and_zoom_map[self.agentX][self.agentY]        if(zoomedValue < 0):            return True        return False    def isCellEmpty(self):        return self.state.isEmpty(self.agentX, self.agentY)    def isTheCellNextClicked(self):        clickedValue= self.clicked_and_zoom_map[self.agentX][self.agentY]        if not self.isEndRow(self.agentY):            new_y = self.agentY + 1        else:            new_y = self.agentY - 1        value =  self.clicked_and_zoom_map[self.agentX][new_y]        if value > 0:            if clickedValue == 0 or value > clickedValue:                return True, new_y        return False, -1    def isTheRowAboveOrBellowClicked(self):        clickedValue= self.clicked_and_zoom_map[self.agentX][self.agentY]        if not self.isTheLastRow(self.agentX):            new_x = self.agentX + 1        else:            new_x = self.agentX - 1        value = self.clicked_and_zoom_map[new_x][self.agentY]        if value > 0:            if clickedValue == 0 or value > clickedValue:                return True, new_x        return False, -1    def isFirstRow(self, i):        if i > 0: return False        return True    def isTheLastRow(self, i):        if i< self.state.x_length - 1:            return False        return True    def isEndRow(self, j):        if j == self.state.y_length - 1:            return True        return False    def isBeginningRow(self, j):        if j == 0:            return True        return Falseclass InterfaceAgentState:    def __init__(self):        self.map = initialMap        self.x_length = len(initialMap[0])        self.y_length = len(initialMap[0])        self.agentY = [-1]        self.agentX = [-1]    def setAgentX(self, x):        self.agentX = x    def setAgentY(self, y):        self.agentY = y    def getState(self):        return self    def isButton(self, i, j):        return self.map[i][j] == MockedInterface.BUTTON    def isText(self, i, j):        return self.map[i][j] == MockedInterface.TEXT    def isEmpty(self, i, j):        return self.map[i][j] == MockedInterface.EMPTY    def increaseButton(self, i, new_j):        if self.map[i[-1]][new_j] == MockedInterface.EMPTY:            self.agentY.append(new_j)            self.map[i[-1]][new_j] = MockedInterface.BUTTON    def moveButton(self, new_i, j, i):        if self.map[new_i][j[-1]] == MockedInterface.EMPTY:            self.agentX = new_i            self.map[new_i][j[-1]] = MockedInterface.BUTTON            self.map[i[-1]][j[-1]] = MockedInterface.EMPTY    def increaseText(self, i, j):        # todo check that they zoomed        if j[-1] == self.y_length-1:            new_j = j[-1]-1        else: new_j = j[-1]+1        if(self.map[i[-1]][new_j] == MockedInterface.EMPTY):            self.map[i[-1]][new_j] = MockedInterface.TEXT            self.agentY.append(new_j)    def showMap(self):        pyplot.figure(figsize=(self.x_length, self.y_length))        pyplot.imshow(self.map)        pyplot.show()class InterfaceEnvironment:    def __init__(self, state, agent):        self.state = state        self.agent = agent    def getPercent(self, agent):        perception = InterfaceAgentPerception(self.state, agent)        return perception    def setInitialState(self, state):        self.state = state    def getCurrentState(self):        return self.state    def updateState(self, action):        self.state = action.execute(self.state)class IncreaseTextAction:    def execute(self, state):        i = state.agentX        j = state.agentY        state.increaseText(i, j)        return stateclass MoveButtonAction:    def __init__(self, new_i = -1):        self.new_i = new_i    def execute(self, state):        if(self.new_i > 0):            j = state.agentY            i = state.agentX            state.moveButton(self.new_i, j, i)        return stateclass IncreaseButtonAction:    def __init__(self, new_j = -1):        self.new_j = new_j    def execute(self, state):        if(self.new_j > 0):            i = state.agentX            state.increaseButton(i, self.new_j)        return state## print(initialMap)# state = InterfaceAgentState()# state.showMap()