class Bullet:
    def __init__(self):
        self.name = ""
        self.color = "Red"
        self.x = 0
        self.y = 0
        self.speed = 0

    def disp(self):
        print(f"Bullet Name: {self.name}")
        print(f"Color: {self.color}")
        print(f"Position: {self.x},{self.y}")
        print(f"Speed: {self.speed}")

bulletStatCount = 5
def loadBullets(file):
    bullets = []
    lines=file.readlines()
    for index,line in enumerate(lines):
        if line == '':
            break
        if index%bulletStatCount == 0:
            currentBullet = Bullet()
            currentBullet.name = line[line.find("=")+1: len(line)-1]
        elif index%bulletStatCount == 1:
            currentBullet.color = line[line.find("=")+1: len(line)-1]
        elif index%bulletStatCount == 2:
            currentBullet.x = float(line[line.find("=")+1: len(line)])
        elif index%bulletStatCount == 3:
            currentBullet.y = float(line[line.find("=")+1: len(line)])
        elif index%bulletStatCount == 4:
            currentBullet.speed = float(line[line.find("=")+1: len(line)])

            bullets.append(currentBullet)

    return bullets


test = open("test.txt","r")
bullets = loadBullets(test)
for bullet in bullets:
    bullet.disp()
