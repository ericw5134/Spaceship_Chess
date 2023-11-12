from menus import button
import pygame

from modules.logic import dice
# dice inherits the button class 
# added features for updating the image based on the RNG
class DiceButton(button.Button):
        def __init__(self, x, y, image, scale):
                super().__init__(x, y, image, scale)
                self.value = 0
                self.images = {}
                self.renderedImages = {}

        # put images into a dictionary 
        def assign_image(self, key, object):
                self.images.update({key:object})
        
        # process images into something drawable
        def render_images(self):
                for i in self.images:
                        rendered_image = pygame.transform.scale(self.images.get(i), 
                                                                (int(self.width * self.scale), 
                                                                 int(self.height * self.scale)))
                        self.renderedImages.update({i:rendered_image})
        
        
        def update_image(self, surface):
                try:
                        surface.blit(self.image, (self.rect.x, self.rect.y))
                except:
                        pass

        
        def update_image(self, surface, index):
                self.image = self.renderedImages.get(index, IndexError)
               