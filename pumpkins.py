import utils

FIELD_WIDTH_FOR_ONE_DRONE = get_world_size() / max_drones()
NUMBER_OF_CELLS_PER_DRONE = get_world_size() * FIELD_WIDTH_FOR_ONE_DRONE

LEFT_HORIZONTAL_BOUNDARY = 'LEFT_HORIZONTAL_BOUNDARY'
NOT_HORIZONTAL_BOUNDARY = 'NOT_HORIZONTAL_BOUNDARY'
RIGHT_HORIZONTAL_BOUNDARY = 'RIGHT_HORIZONTAL_BOUNDARY'

ownStartPoint = None
deadPumpkins = []

def startPumpking():
	startPositionsForSubdrones = calculatePositionsForSubdrones()
	placeSubrones(startPositionsForSubdrones)
	plantPumpkinsAsMaster()

def calculatePositionsForSubdrones():

	global ownStartPoint
	ownStartPoint = utils.getCurrentPosition()

	currentX = ownStartPoint['x']
	startPositionsForSubdrones = []
	for i in range(max_drones() - 1):
		currentX += FIELD_WIDTH_FOR_ONE_DRONE
		nextSubdronePosition = utils.newPoint(currentX, ownStartPoint['y'])
		startPositionsForSubdrones.append(nextSubdronePosition)
	return startPositionsForSubdrones


def placeSubrones(startPositionsForSubdrones):
	for startPositionForSubdrone in startPositionsForSubdrones:
		placeSubdrone(startPositionForSubdrone)

def placeSubdrone(startPoint):
	utils.moveToPoint(startPoint)
	def plantPumpkinsAsSubdrone():
		global ownStartPoint
		ownStartPoint = startPoint
		while True:
			plantPumpkinsOnOwnTerritory()
			traverseOwnDeadPumpkinsFirstTime()
			# TODO here i stopped
			while thereAreDeadPumpkins():
				traverseOwnDeadPumpkins()
			# TODO help neighbour?
			waitForTheBiggestPumpkinHarvesting()
	spawn_drone(plantPumpkinsAsSubdrone)

def plantPumpkinsAsMaster():
	global ownStartPoint
	utils.moveToPoint(ownStartPoint)
	while True:
		plantPumpkinsOnOwnTerritory()
		traverseOwnDeadPumpkinsFirstTime()
		while len(deadPumpkins) != 0:
			traverseOwnDeadPumpkins()
		while theBiggestPumpkinIsGrown() != True:
			observeTheBiggestPumpkin()
		harvest()

def plantPumpkinsOnOwnTerritory():
	global ownStartPoint
	utils.moveToPoint(ownStartPoint)
	for i in range(NUMBER_OF_CELLS_PER_DRONE):
		plantPumpkin()
		goToNextCell()

def plantPumpkin():
	# TODO do it once in first traversing
	if (get_ground_type() != Grounds.Soil):
		till()
	plant(Entities.Pumpkin)


def goToNextCell():
	# TODO it is not needed if you have 32 drones
	horizontalBoundary = compareHorizontalBoundary()
	if (horizontalBoundary == LEFT_HORIZONTAL_BOUNDARY):
		if get_pos_y() % 2 == 0:
			move(East)
		else:
			move(North)
	elif (horizontalBoundary == NOT_HORIZONTAL_BOUNDARY):
		if get_pos_y() % 2 == 0:
			move(East)
		else:
			move(West)
	elif (horizontalBoundary == RIGHT_HORIZONTAL_BOUNDARY):
		if get_pos_y() % 2 == 0:
			move(North)
		else:
			move(West)
	else:
		utils.moveTo(9)

def compareHorizontalBoundary():
	modX = get_pos_x() % FIELD_WIDTH_FOR_ONE_DRONE
	if modX == 0:
		return LEFT_HORIZONTAL_BOUNDARY
	elif modX == (FIELD_WIDTH_FOR_ONE_DRONE - 1):
		return RIGHT_HORIZONTAL_BOUNDARY
	else:
		return NOT_HORIZONTAL_BOUNDARY

def traverseOwnDeadPumpkinsFirstTime():
	global ownStartPoint
	for i in range(NUMBER_OF_CELLS_PER_DRONE):
		if (isDeadPumpkin()):
			rememberDeadPumpkin()
			plantPumpkin()
		goToNextCell()

def isDeadPumpkin():
	return not can_harvest()

def rememberDeadPumpkin():
	deadPumpkin = utils.getCurrentPosition()
	deadPumpkins.append(deadPumpkin)

def thereAreDeadPumpkins():
	return len(deadPumpkins) != 0

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

clear()
change_hat(Hats.Carrot_Hat)
if __name__ == '__main__':
	startPumpking()