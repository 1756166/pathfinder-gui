import pygame, pygame.draw as draw, math
# A class representing a Waypoint object to be stored in a list of values
class Waypoint:

	white = (255, 255, 255)
	orange = (255, 165, 0)
	coords = [0, 0]
	id_num = 0
	rot = 0
	radius = 7
	bounding_rect = None
	angle_endpoint = None
	def __init__(self, id = 0, xy = [151, 145]):
		self.coords = xy
		self.id_num = id
		self.bounding_rect = pygame.Rect(xy[0] - self.radius, xy[1] - self.radius, self.radius * 2, self.radius * 2)

	def update_coords(self, new_xy):
		self.coords = new_xy
		self.bounding_rect.x = new_xy[0] - self.radius
		self.bounding_rect.y = new_xy[1] - self.radius
		

	def derive_rot(self):
		dist_x = (self.angle_endpoint[0] - self.coords[0])/self.radius
		dist_y = -1 * (self.angle_endpoint[1] - self.coords[1])/self.radius

		if dist_x > 0 and dist_y > 0:
			self.rot = math.asin(dist_y)
		if dist_x < 0 and dist_y > 0:
			self.rot = math.acos(dist_x)
		if dist_x > 0 and dist_y < 0:
			self.rot = math.asin(dist_y)
		if dist_y < 0 and dist_x < 0: 
			self.rot = math.pi - math.asin(dist_y)


	def set_endpoint(self, endpoint):
		self.angle_endpoint = endpoint

	def draw(self, surface, other_color=None):
		if other_color:
			self.bounding_rect = draw.circle(surface, other_color, tuple(self.coords), self.radius)
		else:
			self.bounding_rect = draw.circle(surface, self.white, tuple(self.coords), self.radius)

	def transpose(self, transpose_coords):
		self.coords[0] -= transpose_coords[0]
		self.coords[1] -= transpose_coords[1]
		self.bounding_rect.x = self.coords[0] - self.radius
		self.bounding_rect.y = self.coords[1] - self.radius

	def encapsulate(self):
		return [self.coords[0], self.coords[1], self.rot]

