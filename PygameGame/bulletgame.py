import pygame, sys, time, random
from pygame.locals import *

pygame.init()

FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

text = pygame.font.SysFont('Comic Sans MS', 30)

DISPLAYSURF = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('Mizhou Episode 0.5')

gameState = 0

######################################################
# SPRITES AND GAME ASSETS
######################################################
def ezload(img):
    return pygame.image.load(f'PygameGame/{img}')
#===========PLAYER============
jiangSprite = ezload('player.png')
playerHitbox = ezload('playerHitbox.png')
focusBagua = ezload('baguaFocus.png')
focusSpear = ezload('spearFocus.png')
pygame.Surface.set_alpha(focusBagua, 110)
pygame.Surface.set_alpha(focusSpear, 110)

#===========Bullets============
basicPlayerBullet = ezload('sealBullet.png')
basicBullet = ezload('bullet.png')
yellowbullet = ezload('yellowBullet.png')
yellowbeam = ezload('yellowBeam.png')


pygame.Surface.set_alpha(basicPlayerBullet, 185)

#===========BOSSES============
qiSprite = ezload('qiBoss.png')

#===========MUSIC============
MUSIC = pygame.mixer.music
MUSIC.load('PygameGame/QiTheme.mp3')
MUSIC.play()
MUSIC.set_volume(0.5)



######################################################
# PLAYER CODE & setup
######################################################
playerSprite = jiangSprite
playerX = 500
playerY = 500
playerSpeed = 5
focusBaguaRotation = 0
playerBullets = []
bulletCooldown = 4

# Setup =====================
enemyBullets = []

######################################################
# GRAPHIC FUNCTIONS IN MAIN GAMEzz
######################################################
def displayIMGPlayer(img):
    DISPLAYSURF.blit(img, (playerX - img.get_width()/2, playerY - img.get_height()/2))

def updateGraphics():
    #==========================
    # Enemies
    #==========================
    #bullets
    for bullet in enemyBullets:
        bullet.move()
        bullet.render()
        bulletDestroyed = bullet.destroy()
        if bulletDestroyed[0]:
            for bulletNewID in enemyBullets[bulletDestroyed[1]:]:
                bulletNewID.index = bulletNewID.index-1

    # Boss ==========================
    boss.render()
    
    #==========================
    # Player
    #==========================
    #bullets
    for bullet in playerBullets:
        bullet.move()
        bullet.render()
        bulletDestroyed = bullet.destroy()
        if bulletDestroyed[0]:
            for bulletNewID in playerBullets[bulletDestroyed[1]:]:
                bulletNewID.index = bulletNewID.index-1
    if focus == True:
        displayIMGPlayer(pygame.transform.rotate(focusBagua, focusBaguaRotation))
        displayIMGPlayer(pygame.transform.rotate(focusSpear, 0-focusBaguaRotation))
    displayIMGPlayer(playerSprite)
    if focus == True:
        displayIMGPlayer(playerHitbox)



######################################################
# CLASSES & EXTRA FUNCTIONS
######################################################
class PlayerBullet:
    def __init__(self, typeBullet, playerPos, velocity, index):
        self.typeBullet = typeBullet
        self.position = playerPos
        self.velocity = velocity
        self.index = index
    
    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
    
    def render(self):
        if self.typeBullet == "basic":
            self.selfDraw(basicPlayerBullet)
        else:
            self.selfDraw(basicPlayerBullet)
    def selfDraw(self, img):
        DISPLAYSURF.blit(img, (self.position[0] - img.get_width()/2, self.position[1] - img.get_height()/2))

    def destroy(self):
        if self.position[1] < -10:
            playerBullets.pop(self.index)
            return (True, self.index)
        else:
            return (False, self.index)

class EnemyBullet:
    def __init__(self, typeBullet, startPos, velocity, index):
        self.typeBullet = typeBullet
        self.position = startPos
        self.velocity = velocity
        self.index = index
    
    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        if self.position[1] < 100 and self.typeBullet == "yellowAccelerate":
            self.velocity[1] += 0.1
        elif 140 <= self.position[1] < 150 and self.typeBullet == "yellowAccelerate" and self.velocity[0] == 0:
            self.velocity[0] = random.randint(-4, 4)
            self.velocity[1] -= random.randrange(4, 6)
        elif self.position[1] < 200 and self.typeBullet == "yellowAccelerate":
            self.velocity[1] += 0.1
    
    def render(self):
        if self.typeBullet == "basic":
            self.selfDraw(basicBullet)
        elif self.typeBullet == "yellowbasic" or self.typeBullet == "yellowAccelerate":
            self.selfDraw(yellowbullet)
        elif self.typeBullet == "yellowbeam":
            self.selfDraw(yellowbeam)
        else:
            self.selfDraw(basicBullet)
    def selfDraw(self, img):
        DISPLAYSURF.blit(img, (self.position[0] - img.get_width()/2, self.position[1] - img.get_height()/2))

    def destroy(self):
        if self.position[1] > 1010:
            enemyBullets.pop(self.index)
            return (True, self.index)
        else:
            return (False, self.index)
    
class Boss:
    def __init__(self, level):
        self.level = level
        self.position = [500, 120]
        self.velocity = [0,0]
        self.health = 999
        self.maxV = [10,10]
        if self.level == 2:
            self.health = 200
                
    def move(self):
        if self.velocity[0] > self.maxV[0]:
            self.velocity[0] = self.maxV[0]
        elif self.velocity[0] < -(self.maxV[0]):
            self.velocity[0] = self.maxV[0]
            
        if self.velocity[1] > self.maxV[1]:
            self.velocity[1] = self.maxV[1]
        elif self.velocity[1] < -(self.maxV[1]):
            self.velocity[1] = self.maxV[1]
            
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
    
    def gotoPos(self, target, pos, vel, ogPos, steps):
        distanceX = target - ogPos
        currentDistX = target - pos
        if pos[0] < target[0]: 
            if  target[0] - pos[0] <  (target[0] - ogPos[0])/2:
                vel[0] += 1
            else:
                vel[0] -= 2
        elif pos[0] > target[0]: 
            vel[0] -= 1
            if target[0] - pos[0] < (target[0] - ogPos[0])/2:
                vel[0] -= 1
            else:
                vel[0] += 2
        else:
            vel[0] = 0
            
        if pos[1] < target[1]:
            if target[1] - pos[1] < (target[1] - ogPos[1])/2:
                vel[1] += 1
            else:
                vel[1] -= 1
        elif pos[1] > target[1]: 
            if target[1] - pos[1] < (target[1] - ogPos[1])/2:
                vel[1] -= 1
            else:
                vel[1] += 1
        else:
            vel[1] = 0      
        print(f"{vel[0]=};{pos[0]=};{target[0]=};{ogPos[0]=}")
        if vel[0] > 10:
            vel[0] = 10
        elif vel[0] < -10:
            vel[0] = -10
        
        return vel
        
    def render(self):
        if self.level == 2:
            self.selfDraw(qiSprite)
        
    def selfDraw(self, img):
        DISPLAYSURF.blit(img, (self.position[0] - img.get_width()/2, self.position[1] - img.get_height()/2))
        
    #==========================
    # Boss Special Attacks
    #==========================
    def bossAttack(self, boss, special):
        if boss == 2:
            if special == 0:
                self.addBullet("yellowbasic", self.position[:], [0,5])
                self.addBullet("yellowbasic", self.position[:], [1.5,4.5])
                self.addBullet("yellowbasic", self.position[:], [2.5,4])
                self.addBullet("yellowbasic", self.position[:], [-2.5,4])
                self.addBullet("yellowbasic", self.position[:], [-1.5,4.5])
                self.addBullet("yellowbasic", self.position[:], [3,3])
                self.addBullet("yellowbasic", self.position[:], [-3,3])
            if special == 1:
                for i in range(2):
                    self.addBullet("yellowAccelerate", [700, -40], [0,0])
                    self.addBullet("yellowAccelerate", [300, -40], [0,0])
    
    def addBullet(self, btype,pos,vel):
        enemyBullets.append(EnemyBullet(btype, pos, vel, len(enemyBullets)))

#==========================
# Setup
#==========================
boss = Boss(2)
######################################################
# EXTRA FUNCTIONS
######################################################

def menuGetColour(id):
    if menuSelect == id:
        return (255,255,0)
    else: 
       return (255,255,255)

######################################################
# MAIN GAME LOOP
######################################################
bulletCooldownTimer = 10
bossbulletCooldownTimer = 0
bosscdthreshold = 10
numBossattacks = 0
menuSelect = 0
inputCooldown = 10
while True:
    keys = pygame.key.get_pressed()
    match gameState:
        case 0: # Main menu
            DISPLAYSURF.fill((0,0,0))
            if inputCooldown == 10:
                if keys[K_UP]:
                    if menuSelect > 0:
                        menuSelect -= 1
                    else:
                        menuSelect = 3
                    inputCooldown = 0
                elif keys[K_DOWN]:    
                    if menuSelect < 3:
                        menuSelect += 1
                    else:
                        menuSelect = 0
                    inputCooldown = 0
                if keys[K_z]:
                    if menuSelect == 0:
                        gameState = 1
            
            menutext = ["Story", "Options", "Music Room", "Exit"]
            for textNum in range(len(menutext)):
                textDisplay = text.render(menutext[textNum], False, menuGetColour(textNum))
                DISPLAYSURF.blit(textDisplay, (700,300+textNum*100))
                
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
            if inputCooldown < 10:
                inputCooldown += 1
            
        case 1: #main gameply
            DISPLAYSURF.fill((0,0,0))

            
            
            if keys[K_LEFT]:
                    playerX -= playerSpeed
            elif keys[K_RIGHT]:   
                    playerX += playerSpeed
            if keys[K_UP]:
                    playerY -= playerSpeed
            elif keys[K_DOWN]:    
                    playerY += playerSpeed
            if keys[K_LSHIFT] or keys[K_LCTRL]:
                focus = True
                playerSpeed = 3
                if focusBaguaRotation <= 360:
                    focusBaguaRotation += 1
                else: 
                    focusBaguaRotation = 0
            else:
                focus = False
                playerSpeed = 6

            if keys[K_z]:
                if bulletCooldownTimer >= bulletCooldown:
                    playerBullets.append(PlayerBullet("basic", [playerX+15, playerY], [0, -25], len(playerBullets)))
                    playerBullets.append(PlayerBullet("basic", [playerX-15, playerY], [0, -25], len(playerBullets)))
                    bulletCooldownTimer = 0


            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()





            #==========================
            # Boss Loop
            #==========================
            if bossbulletCooldownTimer == bosscdthreshold:
                #Moving=================
                if 120 < numBossattacks < 130:
                    boss.velocity[0] -= 1
                elif 140 < numBossattacks < 150:
                    boss.velocity[0] += 1 

                elif 170 < numBossattacks < 180:
                    boss.velocity[0] += 1
                elif 200 < numBossattacks < 210:
                    boss.velocity[0] -= 1 

                #left right left
                elif 230 < numBossattacks < 240:
                    boss.velocity[0] -= 1
                elif 260 < numBossattacks < 270:
                    boss.velocity[0] += 1 

                elif 290 < numBossattacks < 300:
                    boss.velocity[0] += 1
                elif 320 < numBossattacks < 330:
                    boss.velocity[0] -= 1 

                elif 350 < numBossattacks < 360:
                    boss.velocity[0] -= 1
                elif 380 < numBossattacks < 390:
                    boss.velocity[0] += 1 

                #back to centre
                elif 410 < numBossattacks < 420:
                    boss.velocity[0] += 1
                elif 437 < numBossattacks < 447:
                    boss.velocity[0] -= 1 

                #Shooting===============
                if numBossattacks % 40 < 5 and numBossattacks < 447:
                    boss.bossAttack(2,0)
                    bossbulletCooldownTimer = 0

                elif numBossattacks and 447 < numBossattacks < 999:
                    boss.bossAttack(2,1)
                    bossbulletCooldownTimer = 0 


                numBossattacks +=1
            boss.move()
            #==========================
            # Per Loop Updates
            #==========================
            if bulletCooldownTimer < 10:
                bulletCooldownTimer += 1
            if bossbulletCooldownTimer < bosscdthreshold:
                bossbulletCooldownTimer += 1
            updateGraphics()
    pygame.display.update()
    fpsClock.tick(FPS)