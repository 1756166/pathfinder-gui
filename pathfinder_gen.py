import pygame, csv
from way_point import Waypoint

def transpose(waypoints_info):
	pass

''' -- FRC STANDARD FIELD DIMENSIONS -- 
 		27 ft 7 in X 54 ft 1 in
 		scale accordingly
'''
pygame.init()

background = pygame.image.load('Resources\\game_image.jpg')
background = pygame.transform.scale(background, (background.get_width() * 2, background.get_height() * 2))
dimensions = (background.get_width(), background.get_height())

plus_button = pygame.image.load('Resources\\add_waypoint.jpg')
plus_button = pygame.transform.scale(plus_button, (42, 42)) # NICE
trash_can = pygame.image.load('Resources\\remove_waypoint.jpg')
trash_can = pygame.transform.scale(trash_can, (42, 42)) # VERY NICE


display = pygame.display.set_mode(dimensions)
pygame.display.set_caption('Generate Waypoints')
clock = pygame.time.Clock()

add_waypoint_rect = display.blit(plus_button, (0, 0))
del_waypoint_rect = display.blit(trash_can, (background.get_width() - 42, 0))

CRASHED = False

waypoint = Waypoint() # Default constructor
waypoints_info = [(waypoint, waypoint.bounding_rect(display))]
id = len(waypoints_info) - 1

init_x, init_y = 10, 50

selected_waypoint = None

while not CRASHED:
	clock.tick(60)
	# Draws the delete button, add waypoint button, and bakckground image.
	display.blit(background, (0, 0))
	display.blit(plus_button, (0, 0))
	display.blit(trash_can, (background.get_width() - 42, 0))

	mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))

	for waypnt, bounding_rect in waypoints_info:
		waypnt.draw(display)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			CRASHED = True

		if event.type == pygame.MOUSEBUTTONDOWN:
			if add_waypoint_rect.contains(mouse_rect): # if the plus button is pressed
				# add a new waypoint to array, which will then be drawn
				id += 1
				new_waypoint = Waypoint(id, [init_x, init_y])
				waypoints_info.append((new_waypoint, new_waypoint.bounding_rect(display)))
				init_y += 12
			if del_waypoint_rect.contains(mouse_rect): # if delete waypoint button is pressed
				# delete last waypoint
				if selected_waypoint is waypoints_info[-1]:
					selected_waypoint = None
				id -= 1
				init_y -= 12
				waypoints_info.pop(-1) # Deletes last elem in list of waypoints

			for waypnt, bounding_rect in waypoints_info: # Allows you to select other waypoints
				if bounding_rect.contains(mouse_rect):
					selected_waypoint = [waypnt, bounding_rect]

		if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1: # if mouse is dragged
			if not add_waypoint_rect.contains(mouse_rect) and not del_waypoint_rect.contains(mouse_rect):	
				if selected_waypoint != None:
					selected_waypoint[0].update_coords(list(pygame.mouse.get_pos()))
					# Updates the waypoint coords 
					selected_waypoint[1].x = selected_waypoint[0].coords[0] - 7
					selected_waypoint[1].y = selected_waypoint[0].coords[1] - 7

		pygame.display.update()


pygame.quit()
quit()