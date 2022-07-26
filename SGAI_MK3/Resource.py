class Resource:
    name = ""
    currentValue : int = 0
    maxValue : int = 0
    actions = {        }
    
    def __init__(self, name, maxval, action):
        self.name = name
        self.maxValue = maxval
        self.actions = action

    def clone(self):
        ret = Resource(self.name, self.maxValue)
        ret.currentValue = self.currentValue
        return ret

    def alterByPercent(self, percent, max):
        newVal = self.currentValue 

        if max == True:
            newVal += self.maxValue * (percent/100)
        else:
            newVal += self.currentValue * (percent/100)

        if newVal >= self.maxValue:
            self.currentValue = self.maxValue
        elif newVal <= 0:
            self.currentValue = 0 
        else:
            self.currentValue = newVal

    def alterByValue(self, value):
        newVal = self.currentValue + value

        if newVal >= self.maxValue:
            self.currentValue = self.maxValue
        elif newVal <= 0:
            self.currentValue = 0 
        else:
            self.currentValue = newVal
    def setToMax(self):
        self.currentValue = self.maxValue        
    def checkCost(self, action):
        if self.actions[action] > self.currentValue:
            return False
        return True