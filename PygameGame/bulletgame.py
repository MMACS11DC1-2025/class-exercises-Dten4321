import pygame, sys, time, random, math
from pygame.locals import *

pygame.init()

FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

text = pygame.font.SysFont('Times New Roman', 30)

DISPLAYSURF = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('Mizhou Episode 0.5')

gameState = 0

######################################################
# IMAGES AND GAME ASSETS
######################################################
def ezload(img):
    return pygame.image.load(f'PygameGame/{img}')
#===========PLAYER============
jiangSprite = ezload('player.png')
playerHitbox = ezload('playerHitbox.png')
focusBagua = ezload('baguaFocus.png')
focusSpear = ezload('spearFocus.png')
bambooSprite = ezload('Bamboo.png')
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
MUSIC.load('PygameGame/LandOfTheLostFog.mp3')
MUSIC.play()
MUSIC.set_volume(0.5)

# PLAYER CODE & setup=======================

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.playerSprite = jiangSprite
        self.x = 500
        self.y = 500
        self.diameter = 5
        self.playerSpeed = 5
        self.focusBaguaRotation = 0
        self.playerBullets = []
        self.bulletCooldown = 4
        self.rect = Rect(self.x-self.diameter/2, self.y-self.diameter/2, self.diameter,self.diameter) #math.sqrt(self.diameter/2), math.sqrt(self.diameter/2))

# Setup =====================
enemyBullets = []

######################################################
# GRAPHIC FUNCTIONS IN MAIN GAMEzz
######################################################
def displayIMGPlayer(img):
    DISPLAYSURF.blit(img, (player.x - img.get_width()/2, player.y - img.get_height()/2))

def updateGraphics():
    

    # Boss ==========================
    boss.render()
    #pygame.draw.rect(DISPLAYSURF, (0,255,0) , boss.rect)
    
    #==========================
    # Player
    #==========================
    #bullets
    for bullet in player.playerBullets:
        bullet.move()
        bullet.render()
        bulletDestroyed = bullet.destroy()
        if bulletDestroyed[0]:
            for bulletNewID in player.playerBullets[bulletDestroyed[1]:]:
                bulletNewID.index = bulletNewID.index-1
    if focus == True:
        displayIMGPlayer(pygame.transform.rotate(focusBagua, player.focusBaguaRotation))
        displayIMGPlayer(pygame.transform.rotate(focusSpear, 0-player.focusBaguaRotation))
    displayIMGPlayer(player.playerSprite)
    #pygame.draw.rect(DISPLAYSURF, (255,0,255) , player.rect)
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
        pygame.draw.rect(DISPLAYSURF, (255,255,0) , bullet.rect)
    if focus == True:
        displayIMGPlayer(playerHitbox)


######################################################
# CLASSES & EXTRA FUNCTIONS
######################################################

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, typeBullet, playerPos, velocity, index):
        self.typeBullet = typeBullet
        self.position = playerPos
        self.velocity = velocity
        self.index = index
        self.diameter = 12
    
    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
    
    def render(self):
        self.selfDraw(basicPlayerBullet)
    def selfDraw(self, img):
        DISPLAYSURF.blit(img, (self.position[0] - img.get_width()/2, self.position[1] - img.get_height()/2))
    def destroy(self):
        if self.position[1] > 1010:
            player.playerBullets.pop(self.index)
            return (True, self.index)
        else:
            return (False, self.index)

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, typeBullet, startPos, velocity, angle,index):
        self.typeBullet = typeBullet
        self.position = startPos
        self.velocity = velocity
        self.index = index
        self.angle = angle
        
        if self.typeBullet == "basic":
            self.sprite = basicBullet
        elif self.typeBullet in ["yellowbasic", "yellowAccelerate"]:
            self.sprite = yellowbullet
        elif self.typeBullet == "yellowbeam":
            self.sprite = yellowbeam
        elif self.typeBullet == "bamboo":
            self.sprite = bambooSprite
        else:
            self.sprite = basicBullet
        
        if self.typeBullet == "bamboo":
            self.diameter = 28
            self.rect = Rect(self.position[0]-self.diameter/2, self.position[1]-self.diameter/2, self.diameter, self.diameter)
        if self.typeBullet in ["basic","yellowbasic","yellowAccelerate"]:
            self.diameter = 20
            self.rect = Rect(self.position[0]-self.diameter/2, self.position[1]-self.diameter/2, self.diameter, self.diameter)

    
    def move(self):
        self.position[0] += math.cos(math.radians(self.angle))*self.velocity
        self.position[1] += math.sin(math.radians(self.angle))*self.velocity
        #if self.typeBullet in ["basic","yellowbasic","yellowAccelerate", "yellowturn"]:
        self.rect.update([self.position[0]-self.diameter/2, self.position[1]-self.diameter/2], [self.diameter,self.diameter])
        if self.typeBullet == "yellowAccelerate":
            self.velocity += 0.02

    
    def render(self):
        self.selfDraw(self.sprite)
        
    def selfDraw(self, img):
        if self.typeBullet == "bamboo":
            DISPLAYSURF.blit(img, (self.position[0] - img.get_width()/2, self.position[1] - img.get_height()))
        else:
            DISPLAYSURF.blit(img, (self.position[0] - img.get_width()/2, self.position[1] - img.get_height()/2))

    def destroy(self):
        if self.position[1] > 1010 + self.sprite.get_height():
            enemyBullets.pop(self.index)
            return (True, self.index)
        else:
            return (False, self.index)
    
class Boss(pygame.sprite.Sprite):
    def __init__(self, level):
        self.level = level
        self.position = [500, 120]
        self.velocity = 0
        self.health = 999
        self.maxV = [10,10]
        self.diameter = 70
        self.maxSpeed = 5
        self.rect = Rect(self.position[0],self.position[1], 70, 70)
        self.rect.update([self.position[0]-self.diameter/2, self.position[1]-self.diameter/2], [self.diameter,self.diameter])
        if self.level == 2:
            self.health = 200
    
    def gotoPos(self, target, pos, ogPos):
        angleTowards = math.atan2(ogPos[1]-target[1],ogPos[0]-target[0])
        ogDist = math.sqrt((ogPos[0] - target[0])**2 + (ogPos[1] - target[1])**2) #pythagoras to find hypotenuse
        currDist = math.sqrt((pos[0] - target[0])**2 + (pos[1] - target[1])**2) #pythagoras to find hypotenuse
        #print(f"ogdist = {ogDist}, currdist = {currDist}, vel = {self.velocity}")
        if currDist >= 10:
            self.velocity = 10
            self.position[0] -= math.cos(angleTowards)*self.velocity
            self.position[1] -= math.sin(angleTowards)*self.velocity
            return True
        return False
    
    def makeogPos(self, NumBssAtks, currNumBssAtk, currOgPos):
        if currNumBssAtk == NumBssAtks:
            return boss.position
        return currOgPos
    
    def fancyGotoPos(self, target, ogPos, NumBssAtks, startEndTime): 
        angleTowards = math.atan2(ogPos[1]-target[1],ogPos[0]-target[0])
        ogDist = math.sqrt((ogPos[0] - target[0])**2 + (ogPos[1] - target[1])**2) #pythagoras to find hypotenuse
        currDist = math.sqrt((boss.position[0] - target[0])**2 + (boss.position[1] - target[1])**2) #pythagoras to find hypotenuse
        speedChangetime = ((self.maxSpeed+1)*self.maxSpeed)/2
        print(f"ogdist = {ogDist}, currdist = {currDist}, vel = {self.velocity}")
        if NumBssAtks > startEndTime[0] and NumBssAtks < startEndTime[1]:
            if currDist > 0:
                if ogDist > speedChangetime:
                    if abs(self.velocity) < self.maxSpeed and currDist > speedChangetime:
                        self.velocity-=1
                        print("going!")
                    elif currDist < speedChangetime:
                        self.velocity+=1
                        print("decelerating!")
                elif ogDist == speedChangetime:
                    if currDist > speedChangetime:
                        self.velocity-=1
                    elif currDist < speedChangetime:
                        self.velocity+=1
                elif ogDist < speedChangetime*2:
                    if currDist > ogDist/2:
                        self.velocity-=1
                    elif currDist < ogDist/2:
                        self.velocity1+=1
                self.position[0] += math.cos(angleTowards)*self.velocity
                self.position[1] += math.sin(angleTowards)*self.velocity
                self.rect.update([self.position[0]-self.diameter/2, self.position[1]-self.diameter/2], [self.diameter,self.diameter])
                return ogPos
            else:
                self.velocity = 0
        if NumBssAtks == startEndTime[0]:
            return boss.position[:]
        else:
            return ogPos
    
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
                for i in range(7):
                    self.addBullet("yellowbasic", self.position[:], 8, math.degrees(math.atan2(player.y-200,player.x-500))-45+i*15)
                
            if special == 1:
                self.addBullet("yellowAccelerate", [700, -15], 1, random.randint(60,120))
                self.addBullet("yellowAccelerate", [500, -15], 1, random.randint(60,120))
                self.addBullet("yellowAccelerate", [300, -15], 1, random.randint(60,120))

    
    def addBullet(self, btype,pos,vel,angle):
        enemyBullets.append(EnemyBullet(btype, pos, vel, angle,len(enemyBullets)))
###################################################
#STAGE CODE
###################################################
def runStage(stageData, runStage):
	for item in stageData:
		if item[0]*100 == stageCount:
			enemyBullets.append(EnemyBullet(item[1], item[2], item[3], item[4],len(enemyBullets)))
#== STAGE 1 =======================================
def getStageData(stage):
    if stage == 1:
    	return (
            (1, "bamboo", [150, -40], 12, 90),
            (1, "bamboo", [850, -40], 12, 90),
            (2, "bamboo", [150, -40], 12, 90),
            (2, "bamboo", [850, -40], 12, 90),
            (3, "bamboo", [150, -40], 12, 90),
            (3, "bamboo", [850, -40], 12, 90),
            (4, "bamboo", [150, -40], 12, 90),
            (4, "bamboo", [850, -40], 12, 90),
            (5, "bamboo", [150, -40], 12, 90),
            (5, "bamboo", [850, -40], 12, 90),
            (6, "bamboo", [150, -40], 12, 90),
            (6, "bamboo", [850, -40], 12, 90),
    	    ) #Format for each item (time, bullet type,position,velocity,angle/direction)...

#==========================
# Setup
#==========================
player = Player()
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
bulletCooldownTimer = 12

stage = 1
stageCount = 0

bossReady = False
bossbulletCooldownTimer = 0
bosscdthreshold = 10
numBossattacks = 0
ogPos = boss.position[:]

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
                    if menuSelect == 3:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
            
            menutext = ["Story", "Options", "Music Room", "Exit"]
            for textNum in range(len(menutext)):
                textDisplay = text.render(menutext[textNum], False, menuGetColour(textNum))
                DISPLAYSURF.blit(textDisplay, (700,300+textNum*100))
            
            if inputCooldown < 10:
                inputCooldown += 1
            
        case 1: #main gameply
            DISPLAYSURF.fill((0,0,0))
            
            if keys[K_LEFT]:
                    player.x -= playerSpeed
            elif keys[K_RIGHT]:   
                    player.x += playerSpeed
            if keys[K_UP]:
                    player.y -= playerSpeed
            elif keys[K_DOWN]:    
                    player.y += playerSpeed
            if keys[K_LSHIFT] or keys[K_LCTRL]:
                focus = True
                playerSpeed = 3
                if player.focusBaguaRotation <= 360:
                    player.focusBaguaRotation += 1
                else: 
                    player.focusBaguaRotation = 0
            else:
                focus = False
                playerSpeed = 6
            player.rect.update(player.x-player.diameter/2, player.y-player.diameter/2,7,7)

            if keys[K_z]:
                if bulletCooldownTimer >= player.bulletCooldown:
                    player.playerBullets.append(PlayerBullet("basic", [player.x+15, player.y], [0, -25], len(player.playerBullets)))
                    player.playerBullets.append(PlayerBullet("basic", [player.x-15, player.y], [0, -25], len(player.playerBullets)))
                    bulletCooldownTimer = 0
            
            
            
            #==========================
            # Boss Loop
            #==========================
            if bossReady:
                if bossbulletCooldownTimer == bosscdthreshold:
                    #Shooting===============
                    if numBossattacks % 40 < 5 and numBossattacks < 447:
                        boss.bossAttack(2,0)
                        bossbulletCooldownTimer = 0

                    elif numBossattacks and 447 < numBossattacks < 800:
                        boss.bossAttack(2,1)
                        bossbulletCooldownTimer = 0 
                    elif numBossattacks and 800 < numBossattacks < 1200:
                        boss.bossAttack(2,0)
                        bossbulletCooldownTimer = 0 


                    numBossattacks +=1
                #Moving=================
                ogPos = boss.fancyGotoPos([200, boss.position[1]], ogPos, numBossattacks, [80, 200])
                ogPos = boss.fancyGotoPos([800, boss.position[1]], ogPos, numBossattacks, [200, 320])
                ogPos = boss.fancyGotoPos([500, boss.position[1]], ogPos, numBossattacks, [320, 420])
                #print(ogPos)
            #==========================
            # Per Loop Updates
            #==========================
            if pygame.sprite.spritecollide(player,enemyBullets,False,pygame.sprite.collide_rect_ratio(1)):
                gameState = 0

            if pygame.sprite.collide_rect(player, boss):
                gameState = 0
            if bulletCooldownTimer < 10:
                bulletCooldownTimer += 1
            if bossbulletCooldownTimer < bosscdthreshold:
                bossbulletCooldownTimer += 1
            
            runStage(getStageData(stage), stageCount)
            stageCount +=1
            updateGraphics()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)