import pygame, sys, time, random, math
from pygame.locals import *

pygame.init()

FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

text = pygame.font.SysFont('Times New Roman', 30)

level_1_data = (
    [(0 + random.random(), "EMbox", [random.randint(50,950), -40], 5, 90) for i in range(10)] +
    [(1 + random.random(), "EMbox", [random.randint(50,950), -40], 5, 90) for i in range(10)] +
    [(2 + random.random(), "EMbox", [random.randint(50,950), -40], 5, 90) for i in range(10)] +
    [(3 + random.random(), "yinyangright", [1200, 100 + random.randint(-10,600)], 10 + random.randint(-2,2), 190) for i in range(7)] +
    [(4 + random.random(), "yinyangright", [1200, 100 + random.randint(-10,600)], 10 + random.randint(-2,2), 190) for i in range(7)] +
    [(5 + random.random(), "yinyangright", [1200, 100 + random.randint(-200,600)], 10 + random.randint(-2,2), 190) for i in range(10)] +
    [(6.4 + random.random(), "yinyangleft", [-200, 100 + random.randint(-200,600)], 10 + random.randint(-2,2), 350) for i in range(10)] +
    [(7 + random.random(), "yinyangleft", [-200, 100 + random.randint(-200,600)], 10 + random.randint(-2,2), 350) for i in range(10)] +
    [(8 + random.random(), "yinyangleft", [-200, 100 + random.randint(-200,600)], 10 + random.randint(-2,2), 350) for i in range(10)] +
    [(9 + random.random(), "yinyang", [random.randint(100,1500), -40], 7 + random.randint(-2,2), 110) for i in range(35)] +
    [(random.randint(10,13) + random.random(), "EMbox", [random.randint(50,950), -40], 5, 90) for i in range(30)] +
    [(13 + random.random(), "yinyang", [random.randint(100,1500), -40], 10 + random.randint(-2,2), 110) for i in range(30)] +
    [(random.randint(15,17) + random.random(), "EMbox", [random.randint(50,950), -40], 5, 90) for i in range(30)] +
    [(random.randint(15,17), "yinyang", [1050, random.randint(50,950)], 6 + random.randint(-2,2), 170) for i in range(5)] +
    [(random.randint(15,17), "yinyang", [-50, random.randint(50,950)], 6 + random.randint(-2,2), 10) for i in range(5)] +
    [(0 + i/3, "EMyinyangevil", [1200, 50], 7, 160) for i in range(10)] +
    [(14, "boss", 2)]
)    

DISPLAYSURF = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('Mizhou Episode 0.5')

gameState = 0

############################################################################################################
# IMAGES AND GAME ASSETS
############################################################################################################
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
bambooSprite = ezload('Bamboo.png')
boxSprite = ezload('box.png')
yinyangSprite = ezload('yinyang.png')
evilyinyangSprite = ezload('evilyinyangbig.png')
eMyinyang = ezload('enemyyinyang.png')

pygame.Surface.set_alpha(evilyinyangSprite, 200)
pygame.Surface.set_alpha(eMyinyang, 230)
pygame.Surface.set_alpha(basicPlayerBullet, 185)

#===========BOSSES============
qiSprite = ezload('qiBoss.png')

#===========MUSIC============
MUSIC = pygame.mixer.music
MUSIC.load('PygameGame/LandOfTheLostFog.mp3')
MUSIC.play()
MUSIC.set_volume(0.5)

#===========================================================================================================
# PLAYER CODE & setup
#===========================================================================================================
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
enemies = []


############################################################################################################
############################################################################################################
# GRAPHIC FUNCTIONS IN MAIN GAME
############################################################################################################
############################################################################################################
def displayIMGPlayer(img):
    DISPLAYSURF.blit(img, (player.x - img.get_width()/2, player.y - img.get_height()/2))

def updateGraphics():
    # Boss ==========================
    boss.render()
    #pygame.draw.rect(DISPLAYSURF, (0,255,0) , boss.rect)
    
    #enemies collide
    for enemy in enemies:
        if enemy.hitcooldown < 5:
            enemy.hitcooldown += 1
        if enemy.typeBullet == "EMyinyangevil":
            if enemy.cooldown == 30:
                enemy.cooldown = 0
                enemy.attack()
            elif enemy.cooldown < 30:
                enemy.cooldown += 1

        if pygame.sprite.spritecollide(enemy,player.playerBullets,False,pygame.sprite.collide_rect_ratio(1)) and enemy.hitcooldown == 10:
            enemy.hp -= 1
            enemy.hitcooldown = 0
            if enemy.hp <= 0:
                enemyDestroyed = enemy.destroy()
                removedBullet = True
            #print(f"removedBullet = {removedBullet}, bulletDestroyed = {bulletDestroyed}")
        elif enemy.position[1] > 1100:
            enemyDestroyed = enemy.destroy()
            removedBullet = True
    
    #==========================
    # Player
    #==========================
    #bullets
    for bullet in player.playerBullets:
        bullet.move()
        #pygame.draw.rect(DISPLAYSURF, (255,0,255) , bullet.rect)
        bullet.render()
        
        removedBullet = False
        if pygame.sprite.spritecollide(bullet,enemies,False,pygame.sprite.collide_rect_ratio(1)):
            bulletDestroyed = bullet.destroy()
            removedBullet = True
            #print(f"removedBullet = {removedBullet}, bulletDestroyed = {bulletDestroyed}")
        elif bullet.position[1] < -20:
            bulletDestroyed = bullet.destroy()
            removedBullet = True
        
        if removedBullet:
            for bulletNewID in player.playerBullets[bulletDestroyed:]:
                bulletNewID.index = bulletNewID.index-1
    if focus == True:
        displayIMGPlayer(pygame.transform.rotate(focusBagua, player.focusBaguaRotation))
        displayIMGPlayer(pygame.transform.rotate(focusSpear, 0-player.focusBaguaRotation))
    displayIMGPlayer(player.playerSprite)
    #pygame.draw.rect(DISPLAYSURF, (255,0,255) , player.rect)
    #==========================
    # Enemies
    #==========================
    #Enemy bullets
    for bullet in enemyBullets:
        bullet.move()
        bullet.render()
        removedBullet = False
        if bullet.position[1] > 1100:
            bulletDestroyed = bullet.destroy()
            removedBullet = True
        #pygame.draw.rect(DISPLAYSURF, (255,255,0) , bullet.rect)
        if removedBullet:
            for bulletNewID in enemyBullets[bulletDestroyed:]:
                bulletNewID.index = bulletNewID.index-1
        #pygame.draw.rect(DISPLAYSURF, (255,255,0) , bullet.rect)
        
    for enemy in enemies:
        enemy.move()
        enemy.render()
        removedBullet = False
        if pygame.sprite.spritecollide(enemy,player.playerBullets,False,pygame.sprite.collide_rect_ratio(1)):
            enemyDestroyed = enemy.destroy()
            removedBullet = True
            #print(f"removedBullet = {removedBullet}, bulletDestroyed = {bulletDestroyed}")
        elif enemy.position[1] > 1100:
            enemyDestroyed = enemy.destroy()
            removedBullet = True
        #pygame.draw.rect(DISPLAYSURF, (255,255,0) , bullet.rect)
        if removedBullet:
            for newID in enemies[enemyDestroyed:]:
                newID.index = newID.index-1
            
    if focus == True:
        displayIMGPlayer(playerHitbox)

############################################################################################################
############################################################################################################
# CLASSES & EXTRA FUNCTIONS
############################################################################################################
############################################################################################################

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, typeBullet, playerPos, velocity, angle, index):
        self.typeBullet = typeBullet
        self.position = playerPos
        self.velocity = velocity
        self.index = index
        self.angle = angle
        self.diameter = 30
        self.rect = Rect(self.position[0]-self.diameter/2, self.position[1]-self.diameter/2, self.diameter, self.diameter)

    
    def move(self):
        self.position[0] += math.cos(math.radians(self.angle))*self.velocity
        self.position[1] += math.sin(math.radians(self.angle))*self.velocity
        self.rect.update([self.position[0]-self.diameter/2, self.position[1]-self.diameter/2], [self.diameter,self.diameter])

    
    def render(self):
        self.selfDraw(basicPlayerBullet)
    def selfDraw(self, img):
        DISPLAYSURF.blit(img, (self.position[0] - img.get_width()/2, self.position[1] - img.get_height()/2))
    def destroy(self):
        player.playerBullets.pop(self.index)
        return self.index

#===========================================================================================================
# Ememy bullets
#===========================================================================================================
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, typeBullet, startPos, velocity, angle, index):
        self.typeBullet = typeBullet
        self.position = startPos
        self.velocity = velocity
        self.index = index
        self.angle = angle
        if self.typeBullet[:2] == "EM":
            self.hitcooldown = 0
            if self.typeBullet[2:] == "box":
                self.hp = 3
            elif self.typeBullet[2:] == "yinyangevil":
                self.hp = 10
                self.cooldown = 0
        if self.typeBullet == "basic":
            self.sprite = basicBullet
        elif self.typeBullet in ["yellowbasic", "yellowAccelerate"]:
            self.sprite = yellowbullet
        elif self.typeBullet == "yellowbeam":
            self.sprite = yellowbeam
        elif self.typeBullet == "bamboo":
            self.sprite = bambooSprite
        elif self.typeBullet == "EMbox":
            self.sprite = boxSprite
        elif self.typeBullet[:7] == "yinyang" or self.typeBullet == "EMyinyangevil":
            self.sprite = evilyinyangSprite
            self.visableRotation = 0
            if self.typeBullet == "EMyinyangevil":
                self.sprite = eMyinyang
        else:
            self.sprite = basicBullet
        
        if self.typeBullet == "bamboo":
            self.diameter = 28
            self.rect = Rect(self.position[0]-self.diameter/2, self.position[1]-self.diameter/2, self.diameter, self.diameter)
        elif self.typeBullet[:7] == "yinyang" or self.typeBullet == "EMyinyangevil":
            self.diameter = 40
            self.rect = Rect(self.position[0]-self.diameter/2, self.position[1]-self.diameter/2, self.diameter, self.diameter)
        elif self.typeBullet in ["basic","yellowbasic","yellowAccelerate", "EMbox"]:
            self.diameter = 25
            self.rect = Rect(self.position[0]-self.diameter/2, self.position[1]-self.diameter/2, self.diameter, self.diameter)
    
    def move(self):
        self.position[0] += math.cos(math.radians(self.angle))*self.velocity
        self.position[1] += math.sin(math.radians(self.angle))*self.velocity
        #if self.typeBullet in ["basic","yellowbasic","yellowAccelerate", "yellowturn"]:
        self.rect.update([self.position[0]-self.diameter/2, self.position[1]-self.diameter/2], [self.diameter,self.diameter])
        if self.typeBullet == "yellowAccelerate":
            self.velocity += 0.02
        elif self.typeBullet == "yinyangright":
            self.angle -= 0.5
        elif self.typeBullet == "yinyangleft":
            self.angle += 0.5
        elif self.typeBullet == "EMyinyangevil":
            self.angle += 0.2
        if self.typeBullet[:7] == "yinyang":
            self.visableRotation += 10
        elif self.typeBullet == "EMyinyangevil":
            self.visableRotation += 5

    
    def render(self):
        if self.typeBullet[:7] == "yinyang" or self.typeBullet == "EMyinyangevil":
            self.selfDraw(pygame.transform.rotate(self.sprite, self.visableRotation))
        else:
            self.selfDraw(self.sprite)
            
        
    def selfDraw(self, img):
        if self.typeBullet == "bamboo":
            DISPLAYSURF.blit(img, (self.position[0] - img.get_width()/2, self.position[1] - img.get_height()))
        else:
            DISPLAYSURF.blit(img, (self.position[0] - img.get_width()/2, self.position[1] - img.get_height()/2))

    def destroy(self):
        if self.typeBullet[:2] == "EM":
            enemies.pop(self.index)
        else:
            enemyBullets.pop(self.index)
        return self.index

    def attack(self):
        if self.typeBullet == "EMyinyangevil":
            self.addBullet("basic", self.position[:], 8, math.degrees(math.atan2(player.y-200,player.x-500)))
    
    def addBullet(self, btype, pos, vel, angle):
        enemyBullets.append(EnemyBullet(btype, pos, vel, angle,len(enemyBullets)))

#===========================================================================================================
# Boss
#===========================================================================================================

class Boss(pygame.sprite.Sprite):
    def __init__(self, level):
        self.level = level
        if level > 0:
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
        #print(f"ogdist = {ogDist}, currdist = {currDist}, vel = {self.velocity}")
        if NumBssAtks > startEndTime[0] and NumBssAtks < startEndTime[1]:
            if currDist > 0:
                if ogDist > speedChangetime:
                    if abs(self.velocity) < self.maxSpeed and currDist > speedChangetime:
                        self.velocity-=1
                        #print("going!")
                    elif currDist < speedChangetime:
                        self.velocity+=1
                        #print("decelerating!")
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
        
#==========================
# Setup
#==========================
player = Player()
boss = Boss(0)

def spawnBoss(level):
    return Boss(level)

#########################################################################################################
#STAGE CODE
#########################################################################################################
def runStage(stageData, stageCount):
    for item in stageData:
        if item[1] == "boss":
            if item[0]*100 == stageCount:
                spawnBoss(item[2])
        elif int(item[0]*100) == stageCount:
            if item[1][:2] == "EM":
                enemies.append(EnemyBullet(item[1], item[2], item[3], item[4],len(enemies)))
            else:
                enemyBullets.append(EnemyBullet(item[1], item[2], item[3], item[4],len(enemyBullets)))
        
#== STAGE 1 =======================================
def getStageData(stage):
    if stage == 1:
    	return level_1_data #Format for each item (time, bullet type,position,velocity,angle/direction)...


############################################################################################################
# EXTRA FUNCTIONS
############################################################################################################

def menuGetColour(id):
    if menuSelect == id:
        return (255,255,0)
    else: 
       return (255,255,255)

def setState(state):
    if state == 0:
        MUSIC.load('PygameGame/LandOfTheLostFog.mp3')
        MUSIC.play()
        MUSIC.set_volume(0.5)
    elif state == 1:
        MUSIC.load('PygameGame/Stage1Theme.mp3')
        MUSIC.play()
        MUSIC.set_volume(0.5)
    return state
############################################################################################################
############################################################################################################
# MAIN GAME LOOP
############################################################################################################
############################################################################################################
bulletCooldownTimer = 12

stage = 1
stageCount = 0

bossReady = False
bossbulletCooldownTimer = 0
bosscdthreshold = 10
numBossattacks = 0
ogPos = [0,0]

menuSelect = 0
inputCooldown = 10


while True:
    keys = pygame.key.get_pressed()
    match gameState:
        ############################################################################################################
        # MAIN MENU
        ############################################################################################################
        case 0: 
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
                        gameState = setState(1)
                    if menuSelect == 3:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
            
            menutext = ["Story", "Options", "Music Room", "Exit"]
            for textNum in range(len(menutext)):
                textDisplay = text.render(menutext[textNum], False, menuGetColour(textNum))
                DISPLAYSURF.blit(textDisplay, (700,300+textNum*100))
            
            if inputCooldown < 10:
                inputCooldown += 1
        
        ############################################################################################################
        # MAIN GAMEPLAY
        ############################################################################################################
        case 1:
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
                    player.playerBullets.append(PlayerBullet("basic", [player.x+15, player.y], 25, 270,len(player.playerBullets)))
                    player.playerBullets.append(PlayerBullet("basic", [player.x-15, player.y], 25, 270,len(player.playerBullets)))
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
            if pygame.sprite.spritecollide(player,enemyBullets,False,pygame.sprite.collide_rect_ratio(1)) or pygame.sprite.spritecollide(player,enemies,False,pygame.sprite.collide_rect_ratio(1)):
                gameState = setState(0)
            if bossReady:
                if pygame.sprite.collide_rect(player, boss):
                    gameState = setState(0)
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