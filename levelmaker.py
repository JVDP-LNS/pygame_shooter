import pygame

pygame.init()

levelMakerWindow = pygame.display.set_mode()

levelsFile = open("Levels/levelIndex.txt","r+")
levelCount = 0
levels = []

for index, path in enumerate(levelsFile.readlines()):
    if(index>0) and (path):
        levels.append()

    elif index == 0:
        levelCount = int(path[path.find('=') + 2: len(path) - 1])

print(levelCount)