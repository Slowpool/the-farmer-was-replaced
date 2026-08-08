def multipleMove(directions):
	for direction in directions:
		move(direction)

def isCorner():
	currentX = get_pos_x()
	currentY = get_pos_y()
	return (currentX == 0 or currentX == get_world_size() - 1) and (currentY == 0 or currentY == get_world_size() - 1)

def getCurrentPosition():
	return {'x' : get_pos_x(), 'y' : get_pos_y()}

def moveToPoint(point):
	moveTo(point['x'], point['y'])

def moveTo(x, y):
	x = x % get_world_size()
	y = y % get_world_size()
	halfOfWorldSize = get_world_size() / 2

	currentX = get_pos_x()
	currentY = get_pos_y()

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

def shouldTill(seed):
	return (seed == Entities.Carrot or seed == Entities.Pumpkin or seed == Entities.Cactus) and get_ground_type() != Grounds.Soil

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

def newPoint(x, y):
	return {'x' : x, 'y' : y}