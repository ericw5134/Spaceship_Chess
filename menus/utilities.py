def settings():
	game_window.fill("black")

def create_main_menu(window):
	#background image
	background = pygame.image.load('./assets/images/menu_bg.png').convert_alpha()
	screen = pygame.Surface(window.get_size())
	screen_width = screen.get_width();
	screen_height = screen.get_height();
	pygame.draw.rect(screen, (255,255,255),(0, 0, screen_width, screen_height))

	menu_container = Container(
								screen,
								(0.2, 0.08, 0.6, 0.85),
								(
									screen.get_rect().x,
									screen.get_rect().y,
									screen_width,
									screen_height
								)
							)
	
	menu_container.draw(screen)
	submenu_container = Container(screen, 
									(0.075, 0.02, 0.85, 0.9),
									(
									menu_container.get_x(),
									menu_container.get_y(),
									menu_container.get_width(),
									menu_container.get_height()
									)
								)
	#submenu_container.draw(screen)
	background = pygame.transform.scale(background, window.get_size())
	screen.blit(background, (0,0))
	screen.fill((0,40,200), (menu_container.get_x(), menu_container.get_y(), menu_container.get_width(), menu_container.get_height()))
	button_height_percent = 0.13
	button_vertical_height_buffer = 0.02
	play_button = RectangularButton(screen, (
								(submenu_container.get_x()/screen_width + submenu_container.get_width()/screen_width * 0.1), 
								(submenu_container.get_y()/screen_height + submenu_container.get_height()/screen_height * 0.45),
								round(submenu_container.get_width()*0.8),
								round(submenu_container.get_height()*button_height_percent)
								),
								(190,180, 90),
								"Play"
						)
	play_button.draw(screen)

	settings_button = RectangularButton(screen, ((submenu_container.get_x()/screen_width + submenu_container.get_width()/screen_width*0.1), 
								(submenu_container.get_y()/screen_height + submenu_container.get_y()/screen_height + submenu_container.get_height()/screen_height * 0.45 + button_vertical_height_buffer),
								round(submenu_container.get_width()*0.8),
								round(submenu_container.get_height())*button_height_percent),
								(190,180, 90),
								"Settings"
						)
	settings_button.draw(screen)

	quit_button =RectangularButton(screen, ((submenu_container.get_x()/screen_width + submenu_container.get_width()/screen_width*0.1), 
								(2*submenu_container.get_y()/screen_height + submenu_container.get_y()/screen_height + submenu_container.get_height()/screen_height * 0.45 + 2*button_vertical_height_buffer),
								round(submenu_container.get_width()*0.8),
								round(submenu_container.get_height())*button_height_percent),
								(190,180, 90),
								"Quit"
						)
	quit_button.draw(screen)

	logo_container = Container(screen,
							(0, 0, 1, 0.4),
							(
							submenu_container.get_x(),
							submenu_container.get_y(),
							submenu_container.get_width(),
							submenu_container.get_height()
							)
							)
	#logo_container.draw(screen)
	logo = RectangularButton(screen,
							(
								logo_container.get_x()/screen_width,
								logo_container.get_y()/screen_height,
								logo_container.get_width(),
								logo_container.get_height()
							),
							(0,0,0),
							"Aeroplane Chess"
							)
	logo.draw(screen)

	window.blit(screen, (0,0))
	pygame.display.flip()

def main_menu(window):
	create_main_menu(window)
	#loop var
	run = True
	while run:	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.VIDEORESIZE:
				create_main_menu(window)

# position is for a 4-tuple (x,y,a,b)
# x, y relative to the frame from 0-1
# a is the relative width %
# b is the relative height %
# offset is a tuple (x, y) corresponding to the offset of each in percent
# second tuple is for the object it wants to fit in
class Container():
	def __init__(self, frame, position, container):
		self.x_offset = position[0]
		self.y_offset = position[1]
		self.width_percent = position[2]
		self.height_percent = position[3]
		self.resize(frame, position, container)

	def get_x(self):
		return self.x_location
	def get_y(self):
		return self.y_location
	def get_width(self):
		return self.x_percent
	def get_height(self):
		return self.y_percent

	def resize(self, frame, position, container):
		self.x_location = container[0] + container[2] * self.x_offset
		self.y_location = container[1] + container[3] * self.y_offset
		frame_width = container[2]
		frame_height = container[3]
		self.x_percent = frame_width * self.width_percent
		self.y_percent = frame_height * self.height_percent
		self.rect = pygame.Rect(self.x_location, self.y_location, self.x_percent, self.y_percent)

	def draw(self, frame):
		pygame.draw.rect(frame, (200,200,200), self.rect, 10)

#Abstract class for button
class Button():
	# position is a 4 tuple (a,b,c,d) 
	# a-> left, b -> top, c-> distance right, d->distance down
		def __init__(self, frame, position, color):
			self.position = position
			self.resize(frame)
			self.color = color

		def resize(self, frame):
			frame_size = frame.get_size()
			x_location = round(self.position[0] * frame_size[0])
			y_location = round(self.position[1] * frame_size[1])

			self.rect = pygame.Rect(x_location, y_location, self.position[2], self.position[3])

		def draw(self, frame):
			pygame.draw.rect(frame, (150, 150, 150) ,self.rect)
			pygame.draw.rect(frame, self.color, self.rect, 5, 3)

class RectangularButton(Button):

	def __init__(self, frame, position, color, text):
		self.text = text
		super().__init__(frame, position, color)

	def resize(self, window):
		super().resize(window)
		# readjust height and width
		width = window.get_size()[0]
		height = window.get_size()[1]

		adjusted_width = round(self.position[2] * width)
		adjusted_height = round(self.position[3] * height)
		font_size = min(int(max(8, round(adjusted_height)/2000)),100)
		font = pygame.font.SysFont("Arial", font_size)
		self.rendered_text = font.render(self.text, 1, (255,255,255))
		self.text_position = self.rendered_text.get_rect(center=self.rect.center)

	def draw(self, frame):
		super().draw(frame)
		frame.blit(self.rendered_text, self.text_position)

class Text:
	
	def __init__(self, frame, position, text, centered, color):
		self.frame = frame
		self.position = position
		self.text = text
		self.centered=centered
		self.color=color
		self.font_size = max(8, round(window.get_height()))
		self.font = pygame.font.SysFont('./assets/typeface/BebasNeue-Regular.ttf', self.font_size)

		position[0] = 0.05
		if(self.centered):
			self.position[0] = frame.get_size()[0]/2
			self.position[1] = frame.get_size()[1]/2

	def draw(self, frame):
		frame.blit(self.text, self.position)