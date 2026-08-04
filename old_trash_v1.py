while True:
	for side in range(get_world_size() - 1):
		if can_harvest():
			harvest()
			if get_ground_type() != Grounds.Soil:
				till()
		if get_entity_type() == None:
			plant(Entities.Carrot)
		move(North)

	for side in range(get_world_size() - 1):
		if can_harvest():
			harvest()
			if get_ground_type() != Grounds.Soil:
				till()
		if get_entity_type() == None:
			plant(Entities.Carrot)
		move(East)
	
	for side in range(get_world_size() - 1):
		if can_harvest():
			harvest()
			if get_ground_type() != Grounds.Soil:
				till()
		if get_entity_type() == None:
			plant(Entities.Carrot)
		move(South)
	
	for side in range(get_world_size() - 1):
		if can_harvest():
			harvest()
			if get_ground_type() != Grounds.Soil:
				till()
		if get_entity_type() == None:
			plant(Entities.Carrot)
		move(West)
	
	move(North)
	move(East)
	if can_harvest():
		harvest()
	if get_entity_type() == None:
		plant(Entities.Bush)
	move(North)
	
	if can_harvest():
		harvest()
	if get_entity_type() == None:
		plant(Entities.Grass)
	move(East)
	
	if can_harvest():
		harvest()
	if get_entity_type() == None:
		plant(Entities.Bush)
	move(South)
	
	if can_harvest():
		harvest()
	if get_entity_type() == None:
		plant(Entities.Grass)
	move(West)
	move(West)
	move(South)