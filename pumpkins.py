
def startPumpking():
    calculatePositionsForDrones()
    placeDrones()
    plantPumpkinsAsMaster()

def calculatePositionsForDrones():
    

def plantPumpkinsAsSubordinate():
    while True:
        plantPumpkinsOnOwnTerritory()
        traverseOwnDeadPumpkinsFirstTime()
        while len(deadPumpkins) != 0:
            traverseOwnDeadPumpkins()
        # TODO help neighbour?
        waitForTheBiggestPumpkinHarvesting()

def plantPumpkinsAsMaster():
    while True:
        plantPumpkinsOnOwnTerritory()
        traverseOwnDeadPumpkinsFirstTime()
        while len(deadPumpkins) != 0:
            traverseOwnDeadPumpkins()
        while theBiggestPumpkinIsGrown() != True:
            observeTheBiggestPumpkin()
        harvest()
