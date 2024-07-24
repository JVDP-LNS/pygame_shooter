import pygame.image

class BG:
    def __init__(self, bg: str):
        print(bg)
        self.backgroundImageTemplate = pygame.image.load(bg).convert_alpha()
        self.backgroundImage = self.backgroundImageTemplate

    def setBGSize(self,size: tuple):
        self.backgroundImage = pygame.transform.scale(self.backgroundImageTemplate,size)

    def showBG(self):
        window = pygame.display.get_surface()
        window.blit(self.backgroundImage, (0, 0))
        return
