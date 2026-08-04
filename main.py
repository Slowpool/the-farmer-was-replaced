def multipleMove(directions):
	for direction in directions:
		move(direction)

def shouldHarvest():
	if not enableHarvesting:
		result = False 
	elif (get_entity_type() == Entities.Pumpkin and smartPumpkinCollecting):
		result = canHarvestPumpkinInSmartWay()
	elif (get_entity_type() == Entities.Sunflower and smartSunflowerCollecting):
		result = can_harvest() and (measure() >= 12)
	else:
		result = can_harvest()
	return result

def canHarvestPumpkinInSmartWay():
	return pumpkinCornerMeasures[ANY_CORNER] != 0 and pumpkinCornerMeasures[LEFT_LOWER_CORNER] == pumpkinCornerMeasures[LEFT_UPPER_CORNER] and pumpkinCornerMeasures[LEFT_UPPER_CORNER] == pumpkinCornerMeasures[RIGHT_LOWER_CORNER] and pumpkinCornerMeasures[RIGHT_LOWER_CORNER] == pumpkinCornerMeasures[RIGHT_UPPER_CORNER]

def plantAndWaterAndFertilize(seed, seedIsCompanion):
	if enablePlanting:
		isPlanted = tryPlant(seed)
		
	if not isPlanted:
		return

	if enableWatering and get_water() < minWaterLevel:
		use_item(Items.Water)
	if enableFertilizing:
		use_item(Items.Fertilizer)
	if enableCompanions and not seedIsCompanion:
		if not isCompanion() and not hasCompanion() and get_companion() != None:
			plantCompanion()

def tryPlant(seed):
	if enableCompanions and isCompanion():
		return False
	else:
		plant(seed)
		return True

def isCorner():
	return (get_pos_x() == 0 or get_pos_x() == get_world_size() - 1) and (get_pos_y() == 0 or get_pos_y() == get_world_size() - 1)

def isCompanion():
	currentPosition = getCurrentPosition()
	return (currentPosition['x'], currentPosition['y']) in companionsList

def hasCompanion():
	currentPos = getCurrentPosition()
	key = buildCompanionKey(currentPos['x'], currentPos['y'])
	return key in companions


def buildCompanionKey(parentX, parentY):
	return (parentX, parentY)

def plantCompanion():
	plantType, (companionX, companionY) = get_companion()
	ownPosition = getCurrentPosition()
	moveTo(companionX, companionY)
	harvestAndPlant(plantType, True)
	moveTo(ownPosition['x'], ownPosition['y'])
	addCompanion(ownPosition['x'], ownPosition['y'], companionX, companionY)

def getCurrentPosition():
	return {'x' : get_pos_x(), 'y' : get_pos_y()}

def moveTo(x, y):
	currentPosition = getCurrentPosition()
	halfOfWorldSize = get_world_size() / 2

	currentX = currentPosition['x']
	currentY = currentPosition['y']

	fatX = x
	if (currentX > x):
		fatX += get_world_size()

	if (fatX - currentX < halfOfWorldSize):
		xDirection = East
	else:
		xDirection = West
	while not get_pos_x() == x:	
		move(xDirection)

	fatY = y
	if (currentY > y):
		fatY += get_world_size()

	if (fatY - currentY < halfOfWorldSize):
		yDirection = North
	else:
		yDirection = South
	while not get_pos_y() == y:
		move(yDirection)

def addCompanion(parentX, parentY, companionX, companionY):
	key = buildCompanionKey(parentX, parentY)
	companions[key] = {'x' : companionX, 'y' : companionY}

	companionsList.append(buildCompanionsListValue(companionX, companionY))

def buildCompanionsListValue(companionX, companionY):
	return (companionX, companionY)

def shouldTill(seed):
	return get_ground_type() != Grounds.Soil and (seed == Entities.Carrot or seed == Entities.Pumpkin or seed == Entities.Cactus)

def plantInTheRing(seed, ringSize):
	for i in range(4):
		if i == 0:
			direction = North
		elif i == 1:
			direction = East
		elif i == 2:
			direction = South
		elif i == 3:
			direction = West
		plantOnRingSide(direction, seed, ringSize)
		
def plantOnRingSide(direction, seed, ringSize):
	for side in range(ringSize - 1):
		harvestAndPlant(seed)
		move(direction)

def harvestAndPlant(seed, seedIsCompanion=False):
	if shouldHarvest():
		smartHarvest()
	if shouldTill(seed):
		till()
	if get_entity_type() != seed:
		plantAndWaterAndFertilize(seed, seedIsCompanion)

def smartHarvest():
	if enableCompanions and hasCompanion():
		killCompanion()
	harvest()
	if smartPumpkinCollecting:
		flushPumpkinCornerMeasures()

def flushPumpkinCornerMeasures():
	for cornerPosition in CORNER_POSITIONS:
		pumpkinCornerMeasures[cornerPosition] = 0

def killCompanion():
	ownPosition = getCurrentPosition()
	companionPosition = removeCompanion(ownPosition['x'], ownPosition['y'])
	moveTo(companionPosition['x'], companionPosition['y'])
	harvest()
	moveTo(ownPosition['x'], ownPosition['y'])

def removeCompanion(parentX, parentY):
	key = buildCompanionKey(parentX, parentY)
	companion = companions.pop(key)
	
	companionsListValue = buildCompanionsListValue(companion['x'], companion['y'])
	companionsList.remove(companionsListValue)

	return companion

def goToNextRing():
	move(North)
	move(East)

def goToPrevRing():
	move(West)
	move(South)

def isLastRing(currentRing, countOfRings):
	return currentRing == countOfRings - 1

def getRingSize(numberOfRing, countOfRings):
	return (countOfRings - numberOfRing + 1) * 2

def plantAsRings(seeds):
	countOfRings = len(seeds)
	
	for i in range(countOfRings):
		ringSize = getRingSize(i + 1, countOfRings)
		seed = seeds[i]
		plantInTheRing(seed, ringSize)
		
		if not isLastRing(i, countOfRings):
			goToNextRing()

	for i in range(countOfRings - 1):
		goToPrevRing()

def huntTheTreasure():
	plantTheBiggestMaze()
	findTheTreasure()

def plantTheBiggestMaze():
	plant(Entities.Bush)
	numberOfSubstances = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, numberOfSubstances)

def findTheTreasure():
	direction = North
	while not isTreasure():
		direction = tryGoToNextCellInMaze(direction)
	harvest()

def isTreasure():
	return get_entity_type() == Entities.Treasure

def tryGoToNextCellInMaze(direction):
	if tryMoveRight(direction):
		return rightFrom(direction)
	elif tryMoveTowards(direction):
		return direction
	else:
		return leftFrom(direction)

def tryMoveRight(direction):
	direction = rightFrom(direction)
	return move(direction)

def tryMoveTowards(direction):
	return move(direction)

def rightFrom(direction):
	if direction == North:
		direction = East
	elif direction == East:
		direction = South
	elif direction == South:
		direction = West
	elif direction == West:
		direction = North
	return direction
	
def leftFrom(direction):
	if direction == North:
		direction = West
	elif direction == West:
		direction = South
	elif direction == South:
		direction = East
	elif direction == East:
		direction = North
	return direction

def plantInColumnByDrones(seeds):
	for seed in seeds:
		plantOneColumnByDrone(seed)
		move(West)
		tryUpdatePumpkinMeasuresAndCollectBiggestPumpkin()

def tryUpdatePumpkinMeasuresAndCollectBiggestPumpkin():
	if smartPumpkinCollecting:
		updateLastPumpkinMeasures(measure())
		tryCollectTheBiggestPumpkin()

def updateLastPumpkinMeasures(newMeasure):
	if len(lastPumpkinMeasures) == MAX_PUMPKIN_MEASURES:
		lastPumpkinMeasures.pop(0)
	lastPumpkinMeasures.append(newMeasure)

def tryCollectTheBiggestPumpkin():
	if len(lastPumpkinMeasures) > 1:
		shouldHarvestPumpkin = True
		for i in range(MAX_PUMPKIN_MEASURES - 1):
			shouldHarvestPumpkin = shouldHarvestPumpkin and lastPumpkinMeasures[i] == lastPumpkinMeasures[i + 1]
		if shouldHarvestPumpkin:
			harvest()


def plantOneColumnByDrone(seed):
	def plantOneColumn():
		for _ in range(get_world_size()):
			harvestAndPlant(seed)
			move(North)
			tryRememberPumpkinMeasure()

	drone = None
	while drone == None:
		if num_drones() < MAX_DRONES:
			drone = spawn_drone(plantOneColumn)
	
	return drone

def tryRememberPumpkinMeasure():
	if (smartPumpkinCollecting and isCorner()):
		pumpkinCornerMeasures[(get_pos_x(), get_pos_y())] = measure()

LEFT_LOWER_CORNER = (0, 0)
LEFT_UPPER_CORNER =  (0, get_world_size() - 1)
RIGHT_LOWER_CORNER =  (get_world_size() - 1, 0)
RIGHT_UPPER_CORNER = (get_world_size() - 1, get_world_size() - 1)
CORNER_POSITIONS = (LEFT_LOWER_CORNER, LEFT_UPPER_CORNER, RIGHT_LOWER_CORNER, RIGHT_UPPER_CORNER)

ANY_CORNER = LEFT_LOWER_CORNER

MAX_DRONES = max_drones()

MAX_PUMPKIN_MEASURES = 5

pumpkinCornerMeasures = {}
flushPumpkinCornerMeasures()
smartPumpkinCollecting = False
lastPumpkinMeasures = []

smartSunflowerCollecting = False

enablePlanting = True
enableWatering = True
minWaterLevel = 0.50
enableFertilizing = False
enableHarvesting = True

companions = {}
companionsList = []
enableCompanions = False

# clear()
# findTheTreasure()

#seeds = [Entities.Pumpkin, Entities.Pumpkin, Entities.Pumpkin, Entities.Pumpkin, Entities.Pumpkin, Entities.Pumpkin, Entities.Pumpkin, Entities.Pumpkin]
	
seeds = [Entities.Grass, Entities.Carrot, Entities.Tree, Entities.Carrot, Entities.Grass, Entities.Carrot, Entities.Tree]
	
#seeds = [Entities.Carrot, Entities.Carrot, Entities.Carrot, Entities.Carrot, Entities.Carrot, Entities.Carrot, Entities.Carrot, Entities.Carrot]

seeds = [Entities.Grass, Entities.Carrot, Entities.Grass, Entities.Carrot, Entities.Grass, Entities.Carrot, Entities.Grass, Entities.Carrot]

#seeds = [Entities.Tree, Entities.Bush, Entities.Tree, Entities.Bush, Entities.Tree, Entities.Bush, Entities.Tree, Entities.Bush]

#seeds = [Entities.Tree, Entities.Tree, Entities.Tree, Entities.Tree, Entities.Tree, Entities.Tree, Entities.Tree, Entities.Tree]
	
#seeds = [Entities.Tree, Entities.Carrot, Entities.Tree, Entities.Carrot, Entities.Tree, Entities.Carrot, Entities.Tree, Entities.Carrot]

#seeds = [Entities.Grass, Entities.Grass, Entities.Grass, Entities.Grass, Entities.Grass, Entities.Grass, Entities.Grass, Entities.Grass]

#seeds = [Entities.Sunflower, Entities.Sunflower, Entities.Sunflower, Entities.Sunflower, Entities.Sunflower, Entities.Sunflower, Entities.Sunflower, Entities.Sunflower]
	
#seeds = [Entities.Cactus, Entities.Cactus, Entities.Cactus, Entities.Cactus, Entities.Cactus, Entities.Cactus, Entities.Cactus, Entities.Cactus, Entities.Cactus]

while True:
	# plantAsRings(seeds)

	plantInColumnByDrones(seeds)

	# huntTheTreasure()

# harvest()
# plant(Entities.Pumpkin)
# print(get_entity_type())