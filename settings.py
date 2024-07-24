import pygame.sprite


class Settings:
    def __init__(self):
        configFile = open("config.txt", "r")
        configs = configFile.readlines()
        self.settings = []
        temp_numericConfigCOunt = int(configs[0][configs[0].find("=") + 2: len(configs[0])]) # obtain number of numeric configs for the following loop
        for index, currentConfig in enumerate(configs):
            if index > temp_numericConfigCOunt:  # handling string configs
                currentValue = str(currentConfig[currentConfig.find("=") + 2: len(currentConfig)-1])
                self.settings.append(currentValue)
            else:# handling numeric configs
                currentValue = int(currentConfig[currentConfig.find("=") + 2: len(currentConfig)])
                self.settings.append(currentValue)

    def getMainWindowDimensions(self):
        return (self.settings[1],self.settings[2])
    def updateMainWindowDimensions(self, newSize: tuple):
        self.settings[1] = newSize[0]
        self.settings[2] = newSize[1]

    def getFPS(self):
        return self.settings[3]

    def getBackgroundImage(self):
        return self.settings[self.settings[0]+1]

    def getPlayerImage(self):
        return self.settings[self.settings[0]+2]

    def getWeaponImage(self):
        return self.settings[self.settings[0]+3]

    def getBulletImage(self):
        return self.settings[self.settings[0]+4]


class SharedLists:
    def __init__(self):
        self.bulletGroups = {}
        self.playerGroups = {}
        self.enemyGroups = {}

    def addBulletGroup(self, groupName: str, group: pygame.sprite.Group):
        self.bulletGroups[groupName] = group

    def getBulletGroup(self, groupName):
        return self.bulletGroups[groupName]

    def addPlayerGroup(self, groupName: str, group: pygame.sprite.Group):
        self.playerGroups[groupName] = group

    def getPlayerGroup(self, groupName):
        return self.playerGroups[groupName]

    def addEnemyGroup(self, groupName: str, group: pygame.sprite.Group):
        self.enemyGroups[groupName] = group

    def getEnemyGroup(self, groupName):
        return self.enemyGroups[groupName]


settings = Settings()
sharedLists = SharedLists()
