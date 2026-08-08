import utils

relativeStartPoint = None
fieldWidthForOneDrone = None
deadPumpkins = []

def startPumpking():
    startPositionsForSubdrones = calculatePositionsForSubdrones()
    print(startPositionsForSubdrones)
    placeSubrones(startPositionsForSubdrones)
    plantPumpkinsAsMaster()

def calculatePositionsForSubdrones():

    global relativeStartPoint
    global fieldWidthForOneDrone
    relativeStartPoint = utils.getCurrentPosition()
    
    fieldWidthForOneDrone = calculateFieldWidthForOneDrone()

    currentX = relativeStartPoint['x']
    startPositionsForSubdrones = []
    for i in range(max_drones() - 1):
        currentX += fieldWidthForOneDrone
        nextSubdronePosition = utils.newPoint(currentX, relativeStartPoint['y'])
        startPositionsForSubdrones.append(nextSubdronePosition)
    return startPositionsForSubdrones

def calculateFieldWidthForOneDrone():
    return get_world_size() / max_drones()

def placeSubrones(startPositionsForSubdrones):
    for startPositionForSubdrone in startPositionsForSubdrones:
        placeSubdrone(startPositionForSubdrone)

def placeSubdrone(startPoint):
    utils.moveToPoint(startPoint)
    def plantPumpkinsAsSubdrone():
        ownStartPoint = startPoint
        # TODO use startPoint somehow
        while True:
            plantPumpkinsOnOwnTerritory()
            traverseOwnDeadPumpkinsFirstTime()
            while len(deadPumpkins) != 0:
                traverseOwnDeadPumpkins()
            # TODO help neighbour?
            waitForTheBiggestPumpkinHarvesting()
    spawn_drone(plantPumpkinsAsSubdrone)

def plantPumpkinsAsMaster():
    global relativeStartPoint
    utils.moveToPoint(relativeStartPoint)
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

if __name__ == '__main__':
    startPumpking()