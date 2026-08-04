import utils

relativeStartPoint = None
fieldWidthForOneDrone = None
deadPumpkins = []

def startPumpking():
    positionsForDrones = calculatePositionsForDrones()
    print(positionsForDrones)
    placeDrones(positionsForDrones)
    plantPumpkinsAsMaster()

def calculatePositionsForDrones():
    global relativeStartPoint, fieldWidthForOneDrone
    relativeStartPoint = utils.getCurrentPosition()
    
    fieldWidthForOneDrone = calculateFieldWidthForOneDrone()

    currentX = relativeStartPoint['x']
    positionsForDrones = [relativeStartPoint]
    for i in range(max_drones() - 1):
        currentX += fieldWidthForOneDrone
        nextDronePosition = (currentX, relativeStartPoint['y'])
        positionsForDrones.append(nextDronePosition)
    return positionsForDrones

def calculateFieldWidthForOneDrone():
    return get_world_size() / max_drones()

def placeDrones():
    # TODO
    pass

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

def plantPumpkinsOnOwnTerritory():
    # TODO
    pass

def traverseOwnDeadPumpkinsFirstTime():
    # TODO
    pass
def traverseOwnDeadPumpkins():
    # TODO
    pass

def waitForTheBiggestPumpkinHarvesting():
    # TODO
    pass

def theBiggestPumpkinIsGrown():
    # TODO
    pass

def observeTheBiggestPumpkin():
    # TODO
    pass