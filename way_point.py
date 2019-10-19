import pygame
# A class representing a Waypoint object to be stored in a list of values
class Waypoint:
	white = (255, 255, 255)
	orange = (255, 165, 0)
	coords = [0, 0]
	id_num = 0
	rot = 0
	radius = 7
	bounding_rect = None
	angle_rect = None
	def __init__(self, id = 0, xy = [151, 145], rotation = 0):
		self.coords = xy
		self.id_num = id
		self.rot = rotation
		self.bounding_rect = pygame.Rect(xy[0] - self.radius, xy[1] - self.radius, self.radius * 2, self.radius * 2)

	def update_coords(self, new_xy):
		self.coords = new_xy
		self.bounding_rect.x = new_xy[0] - self.radius
		self.bounding_rect.y = new_xy[1] - self.radius

	def update_rot(self, rotation):
		self.rot = rotation

	def draw(self, surface, other_color=None):
		if other_color:
			self.bounding_rect = pygame.draw.circle(surface, other_color, tuple(self.coords), self.radius)
		else:
			self.bounding_rect = pygame.draw.circle(surface, self.white, tuple(self.coords), self.radius)

	def draw_line(self, surface, line_endpt):
		self.angle_rect = pygame.draw.line(surface, self.orange, tuple(self.coords), line_endpt, 2)
		print(self.angle_rect)

	def transpose(self, transpose_coords):
		self.coords[0] -= transpose_coords[0]
		self.coords[1] -= transpose_coords[1]
		self.bounding_rect.x = self.coords[0] - self.radius
		self.bounding_rect.y = self.coords[1] - self.radius

	def encapsulate(self):
		return [self.coords[0], self.coords[1], self.rot]

