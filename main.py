import pygame # type: ignore
import settings
from background import BG
from sys import exit
import gameobjects

pygame.init()

settingsObj = settings.settings
sharedListsObj = settings.sharedLists

mainWindowDimensions = settingsObj.getMainWindowDimensions()
fullScreen = False
mainWindow = pygame.display.set_mode(mainWindowDimensions,pygame.RESIZABLE)
pygame.display.set_caption("Shooter")

fps = settingsObj.getFPS()

background = BG(settingsObj.getBackgroundImage())

player = gameobjects.Player(settingsObj.getPlayerImage())
playerGroup = pygame.sprite.Group(player)
sharedListsObj.addBulletGroup("Player",playerGroup)

bulletGroup = pygame.sprite.Group()
sharedListsObj.addBulletGroup("Bullet",bulletGroup)
weapon = gameobjects.Weapon(settingsObj.getWeaponImage(), bulletGroup)
bullet = gameobjects.Bullet(settingsObj.getBulletImage())
weapon.setBullet(bullet)
player.setWeapon(weapon)

playerGroup.add(weapon)

enemyNumber = 5
enemyGroup = pygame.sprite.Group()
sharedListsObj.addEnemyGroup("Enemy",enemyGroup)
for i in range(enemyNumber):
    enemy = gameobjects.Enemy()
    enemy.setPosition([1000*(1 - i/10),400])
    enemyGroup.add(enemy)


clock = pygame.time.Clock()

gameActive = False

def updateScreenSize():
    mainWindowDimensions = mainWindow.get_size()
    background.setBGSize(mainWindowDimensions)

while True:
    # Event Loop
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
        if (e.type == pygame.KEYDOWN) and (pygame.key.get_pressed()[pygame.K_F11]):
            if fullScreen:
                mainWindow = pygame.display.set_mode(mainWindowDimensions,pygame.RESIZABLE)
                fullScreen = False
            else:
                mainWindow = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
                fullScreen = True

            updateScreenSize()
            settingsObj.updateMainWindowDimensions(mainWindowDimensions)

    # mainWindow.fill((61,61,61))
    background.showBG()

    playerGroup.update()
    playerGroup.draw(mainWindow)

    bulletGroup.update()
    bulletGroup.draw(mainWindow)

    enemyGroup.update()
    enemyGroup.draw(mainWindow)

    pygame.display.update()
    clock.tick(fps)
