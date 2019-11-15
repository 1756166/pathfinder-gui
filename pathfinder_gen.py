import pygame, math
from way_point import Waypoint

''' -- FRC STANDARD FIELD DIMENSIONS -- 
		27 ft 7 in X 54 ft 1 in
		scale accordingly
'''
def derive_rots(waypoints_info):
	if len(waypoints_info) > 1:
		for i in range(0, len(waypoints_info) - 1):
			waypoints_info[i].derive_rot()
	else:
		waypoints_info[0].rot = 0

def reset(waypoints_info, origin_coords):
	for waypnt in waypoints_info:
		waypnt.transpose(origin_coords)

def write_to_dict(waypoints_info): # updates specified dictionary
	derive_rots(waypoints_info)
	copy, origin_coords = transpose(waypoints_info)
	encapsulated_info = encapsulate(copy)
	return [encapsulated_info, origin_coords]
	
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

def simulate(title, existing_waypoints=None, alliance_color=None):

	pygame.init()
	pygame.display.set_caption('Generate Waypoints: ' + title)
	pygame.display.set_icon(pygame.transform.scale(pygame.image.load('Resources\\pathfinder_logo.png'), (100, 100)))
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
	clock = pygame.time.Clock()

	# Simply to generate bounding rects for each image
	add_waypoint_rect = display.blit(plus_button, (0, 0))
	del_waypoint_rect = display.blit(trash_can, (0, 42))

	CRASHED = False
	waypoints_info = []

	# If modifying existing path
	if existing_waypoints:
		origin_coords = existing_waypoints[1]

		if existing_waypoints[0] == 'Red':
			background = pygame.transform.rotate(background, 180)

		for i, encapsulated in enumerate(existing_waypoints[0]):
			new_waypoint = Waypoint(i, xy = [encapsulated[0], encapsulated[1]])
			waypoints_info.append(new_waypoint)
		reset(waypoints_info, [origin_coords[0] * -1, origin_coords[1] * -1])
		for waypnt in waypoints_info:
			waypnt.set_endpoint([waypnt.coords[0] + waypnt.radius, waypnt.coords[1]])
	
	# If creating a new path
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

		# Draws the delete button, add waypoint button, and bakckground image, initializes mouse bounding rect
		display.blit(background, (0, 0))
		display.blit(plus_button, (0, 0))
		display.blit(trash_can, (0, 42))
		mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))

		if len(waypoints_info) > 1:
			# Draws the waypoints and the lines between each waypoint.
			rad = waypoints_info[0].radius
			for i in range(1, len(waypoints_info)):
				pygame.draw.line(display, (255, 165, 0), waypoints_info[i-1].coords, waypoints_info[i].coords)
				
				# Draw waypoints
				waypoints_info[i-1].draw(display)
				waypoints_info[i].draw(display)

				dist_x = waypoints_info[i].coords[0] - waypoints_info[i-1].coords[0]
				dist_y = (waypoints_info[i].coords[1] - waypoints_info[i-1].coords[1])

				dist_waypnts = math.hypot(dist_x, dist_y)

				angle_x = dist_x * rad/dist_waypnts
				angle_y = dist_y * rad/dist_waypnts

				waypoints_info[i-1].set_endpoint([waypoints_info[i-1].coords[0] + angle_x, waypoints_info[i-1].coords[1] + angle_y])
				
			waypoints_info[0].draw(display, (0, 255, 0)) # Start waypoint
			waypoints_info[-1].draw(display, (255, 0, 0)) # End waypoint
		else:
			waypoints_info[0].draw(display) # so that it doesn't draw the first one as green all the time
 		
 		# draw the "selected circle" circle
		if selected_waypoint != None:
				pygame.draw.circle(display, (255, 165, 0), selected_waypoint.coords, selected_waypoint.radius + 1, 1)
		
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

	encapsulated_info = write_to_dict(waypoints_info)
	
	# Resets coordinates for next time
	origin_coords = [encapsulated_info[1][0] * -1, encapsulated_info[1][1] * -1]
	reset(waypoints_info, origin_coords)

	pygame.quit()
	return encapsulated_info