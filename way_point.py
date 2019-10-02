import pygame
# A class representing a Waypoint object to be stored in a list of values
class Waypoint:
	white = (255, 255, 255)
	orange = ()
	coords = [0, 0]
	id_num = 0
	rot = 0
	bounding_rect = None
	radius = 7
	def __init__(self, id = 0, xy = [151, 145], rotation = 0):
		self.coords = xy
		self.id_num = id
		self.rot = rotation
	def update_coords(self, new_xy):
		self.coords = new_xy

	def set_rot(self, rotation):
		self.rot = rotation

	def bounding_rect(self, surface):
		self.bounding_rect = pygame.draw.circle(surface, self.white, tuple(self.coords), self.radius)
		return self.bounding_rect

	def draw(self, surface, other_color=None):
		if other_color:
			pygame.draw.circle(surface, other_color, tuple(self.coords), self.radius)
		else:
			pygame.draw.circle(surface, self.white, tuple(self.coords), self.radius)

	def encapsulate(self):
		return [self.coords[0], self.coords[1], self.rot]

