import pygame

#button class
class Button():
	def __init__(self, x, y, image, scale):
		self.scale = scale
		self.width = image.get_width()
		self.height = image.get_height()
		self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
	
	def is_clicked(self):
		return self.clicked
	def toggle_clicked(self):
		self.clicked = not self.clicked

	def draw(self, surface):

		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):	
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:	# left click
				self.clicked = True
				action = True
			elif pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False 
		#draw button on screen
		try:
			surface.blit(self.image, (self.rect.x, self.rect.y))
		except:
			pass
		return self.clicked

