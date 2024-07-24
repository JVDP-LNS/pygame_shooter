import math

import pygame.sprite
import settings

settingsObj = settings.settings
sharedLists = settings.sharedLists

defaultSurface = pygame.Surface((20,10))
defaultSurface.fill("White")
bounds = settingsObj.getMainWindowDimensions()


class GameObjects(pygame.sprite.Sprite):
    def __init__(self, img = None):
        super().__init__()
        if img:
            self.image = pygame.image.load(img).convert_alpha()
            self.imageTemplate = pygame.image.load(img).convert_alpha()
        else:
            self.image = defaultSurface
            self.imageTemplate = defaultSurface
        self.x = 0.0
        self.y = 0.0
        self.rect = self.image.get_rect(topleft=(0, 0))

    def setPosition(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect.center = pos

    def getPosition(self):
        return self.rect.center


class Player(GameObjects):
    def __init__(self, path):
        super().__init__(path)
        self.ySpeed = 0.0
        self.moveSpeed = 5.0
        self.jumpSpeed = 10.0
        self.gravity = 0.5
        self.weapon = None

    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.x -= int(self.moveSpeed)
            self.rect.x = self.x
        if keys[pygame.K_d] and self.rect.right < bounds[0]:
            self.x += int(self.moveSpeed)
            self.rect.x = self.x
        if keys[pygame.K_w] and self.rect.bottom == bounds[1]:
            self.ySpeed = -self.jumpSpeed
        if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            self.weapon.fire()

    def setSpeedOne(self, speed):
        self.speed = speed

    def getSpeedOne(self):
        return self.speed

    def handleGravity(self):
        self.ySpeed += self.gravity
        self.y += self.ySpeed
        self.rect.centery = int(self.y)
        if self.rect.bottom > bounds[1]:
            self.rect.bottom = bounds[1]
            self.y = self.rect.centery
            self.ySpeed = 0

    def setWeapon(self, weapon):
        self.weapon = weapon

    def update(self):
        self.playerInput()

        self.handleGravity()

        self.weapon.setPosition(self.rect.center)


class Weapon(GameObjects):
    def __init__(self, img, bulletGroup):
        super().__init__(img)
        self.angle = 0.0
        self.bullet = None
        self.firerate: float = 20.0/60  # framerate
        self.cooldown: int = 0
        self.bulletGroup = bulletGroup

    def setFirerate(self,firerate):
        self.firerate = firerate

    def getFirerate(self):
        return self.firerate

    def setBullet(self, bullet):
        self.bullet = bullet

    def fire(self):
        if self.cooldown > 1:
            self.cooldown = 0
            spawnedBullet = self.bullet.spawn(self.angle)
            xPos = self.x - self.image.get_width() * math.cos(self.angle) / 2
            yPos = self.y + self.image.get_width() * math.sin(self.angle) / 2
            spawnedBullet.setPosition([xPos,yPos])
            self.bulletGroup.add(spawnedBullet)

    def setAngle(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotozoom(self.imageTemplate, math.degrees(angle)+180,1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.cooldown += self.firerate
        mousePos = pygame.mouse.get_pos()
        dx = self.rect.centerx - mousePos[0]
        dy = self.rect.centery - mousePos[1]
        angle = math.atan2(-dy,dx)
        self.setAngle(angle)


class Bullet(GameObjects):
    def __init__(self, img = None, image = None):

        super().__init__(img)
        if image:
            self.image = image
            self.rect = self.image.get_rect(topleft=(0,0))
        self.angle = 0

        self.speed = 10.0
        self.xSpeed = 0.0
        self.ySpeed = 0.0
        self.damage = 1.0

    def setDamage(self, dmg):
        self.damage = dmg

    def getDamage(self):
        return float(self.damage)

    def setAngle(self, angle):
        self.angle = angle % 360
        self.image = pygame.transform.rotozoom(self.image, math.degrees(angle)+180, 1)
        self.xSpeed = -self.speed * math.cos(angle)
        self.ySpeed = self.speed * math.sin(angle)

    def getAngle(self):
        return self.angle

    def setSpeedOne(self, speed):
        self.speed = speed

    def getSpeedOne(self):
        return self.speed

    def setSpeedTwo(self, speeds):
        self.xSpeed = speeds[1]
        self.ySpeed = speeds[2]

    def getSpeedTwo(self):
        return [self.xSpeed, self.ySpeed]

    def updatePosition(self):
        self.x += self.xSpeed
        self.y += self.ySpeed
        self.rect.center = [self.x,self.y]

    def spawn(self,angle):
        bullet = Bullet(None, self.image)
        bullet.setSpeedOne(self.speed)
        bullet.setAngle(angle)
        return bullet

    def moveBullet(self):
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed

    def destroy(self):
        if(self.rect.left > bounds[0]) or (self.rect.right < 0) or (self.rect.top > bounds[1]) or (self.rect.bottom < 0):
            self.kill()

    def update(self):
        self.updatePosition()
        self.destroy()

class Enemy(GameObjects):
    def __init__(self):
        img = "Sprites/player.png"
        super().__init__(img)
        self.hp = 100

    def takeDamage(self, bullet: Bullet):
        self.hp -= bullet.getDamage()

    def checkCollision(self):
        bulletCollisionList = pygame.sprite.spritecollide(self, sharedLists.getBulletGroup("Bullet"), False)
        for bullet in bulletCollisionList:
            self.takeDamage(bullet)
            bullet.kill()
            print("yeah")

    def update(self):
        self.checkCollision()
        if self.hp <= 0:
            self.kill()
