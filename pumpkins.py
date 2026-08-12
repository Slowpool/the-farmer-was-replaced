import utils

FIELD_WIDTH_FOR_ONE_DRONE = get_world_size() / max_drones()
NUMBER_OF_CELLS_PER_DRONE = get_world_size() * FIELD_WIDTH_FOR_ONE_DRONE

LEFT_HORIZONTAL_BOUNDARY = 'LEFT_HORIZONTAL_BOUNDARY'
NOT_HORIZONTAL_BOUNDARY = 'NOT_HORIZONTAL_BOUNDARY'
RIGHT_HORIZONTAL_BOUNDARY = 'RIGHT_HORIZONTAL_BOUNDARY'

MIN_THE_BIGGEST_PUMPKIN_PROBES = get_world_size() / 2

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
	utils.moveToPosition(startPoint)
	def plantPumpkinsAsSubdrone():
		global ownStartPoint
		ownStartPoint = startPoint
		while True:
			plantPumpkinsOnOwnTerritory()
			traverseOwnDeadPumpkinsFirstTime()
			while thereAreDeadPumpkins():
				traverseOwnDeadPumpkins()
			# TODO help neighbour?
			waitForTheBiggestPumpkinHarvesting()
	spawn_drone(plantPumpkinsAsSubdrone)

def plantPumpkinsAsMaster():
	global ownStartPoint
	utils.moveToPosition(ownStartPoint)
	theBiggestPumpkinProbes = []
	while True:
		plantPumpkinsOnOwnTerritory()
		traverseOwnDeadPumpkinsFirstTime()
		while thereAreDeadPumpkins():
			traverseOwnDeadPumpkins()
		while not theBiggestPumpkinIsGrown(theBiggestPumpkinProbes):
			clearTheBiggestPumpkinProbes(theBiggestPumpkinProbes)
			collectTheBiggestPumpkinInfo(theBiggestPumpkinProbes)
		harvest()


def plantPumpkinsOnOwnTerritory():
	global ownStartPoint
	utils.moveToPosition(ownStartPoint)
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
	for deadPumpkinPosition in deadPumpkins:
		utils.moveToPosition(deadPumpkinPosition)
		if isDeadPumpkin():
			plantPumpkin()
		else:
			forgetDeadPumpkin(deadPumpkinPosition)

def forgetDeadPumpkin(position):
	deadPumpkins.remove(position)

def waitForTheBiggestPumpkinHarvesting():
	while thereIsPumpkinBeneath():
		pass

def thereIsPumpkinBeneath():
	return get_entity_type() == Entities.Pumpkin

def theBiggestPumpkinIsGrown(theBiggestPumpkinProbes):
	if len(theBiggestPumpkinProbes) < MIN_THE_BIGGEST_PUMPKIN_PROBES:
		return False

	prevPumpkinProbe = theBiggestPumpkinProbes[0]
	for i in range(len(theBiggestPumpkinProbes) - 1):
		if prevPumpkinProbe != theBiggestPumpkinProbes[i + 1]:
			return False
		else:
			# theBiggestPumpkinProbes[i + 1] copy-pasted in optimization purposes
			prevPumpkinProbe = theBiggestPumpkinProbes[i + 1]
	return True

# TODO does it work?
def clearTheBiggestPumpkinProbes(theBiggestPumpkinProbes):
	while len(theBiggestPumpkinProbes) != 0:
		theBiggestPumpkinProbes.pop()

def collectTheBiggestPumpkinInfo(theBiggestPumpkinProbes):
	# collectTheBiggestPumpkinInfoRandomly()
	collectTheBiggestPumpkinInfoTraversing(theBiggestPumpkinProbes)

def collectTheBiggestPumpkinInfoTraversing(theBiggestPumpkinProbes):
	for i in range(get_world_size()):
		theBiggestPumpkinProbes.append(measure())
		move(North)


clear()
change_hat(Hats.Carrot_Hat)
if __name__ == '__main__':
	startPumpking()