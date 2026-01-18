############################################################################################################
############################################################################################################
# SYSTEM SETUP
############################################################################################################
############################################################################################################

import pygame, sys, random, math
from pygame.locals import *

pygame.init()

FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()
DEBUG = False

text = pygame.font.SysFont('Times New Roman', 30)

DISPLAYSURF = pygame.display.set_mode((1000, 950))
pygame.display.set_caption('Mizhou Episode 0.5')

############################################################################################################
############################################################################################################
# VARIABLE SETUP
############################################################################################################
############################################################################################################
gameState = 0

enemyBullets = []
enemies = []
items = []
bulletCooldownTimer = 4
bombCooldownTimer = 4

lives = 5
bombs = 3
points = 0
bombing = 0

stage = 1
stageCount = 0

bossReady = False
bossbulletCooldownTimer = 0
bosscdthreshold = 20
numBossattacks = 0
ogPos = [0,0]

menuSelect = 0
inputCooldown = 10

playerInvincability = 0
dialogue = 0
despawnRange = [1600,-600]


############################################################################################################
############################################################################################################
# GAME ASSETS
############################################################################################################
############################################################################################################

def ezload(img):
    return pygame.image.load(f'PygameGame/{img}')
def portraitload(img):
    return pygame.image.load(f'PygameGame/portraits/{img}')
#===========PLAYER============
jiangSprite = ezload('player.png')
playerHitbox = ezload('playerHitbox.png')
focusBagua = ezload('baguaFocus.png')
focusSpear = ezload('spearFocus.png')
liveSprite = ezload('biglife.png')
bombSprite = ezload('bigbomb.png')
pointsSprite = ezload('points.png')

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
evilyinyangSprite = ezload('bluespirit.png')
eMyinyang = ezload('enemyyinyang.png')

pygame.Surface.set_alpha(evilyinyangSprite, 180)
pygame.Surface.set_alpha(eMyinyang, 230)
pygame.Surface.set_alpha(basicPlayerBullet, 185)

#===========BOSSES============
qiSprite = ezload('qiBoss.png')

#Portraits
PORTRAITS = {
    "Jiang" : {
        "neutral" : portraitload("jiangNeutral.png"),
        "angry" : portraitload("jiangAngry.png"),
        "annoyed" : portraitload("jiangAnnoyed.png"),
        "confused" : portraitload("jiangConfused.png"),
        "happy" : portraitload("jiangHappy.png"),
        "smug" : portraitload("jiangSmug.png"),
        "sweat" : portraitload("jiangSweat.png")
    },
    "Qi" : {
        "neutral" : portraitload("qiNeutral.png"),
        "angry" : portraitload("qiAngry.png"),
        "confused" : portraitload("qiConfused.png"),
        "sweat" : portraitload("qiSweat.png")
    }
}

#===========MUSIC============
MUSIC = pygame.mixer.music
MUSIC.load('PygameGame/LandOfTheLostFog.mp3')
MUSIC.play()
MUSIC.set_volume(0.5)

############################################################################################################
############################################################################################################
# GAME DATA
############################################################################################################
############################################################################################################

DIALOGUEBOSS2 = (
    ("Jiang", "smug","Hmm, I think I've found the culprit..."),
    ("Qi", "neutral","Really?"),
    ("Jiang", "smug","Don't act suprised, culprit."),
    ("Qi", "confused","What!?"),
    ("Qi", "angry","I'm the one who is missing stuff!"),
    ("Jiang", "smug","That's exactly what the culprit would say!"),
)

level_1_data = (
    #[(1 + random.random(), "EMbox", [random.randint(50,950), -40], 5, 90) for i in range(5)] +
    #[(2 + random.random(), "EMbox", [random.randint(50,950), -40], 5, 90) for i in range(5)] +
    #[(3 + random.random(), "EMbox", [random.randint(50,950), -40], 5, 90) for i in range(5)] +
    #[(4 + random.random(), "yinyangright", [1200, 100 + random.randint(-10,600)], 10 + random.randint(-2,2), 190) for i in range(7)] +
    #[(5 + random.random(), "yinyangright", [1200, 100 + random.randint(-10,600)], 10 + random.randint(-2,2), 190) for i in range(7)] +
    #[(6 + random.random(), "yinyangright", [1200, 100 + random.randint(-200,600)], 10 + random.randint(-2,2), 190) for i in range(10)] +
    #[(7.4 + random.random(), "yinyangleft", [-200, 100 + random.randint(-200,600)], 10 + random.randint(-2,2), 350) for i in range(10)] +
    #[(8 + random.random(), "yinyangleft", [-200, 100 + random.randint(-200,600)], 10 + random.randint(-2,2), 350) for i in range(10)] +
    #[(9 + random.random(), "yinyangleft", [-200, 100 + random.randint(-200,600)], 10 + random.randint(-2,2), 350) for i in range(10)] +
    #[(10 + random.random(), "yinyang", [random.randint(100,1500), -40], 7 + random.randint(-2,2), 110) for i in range(35)] +
    #[(random.randint(11,14) + random.random(), "EMbox", [random.randint(50,950), -40], 5, 90) for i in range(10)] +
    #[(14 + random.random(), "yinyang", [random.randint(100,1500), -40], 10 + random.randint(-2,2), 110) for i in range(30)] +
    #[(random.randint(16,18) + random.random(), "EMbox", [random.randint(50,950), -40], 5, 90) for i in range(10)] +
    #[(random.randint(16,18), "yinyang", [1050, random.randint(50,950)], 6 + random.randint(-2,2), 170) for i in range(5)] +
    #[(random.randint(16,18), "yinyang", [-50, random.randint(50,950)], 6 + random.randint(-2,2), 10) for i in range(5)] +
    #[(19 + i/3, "EMyinyangevil", [1200, 50], 7, 160) for i in range(10)] +
    #[(20 + i/2, "yinyang", [1200, 100+i*100], 4, 180) for i in range(10)] +
    #[(20 + i/2, "yinyang", [-200, 100+i*100], 4, 0) for i in range(10)] +
    #[(24 + i/3, "EMyinyangevil", [1200, 50], 5, 160) for i in range(8)] +
    #[(28 + random.random(), "yinyangright", [1200, 100 + random.randint(-10,600)], 10 + random.randint(-2,2), 190) for i in range(10)] +
    #[(31 + random.random(), "yinyang", [random.randint(100,1500), -40], 7 + random.randint(-2,2), 110) for i in range(35)] +
    [(0, "boss", 2)] #34
)    

#===========================================================================================================
# PLAYER CODE & setup
#===========================================================================================================
class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.lives = 5
        self.bombs = 3
        self.playerSprite = jiangSprite
        self.x = 500
        self.y = 500
        self.diameter = 5
        self.playerSpeed = 5
        self.focusBaguaRotation = 0
        self.playerBullets = []
        self.bulletCooldown = 4
        self.rect = Rect(self.x-self.diameter/2, self.y-self.diameter/2, self.diameter,self.diameter) #math.sqrt(self.diameter/2), math.sqrt(self.diameter/2))


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
    if DEBUG and boss.level > 0:
        pygame.draw.rect(DISPLAYSURF, (0,255,0) , boss.rect)
    #enemies collide
    for enemy in enemies:
        if enemy.hitcooldown < 3:
            enemy.hitcooldown += 1
        if enemy.typeBullet == "EMyinyangevil":
            if enemy.cooldown == 30:
                enemy.cooldown = 0
                enemy.attack()
            elif enemy.cooldown < 30:
                enemy.cooldown += 1

        removedBullet = False
        if pygame.sprite.spritecollide(enemy,player.playerBullets,False,pygame.sprite.collide_rect_ratio(1)) and enemy.hitcooldown == 3 or bombing > 0:
            enemy.hp -= 1
            enemy.hitcooldown = 0
            if enemy.hp <= 0:
                enemyDestroyed = enemy.destroy()
                removedBullet = True
                #print(f"removedBullet = {removedBullet}, bulletDestroyed = {enemyDestroyed}")
        elif enemy.position[1] > despawnRange[0] or enemy.position[1] < despawnRange[1] or enemy.position[0] > despawnRange[0] or enemy.position[0] < despawnRange[1]:
            enemyDestroyed = enemy.destroy()
            removedBullet = True
        if removedBullet:
            for newID in enemies[enemyDestroyed:]:
                newID.index = newID.index-1
    # Items
    for item in items:
        global lives
        global bombs
        global points
        item.move()
        if DEBUG:
            pygame.draw.rect(DISPLAYSURF, (0,0,255) , bullet.rect)
        item.render()
        removed = False
        if pygame.sprite.collide_circle_ratio(3)(item,player):
            itemDestroyed = item.destroy()
            removed = True
            if item.itemType == "life":
                if lives < 8:
                    lives += 1
            elif item.itemType == "bomb":
                if bombs < 8:
                    bombs += 1
            elif item.itemType == "points":
                points += 100
        elif item.position[1] < despawnRange[1]:
            itemDestroyed = item.destroy()
            removed = True
        if removed:
            for newID in items[itemDestroyed:]:
                newID.index = newID.index-1
    #==========================
    # Player
    #==========================
    #bullets
    for bullet in player.playerBullets:
        bullet.move()
        if DEBUG:
            pygame.draw.rect(DISPLAYSURF, (255,0,255) , bullet.rect)
        bullet.render()
        
        removedBullet = False
        if pygame.sprite.spritecollide(bullet,enemies,False,pygame.sprite.collide_rect_ratio(1)):
            bulletDestroyed = bullet.destroy()
            removedBullet = True
            #print(f"removedBullet = {removedBullet}, bulletDestroyed = {bulletDestroyed}")
        elif boss.level > 0:
            if pygame.sprite.collide_rect(bullet,boss):
                boss.health -= 1
                bulletDestroyed = bullet.destroy()
                removedBullet = True
        elif bullet.position[1] < despawnRange[1]:
            bulletDestroyed = bullet.destroy()
            removedBullet = True
        
        if removedBullet:
            for bulletNewID in player.playerBullets[bulletDestroyed:]:
                bulletNewID.index = bulletNewID.index-1
    if focus == True:
        displayIMGPlayer(pygame.transform.rotate(focusBagua, player.focusBaguaRotation))
        displayIMGPlayer(pygame.transform.rotate(focusSpear, 0-player.focusBaguaRotation))
    
    if playerInvincability > 0:
        pygame.Surface.set_alpha(player.playerSprite, 255 - playerInvincability)

        displayIMGPlayer(player.playerSprite)
    else:
        pygame.Surface.set_alpha(player.playerSprite, 255)
        displayIMGPlayer(player.playerSprite)
    if DEBUG:
        pygame.draw.rect(DISPLAYSURF, (255,0,255) , player.rect)
    #==========================
    # Enemies
    #==========================
    #Enemy bullets
    for bullet in enemyBullets:
        bullet.move()
        bullet.render()
        removedBullet = False
        if bullet.position[1] > despawnRange[0] or bullet.position[1] < despawnRange[1] or bullet.position[0] > despawnRange[0] or bullet.position[0] < despawnRange[1] or bombing > 0:
            bulletDestroyed = bullet.destroy()
            removedBullet = True
        if DEBUG:
            pygame.draw.rect(DISPLAYSURF, (255,255,0) , bullet.rect)
        if removedBullet:
            for bulletNewID in enemyBullets[bulletDestroyed:]:
                bulletNewID.index = bulletNewID.index-1
        
    for enemy in enemies:
        enemy.move()
        enemy.render()
        removedBullet = False
        if DEBUG:
            pygame.draw.rect(DISPLAYSURF, (255,255,0) , enemy.rect)
        
            
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


class Item(pygame.sprite.Sprite):
    def __init__(self, itemType, pos, velocity, index):
        self.itemType = itemType
        self.position = pos
        self.velocity = velocity
        self.index = index
        self.diameter = 30
        self.rect = Rect(self.position[0]-self.diameter/2, self.position[1]-self.diameter/2, self.diameter, self.diameter)

    
    def move(self):
        self.position[1] += self.velocity
        if self.velocity < 6:
            self.velocity += 0.1
        self.rect.update([self.position[0]-self.diameter/2, self.position[1]-self.diameter/2], [self.diameter,self.diameter])

    def render(self):
        if self.itemType == "life":
            self.selfDraw(liveSprite)
        elif self.itemType == "bomb":
            self.selfDraw(bombSprite)
        elif self.itemType == "points":
            self.selfDraw(pointsSprite)
    def selfDraw(self, img):
        DISPLAYSURF.blit(img, (self.position[0] - img.get_width()/2, self.position[1] - img.get_height()/2))
    def destroy(self):
        items.pop(self.index)
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
                self.hp = 1
            elif self.typeBullet[2:] == "yinyangevil":
                self.hp = 5
                self.cooldown = 0
        if self.typeBullet == "basic":
            self.sprite = basicBullet
        elif self.typeBullet in ["yellowbasic", "yellowAccelerate", "yellowRotate"]:
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
        elif self.typeBullet[:7] == "yinyang" or self.typeBullet in ["EMyinyangevil", "EMbox"]:
            self.diameter = 40
            self.rect = Rect(self.position[0]-self.diameter/2, self.position[1]-self.diameter/2, self.diameter, self.diameter)
        elif self.typeBullet in ["basic","yellowbasic","yellowAccelerate", "yellowRotate"]:
            self.diameter = 25
            self.rect = Rect(self.position[0]-self.diameter/2, self.position[1]-self.diameter/2, self.diameter, self.diameter)
    
    def move(self):
        self.position[0] += math.cos(math.radians(self.angle))*self.velocity
        self.position[1] += math.sin(math.radians(self.angle))*self.velocity
        #if self.typeBullet in ["basic","yellowbasic","yellowAccelerate", "yellowturn"]:
        self.rect.update([self.position[0]-self.diameter/2, self.position[1]-self.diameter/2], [self.diameter,self.diameter])
        if self.typeBullet == "yellowAccelerate":
            self.velocity += 0.02
        elif self.typeBullet == "yinyangright" or self.typeBullet ==  "yellowRotate":
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
            if self.typeBullet == "EMbox":
                getPoints = random.randint(0,6)
                if getPoints == 0:
                    items.append(Item("bomb", self.position[:], -3, len(items)))
                else:
                    pointsAmount = random.randint(3,8)
                    for i in range(pointsAmount):
                        items.append(Item(random.choice(["points"]), [self.position[0]+ random.randint(-50,50),self.position[1]+ random.randint(-20,50)], -3, len(items)))
            elif self.typeBullet == "EMyinyangevil":
                getPoints = random.randint(0,3)
                if getPoints == 0:
                    items.append(Item(random.choice(["bomb", "bomb", "bomb","bomb","life"]), self.position[:], -3, len(items)))
                else:
                    pointsAmount = random.randint(3,8)
                    for i in range(pointsAmount):
                        items.append(Item(random.choice(["points"]), [self.position[0]+ random.randint(-50,50),self.position[1]+ random.randint(-20,50)], -3, len(items)))
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
            self.position = [500, -60]
            self.velocity = 0
            self.health = 999
            self.maxV = [10,10]
            self.diameter = 70
            self.maxSpeed = 5
            print("made!!")
            self.rect = Rect(self.position[0],self.position[1], 70, 70)
            self.rect.update([self.position[0]-self.diameter/2, self.position[1]-self.diameter/2], [self.diameter,self.diameter])
            if self.level == 2:
                self.health = 1000
    
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
        if NumBssAtks > startEndTime[0] and NumBssAtks < startEndTime[1]:
            #print(math.degrees(angleTowards))
            #print(f"ogdist = {ogDist}, currdist = {currDist}, vel = {self.velocity}, speedchangetime = {speedChangetime}")
            if currDist > 0:
                if ogDist > speedChangetime*2:
                    if abs(self.velocity) < self.maxSpeed and currDist > ogDist-speedChangetime:
                        self.velocity-=1
                    elif currDist < speedChangetime:
                        self.velocity+=1
                elif ogDist == speedChangetime*2:
                    if currDist > ogDist-speedChangetime:
                        self.velocity-=1
                    elif currDist < speedChangetime:
                        self.velocity+=1
                elif ogDist < speedChangetime*2:
                    if currDist > ogDist/2:
                        self.velocity-=1
                    elif currDist < ogDist/2:
                        self.velocity+=1
                if abs(self.velocity) > self.maxSpeed:
                    if self.velocity > 0:
                        self.velocity = 5
                    elif self.velocity < 0:
                        self.velocity = -5
                self.position[0] += math.cos(angleTowards)*self.velocity
                self.position[1] += math.sin(angleTowards)*self.velocity
                self.rect.update([self.position[0]-self.diameter/2, self.position[1]-self.diameter/2], [self.diameter,self.diameter])
                return ogPos
            else:
                self.velocity = 0
        if NumBssAtks == startEndTime[0]:
            print("done")
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
                
            if special == 2:
                for i in range(12):
                    self.addBullet("yellowRotate", self.position[:], 8, math.degrees(math.atan2(player.y-200,player.x-500))+i*30)

    
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
                return "BossInit"
        elif int(item[0]*100) == stageCount:
            if item[1][:2] == "EM":
                enemies.append(EnemyBullet(item[1], item[2], item[3], item[4],len(enemies)))
            else:
                enemyBullets.append(EnemyBullet(item[1], item[2], item[3], item[4],len(enemyBullets)))
    return ""
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

def setMusic(song):
    MUSIC.load(f'PygameGame/{song}.mp3')
    MUSIC.play()
    MUSIC.set_volume(0.5)

def setState(state):
    if state == 0:
        setMusic("LandOfTheLostFog")
    elif state == 1:
        setMusic("Stage1Theme")
    return state

def doDialouge(level, textID):
    currDia = DIALOGUEBOSS2[textID]
    textpos = [300,700]
    if level == "boss2":
        if textID < len(DIALOGUEBOSS2):
            textDisplay = text.render(currDia[2], False, (255,255,255))
            DISPLAYSURF.blit(PORTRAITS[currDia[0]][currDia[1]],(textpos[0]-250,textpos[1]-50))
            DISPLAYSURF.blit(textDisplay, (textpos[0],textpos[1]))
    return textID+1
    
############################################################################################################
############################################################################################################
# MAIN GAME LOOP
############################################################################################################
############################################################################################################

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
                if player.x > 0:
                    player.x -= playerSpeed
            elif keys[K_RIGHT]:
                if player.x < 1000:
                    player.x += playerSpeed
            if keys[K_UP]:
                if player.y > 0:
                    player.y -= playerSpeed
            elif keys[K_DOWN]:
                if player.y < 950:
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
            if keys[K_x]:
                if bombCooldownTimer >= 40 and bombs > 0:
                    bombs -= 1
                    bombing = 30
                    playerInvincability = 30
                    bombCooldownTimer = 0    
            
            #==========================
            # Boss Loop
            #==========================
            initBoss = runStage(getStageData(stage), stageCount)
            if bossReady:
                if bossbulletCooldownTimer == bosscdthreshold:
                    #Shooting===============
                    if numBossattacks % 40 < 15 and 100 < numBossattacks < 350:
                        boss.bossAttack(2,0)
                        bossbulletCooldownTimer = 0

                    elif numBossattacks and 350 < numBossattacks < 400:
                        bosscdthreshold = 20
                        boss.bossAttack(2,1)
                        bossbulletCooldownTimer = 0 
                    elif numBossattacks % 40 < 5 and 400 < numBossattacks < 450:
                        boss.bossAttack(2,0)
                        bossbulletCooldownTimer = 0 
                    elif numBossattacks % 40 < 5 and 450 < numBossattacks < 600:
                        bosscdthreshold = 15
                        boss.bossAttack(2,2)
                        bossbulletCooldownTimer = 0     
                    elif numBossattacks > 600:
                        bosscdthreshold = 20
                        numBossattacks = 0
                    
                    numBossattacks +=1
                    print(numBossattacks)
                if bossbulletCooldownTimer < bosscdthreshold:
                    bossbulletCooldownTimer += 1
                #Moving=================
                ogPos = boss.fancyGotoPos([boss.position[0], 120], ogPos, numBossattacks, [0, 100])
                ogPos = boss.fancyGotoPos([200, boss.position[1]], ogPos, numBossattacks, [100, 200])
                ogPos = boss.fancyGotoPos([800, boss.position[1]], ogPos, numBossattacks, [200, 320])
                ogPos = boss.fancyGotoPos([500, boss.position[1]], ogPos, numBossattacks, [320, 420])
                
                textDisplay = text.render(f"Boss Health: {boss.health}", False, (255,255,255))
                DISPLAYSURF.blit(textDisplay, (50,50))
                    #print(ogPos)
                if pygame.sprite.collide_rect(player, boss):
                    gameState = setState(0)
                
            #==========================
            # Per Loop Updates
            #==========================
            if playerInvincability == 0:
                if pygame.sprite.spritecollide(player,enemyBullets,False,pygame.sprite.collide_rect_ratio(1)) or pygame.sprite.spritecollide(player,enemies,False,pygame.sprite.collide_rect_ratio(1)):
                    lives -= 1
                    player.x = 500
                    player.y = 500
                    playerInvincability = 120
                    if lives == 0:
                        gameState = setState(0)
                    bombs = 3
            elif playerInvincability > 0:
                playerInvincability -=1
            
            bulletCooldownTimer += 1
            bombCooldownTimer += 1
            
        
            stageCount +=1
                   
            updateGraphics()
            
            if not bossReady:
                if initBoss == "BossInit":
                    if stage == 1:
                        setMusic("QiTheme")
                        dialogue = 1
                        dialogueDone = doDialouge("boss2", 0)
                if dialogue > 0 and stage == 1:
                    if dialogue-1 < len(DIALOGUEBOSS2):
                        dialogue = doDialouge("boss2", dialogue-1)
                        for event in pygame.event.get():
                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    pygame.quit()
                                    sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_z:
                                    dialogue +=1
                    else:
                        boss = Boss(2)
                        bossReady = True
            
            for i in range(lives):
                DISPLAYSURF.blit(liveSprite, (20 + i* 50, 880))
            for i in range(bombs):
                DISPLAYSURF.blit(bombSprite, (940 - i*50, 880))
            if bombing > 0:
                bombing -=1
                
            textDisplay = text.render(f"Points: {points}", False, (255,255,255))
            DISPLAYSURF.blit(textDisplay, (850,50))
            
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)