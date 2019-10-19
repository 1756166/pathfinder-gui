import pygame
from way_point import Waypoint

''' -- FRC STANDARD FIELD DIMENSIONS -- 
		27 ft 7 in X 54 ft 1 in
		scale accordingly
'''
def reset(waypoints_info, origin_coords):
	for waypnt in waypoints_info:
		waypnt.transpose(origin_coords)

def write_to_dict(waypoints_info, alliance_color): # updates specified dictionary
	copy, origin_coords = transpose(waypoints_info)
	encapsulated_info = encapsulate(copy)
	return [alliance_color, encapsulated_info, origin_coords]
	
def encapsulate(waypoints_info): # encapsulates info into easy-to-read list of lists
	encapsulated_info = []
	for waypnt in waypoints_info:
		encapsulated_info.append(waypnt.encapsulate())
	
	return encapsulated_info

def transpose(waypoints_info): # transposes it to make it easier for json loader in java side
	copy = waypoints_info.copy()

	origin_x = copy[0].coords[0]
	origin_y = copy[0].coords[1]
	for waypnt in copy:
		waypnt.transpose([origin_x, origin_y])
	return copy, [origin_x, origin_y]

def simulate(existing_waypoints=None, alliance_color=None):

	pygame.init()

	background = pygame.image.load('Resources\\game_image.jpg')
	background = pygame.transform.scale(background, (background.get_width() * 2, background.get_height() * 2))
	dimensions = (background.get_width(), background.get_height())

	# Init all images/buttons
	plus_button = pygame.image.load('Resources\\add_waypoint.jpg')
	plus_button = pygame.transform.scale(plus_button, (42, 42)) # NICE
	trash_can = pygame.image.load('Resources\\remove_waypoint.jpg')
	trash_can = pygame.transform.scale(trash_can, (42, 42)) # VERY NICE

	# Init display
	display = pygame.display.set_mode(dimensions)
	pygame.display.set_caption('Generate Waypoints')
	clock = pygame.time.Clock()

	# Simply to generate bounding rects for each image
	add_waypoint_rect = display.blit(plus_button, (0, 0))
	del_waypoint_rect = display.blit(trash_can, (0, 42))

	CRASHED = False
	waypoints_info = []

	if existing_waypoints:
		origin_coords = existing_waypoints[2]

		if existing_waypoints[0] == 'Red':
			background = pygame.transform.rotate(background, 180)

		for i, encapsulated in enumerate(existing_waypoints[1]):
			new_waypoint = Waypoint(i, [encapsulated[0], encapsulated[1]], encapsulated[2])
			waypoints_info.append(new_waypoint)
		reset(waypoints_info, [origin_coords[0] * -1, origin_coords[1] * -1])
	else:
		if alliance_color == 'Red':
			background = pygame.transform.rotate(background, 180)

		waypoint = Waypoint() # Default constructor
		waypoints_info = [waypoint]

	id = len(waypoints_info) - 1
	selected_waypoint = None

	init_x, init_y = 10, 140

	while not CRASHED:
		clock.tick(60)

		# Draws the delete button, add waypoint button, and bakckground image.
		display.blit(background, (0, 0))
		display.blit(plus_button, (0, 0))
		display.blit(trash_can, (0, 42))
		mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))

		if len(waypoints_info) > 1:
			for i in range(1, len(waypoints_info)):
				pygame.draw.line(display, (255, 165, 0), waypoints_info[i-1].coords, waypoints_info[i].coords)
				# Draw waypoints
				waypoints_info[i-1].draw(display)
				waypoints_info[i].draw(display)
			waypoints_info[0].draw(display, (0, 255, 0))
			waypoints_info[-1].draw(display, (255, 0, 0))
		else:
			waypoints_info[0].draw(display)
		
		for waypnt in waypoints_info:
			waypnt.draw_line(display, [waypnt.coords[0]+10, waypnt.coords[1]])
			pygame.draw.rect(display, (0, 255, 0), waypnt.angle_rect, 1)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				CRASHED = True

			if event.type == pygame.MOUSEBUTTONDOWN:
				if add_waypoint_rect.contains(mouse_rect): # if the plus button is pressed
					# add a new waypoint to array, which will then be drawn
					id += 1
					new_waypoint = Waypoint(id, [init_x, init_y])
					waypoints_info.append(new_waypoint)
					init_y += 12
				
				elif del_waypoint_rect.contains(mouse_rect): # if delete waypoint button is pressed
					# delete last waypoint
					if waypoints_info:			
						if selected_waypoint is waypoints_info[-1]:
							selected_waypoint = None
						id -= 1
						init_y -= 12
						waypoints_info.pop(-1) # Deletes last elem in list of waypoints

				for waypnt in waypoints_info: # Allows you to select other waypoints
					if waypnt.bounding_rect.contains(mouse_rect):
						selected_waypoint = waypnt
					

			if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1: # if mouse is dragged
				if not add_waypoint_rect.contains(mouse_rect) and not del_waypoint_rect.contains(mouse_rect):	
					if selected_waypoint != None and selected_waypoint.bounding_rect.contains(mouse_rect):
						selected_waypoint.update_coords(list(pygame.mouse.get_pos()))

			pygame.display.update()

	encapsulated_info = write_to_dict(waypoints_info, alliance_color)
	
	# Resets coordinates for next time
	origin_coords = [encapsulated_info[2][0] * -1, encapsulated_info[2][1] * -1]
	reset(waypoints_info, origin_coords)

	pygame.quit()
	return encapsulated_info