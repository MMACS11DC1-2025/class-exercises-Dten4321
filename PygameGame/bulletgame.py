import pygame, sys, time, random, math
from pygame.locals import *

pygame.init()

FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

text = pygame.font.SysFont('Comic Sans MS', 30)

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
        self.radius = 5
        self.playerSpeed = 5
        self.focusBaguaRotation = 0
        self.playerBullets = []
        self.bulletCooldown = 4
        self.rect = Rect(self.x-self.radius/2, self.y-self.radius/2, self.radius,self.radius) #math.sqrt(self.radius/2), math.sqrt(self.radius/2))

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
        #pygame.draw.rect(DISPLAYSURF, (255,255,0) , bullet.rect)
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
        self.radius = 12
    
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
        if self.typeBullet in ["basic","yellowbasic","yellowAccelerate"]:
            self.radius = 20
            self.radiusRect = self.radius
            self.rect = Rect(self.position[0]-self.radius/2, self.position[1]-self.radius/2, self.radiusRect, self.radiusRect)

    
    def move(self):
        self.position[0] += math.cos(math.radians(self.angle))*self.velocity
        self.position[1] += math.sin(math.radians(self.angle))*self.velocity
        if self.typeBullet in ["basic","yellowbasic","yellowAccelerate"]:
            self.rect.update([self.position[0]-self.radius/2, self.position[1]-self.radius/2], [self.radiusRect,self.radiusRect])
        if self.typeBullet == "yellowAccelerate":
            self.velocity += 0.02
    
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
    
class Boss(pygame.sprite.Sprite):
    def __init__(self, level):
        self.level = level
        self.position = [500, 120]
        self.velocity = 0
        self.health = 999
        self.maxV = [10,10]
        self.rect = Rect(self.position[0],self.position[1], 70, 70)
        if self.level == 2:
            self.health = 200
    
    def gotoPos(self, target, pos, ogPos):
        angleTowards = math.degrees(math.atan2(ogPos[1]-target[1],ogPos[0]-target[0]))
        ogDist = (ogPos[0] - target[0], ogPos[1] - target[1]) #pythagoras to find hypotenuse
        currDist = (pos[0] - target[0], pos[1] - target[1]) #pythagoras to find hypotenuse
        if ogDist > 90:
            if self.velocity < 10 and currDist > 45:
                self.velocity+=1
            elif currDist < 45:
                self.velocity-=1
        elif ogDist == 90:
            if currDist > 45:
                self.velocity+=1
            elif currDist < 45:
                self.velocity-=1
        elif ogDist < 90:
            if currDist > ogDist/2:
                self.velocity+=1
            elif currDist < ogDist/2:
                self.velocity-=1
        if pos[0] > target[0]-10 and pos[0] < target[0]+10 and pos[1] > target[1]-10 and pos[1] < target[1]+10:
            return False
        else:
            self.position[0] += math.cos(math.radians(angleTowards))*self.velocity
            self.position[1] += math.sin(math.radians(angleTowards))*self.velocity
            return True
        
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
                self.addBullet("yellowAccelerate", [700, -40], 0, 60)
                self.addBullet("yellowAccelerate", [300, -40], 0, 120)
                self.addBullet("yellowAccelerate", [700, -15], 0, random.randint(60,120))
                self.addBullet("yellowAccelerate", [300, -15], 0, random.randint(60,120))

    
    def addBullet(self, btype,pos,vel,angle):
        enemyBullets.append(EnemyBullet(btype, pos, vel, angle,len(enemyBullets)))

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
            player.rect.update(player.x-player.radius/2, player.y-player.radius/2,7,7)

            if keys[K_z]:
                if bulletCooldownTimer >= player.bulletCooldown:
                    player.playerBullets.append(PlayerBullet("basic", [player.x+15, player.y], [0, -25], len(player.playerBullets)))
                    player.playerBullets.append(PlayerBullet("basic", [player.x-15, player.y], [0, -25], len(player.playerBullets)))
                    bulletCooldownTimer = 0

            #==========================
            # Boss Loop
            #==========================
            if bossbulletCooldownTimer == bosscdthreshold:
                #Moving=================
                if numBossattacks == 120:
                    ogPos = boss.position[:]
                elif 120 < numBossattacks < 130:
                    boss.gotoPos([boss.position[0], 200], boss.position, ogPos)
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

                elif numBossattacks and 447 < numBossattacks < 800:
                    boss.bossAttack(2,1)
                    bossbulletCooldownTimer = 0 
                elif numBossattacks and 800 < numBossattacks < 1200:
                    boss.bossAttack(2,0)
                    bossbulletCooldownTimer = 0 


                numBossattacks +=1
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
            updateGraphics()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)