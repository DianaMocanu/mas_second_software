from random import randomfrom interface_agent import initialMapclicked_and_zoom_map = [ [0]* len(initialMap[0]) for i in range(len(initialMap[0]))]class UpgradingAgent:    def __init__(self):        self.clicked = False        self.zoomed = False    def see(self, perception):        if(perception.isCellClicked()): self.clicked = True        if(perception.isCellZoomed()): self.zoomed = True    def takeAction(self):        a = random()        if a <= 0.04:            return ZoomInAction()        elif a <= 0.24 and a > 0.1:            return ClickAction()class UpgradingAgentPerception:    def __init__(self, state, agent):        self.state = state        self.agent = agent        self.i = state.agentX        self.j = state.agentY    def isCellClicked(self):        return self.state.getZoomClickedMapValue(self.i, self.j) > 0    def isCellZoomed(self):        return self.state.getZoomClickedMapValue(self.i,self.j) < 0class UpgradingAgentState:    def __init__(self):        self.x_length = 6        self.y_length = 6        self.agentY = 0        self.agentX = 0        self.zoomedClickedMap = clicked_and_zoom_map    def setAgentX(self, x):        self.agentX = x    def setAgentY(self, y):        self.agentY = y    def getState(self):        return self    def getZoomClickedMapValue(self, i, j):        return self.zoomedClickedMap[i][j]    def clickCell(self, i, j):        self.zoomedClickedMap[i][j] += 1    def zoomCell(self, i, j):        self.zoomedClickedMap[i][j] -= 1class UpgradingAgentEnv:    def __init__(self, state):        self.state = state    def getPercept(self, agent):        perception  = UpgradingAgentPerception(self.state, agent)        return perception    def setInitialState(self, state):        self.state = state    def getCurrentState(self):        return self.state    def updateState(self, action):        self.state = action.execute(self.state)# Actions"class ZoomInAction:    def execute(self,state):        i = state.agentX        j = state.agentY        state.zoomCell(i, j)        return stateclass ClickAction:    def execute(self, state):        i = state.agentX        j = state.agentY        state.clickCell(i, j)        return state