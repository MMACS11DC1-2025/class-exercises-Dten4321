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

text = pygame.font.SysFont('Lucida Fax', 30)
dialogueText = pygame.font.SysFont('Lucida Fax', 20)
bigText = pygame.font.SysFont('Lucida Fax', 80)

DISPLAYSURF = pygame.display.set_mode((1000, 950))
pygame.display.set_caption('Mizhou Episode 0.5')

############################################################################################################
############################################################################################################
# VARIABLE SETUP
############################################################################################################
############################################################################################################
gameState = 0
backgroundY = 0
pause = False

enemyBullets = []
enemies = []
items = []
particles = []
bulletCooldownTimer = 4
bombCooldownTimer = 4

lives = 5
bombs = 3
points = 0
bombing = 0

stage = 1
stageCount = 0

bossbulletCooldownTimer = 0
bosscdthreshold = 20
numBossattacks = 0
ogPos = [0,0]

menuSelect = 0
inputCooldown = 10

playerInvincability = 0
dialogue = [0, False]
DESPWANRANGE = [1600,-600]


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
bigBullet = ezload('bigBullet.png')

pygame.Surface.set_alpha(evilyinyangSprite, 180)
pygame.Surface.set_alpha(eMyinyang, 230)
pygame.Surface.set_alpha(basicPlayerBullet, 185)

#===========BOSSES============
hanSprite = ezload('hanBoss.png')
qiSprite = ezload('qiBoss.png')
harukiSprite = ezload('harukiBoss.png')

##============PARTICLES=======
particleSprite = ezload('particle.png')
bambooBushSprite = ezload('Bambooleaves.png')
pygame.Surface.set_alpha(bambooBushSprite, 150)
bambooBushSpriteRight = pygame.transform.flip(bambooBushSprite, True, False)
bamboodarkBushSprite = ezload('Bambooleavesdark.png')
pygame.Surface.set_alpha(bamboodarkBushSprite, 150)
bamboodarkBushSpriteRight = pygame.transform.flip(bamboodarkBushSprite, True, False)

#============OTHER============
titleBackdrop = ezload('titleimage.png')
titleWords = ezload('titletext.png')
titleBox = ezload('titlebox.png')
stage1backdrop = ezload('backgroundStage1.png')
stage2backdrop = ezload('backgroundStage2.png')
stage3backdrop = ezload('backgroundStage3.png')
gameoverscreen = ezload('gameOverScreen.png')
victoryScreen = ezload('victoryScreen.png')
transitionSprite = ezload('transition.png')

pygame.Surface.set_alpha(titleBox, 200)

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
    },
    "Haruki" : {
        "neutral" : portraitload("harukiNeutral.png"),
        "angry" : portraitload("harukiAngry.png"),
        "angrier" : portraitload("harukiAngrier.png"),
        "confused" : portraitload("harukiConfused.png"),
        "smug" : portraitload("harukiSmug.png"),
        "sweat" : portraitload("harukiSweat.png")
    },
    "Han" : {
        "neutral" : portraitload("hanNeutral.png"),
        "smug" : portraitload("hanSmug.png")
    }
}

#===========MUSIC============
MUSIC = pygame.mixer.music
MUSIC.load('PygameGame/LandOfTheLostFog.mp3')
MUSIC.play(-1)
MUSIC.set_volume(0.5)

############################################################################################################
############################################################################################################
# GAME DATA
############################################################################################################
############################################################################################################

DIALOGUEBOSS1 = (
    ("Han", "neutral","Oh hello Jiang, what brings you to the town borders?"),
    ("Jiang", "neutral","Apparently someone from out of town stole something"),
    ("Jiang", "annoyed","...and I have to get it back."),
    ("Han", "smug","Don't you think you need to test your skill just in case?"),
    ("Jiang", "annoyed","Fine."),
)
DIALOGUEBOSS1END = (
    ("Han", "smug","You should be ready!"),
    ("Jiang", "angry","Let's not waste any more time..."),
)
DIALOGUEBOSS2 = (
    ("Jiang", "smug","Hmm, I think I've found the culprit..."),
    ("Qi", "neutral","Really?"),
    ("Jiang", "smug","Don't act suprised, culprit."),
    ("Qi", "confused","What!?"),
    ("Qi", "angry","I'm the one who is missing stuff!"),
    ("Jiang", "smug","That's exactly what the culprit would say!")
)
DIALOGUEBOSS2END = (
    ("Jiang", "confused","So you're really not the culprit?"),
    ("Qi", "angry","No..."),
    ("Jiang", "sweat","Oh"),
    ("Jiang", "sweat","Well I'm going to find them now..."),
    ("Qi", "sweat","Good luck I guess?")
)
DIALOGUEBOSS3 = (
    ("Haruki", "angrier","Who are you, and what are you doing here!"),
    ("Jiang", "annoyed", "I'm here to find the suspect who stole a ..lamp?"),
    ("Jiang", "confused","You wouldn't happen to know anything about it?"),
    ("Haruki", "sweat","Uhhh.... No... Totally!"),
    ("Jiang", "annoyed","Won't budge huh?"),
)
DIALOGUEBOSS3END = (
    ("Haruki", "sweat","It was me, it was me!"),
    ("Jiang", "annoyed","This is not allowed..."),
    ("Haruki", "sweat","I promise I won't do it again! It was just too interesting!"),
    ("Jiang", "confused","Interesting?"),
    ("Qi", "sweat","Goodness, I cannot sleep with this fight here!"),
    ("Qi", "neutral","Hey! The device I was missing!"),
    ("Haruki", "sweat","Sorry..."),
    ("Qi", "neutral","So, you like to study stuff?"),
    ("Haruki", "confused","Yes?"),
    ("Qi", "neutral","Well, I didn't make this, 'found it by the border."),
    ("Qi", "neutral","I think it's not from here!"),
    ("Haruki", "confused","Not from here!?"),
    ("Qi", "neutral","I invite you to help me in figuring out how this thing works."),
    ("Haruki", "smug","Of course!"),
    ("Jiang", "confused","Uhhh... I gues my work is done?"),
)

level_1_data = (
    [(1 + random.random(), "EMbox", [random.randint(250,750), -40], 5, 90) for i in range(5)] +
    [(2 + random.random(), "EMbox", [random.randint(250,750), -40], 5, 90) for i in range(5)] +
    [(3 + random.random(), "EMbox", [random.randint(250,750), -40], 5, 90) for i in range(5)] +
    [(4 + random.random(), "yinyangright", [1200, 100 + random.randint(-10,600)], 10 + random.randint(-2,2), 190) for i in range(7)] +
    [(5 + random.random(), "yinyangright", [1200, 100 + random.randint(-10,600)], 10 + random.randint(-2,2), 190) for i in range(7)] +
    [(6 + random.random(), "yinyangright", [1200, 100 + random.randint(-200,600)], 10 + random.randint(-2,2), 190) for i in range(10)] +
    [(7.4 + random.random(), "yinyangleft", [-200, 100 + random.randint(-200,600)], 10 + random.randint(-2,2), 350) for i in range(10)] +
    [(8 + random.random(), "yinyangleft", [-200, 100 + random.randint(-200,600)], 10 + random.randint(-2,2), 350) for i in range(10)] +
    [(9 + random.random(), "yinyangleft", [-200, 100 + random.randint(-200,600)], 10 + random.randint(-2,2), 350) for i in range(10)] +
    [(10 + random.random(), "yinyang", [random.randint(100,1500), -40], 7 + random.randint(-2,2), 110) for i in range(35)] +
    [(random.randint(11,14) + random.random(), "EMbox", [random.randint(250,750), -40], 5, 90) for i in range(10)] +
    [(14 + random.random(), "yinyang", [random.randint(100,1500), -40], 10 + random.randint(-2,2), 110) for i in range(30)] +
    [(random.randint(16,18) + random.random(), "EMbox", [random.randint(250,750), -40], 5, 90) for i in range(10)] +
    [(random.randint(16,18), "yinyang", [1050, random.randint(250,750)], 6 + random.randint(-2,2), 170) for i in range(5)] +
    [(random.randint(16,18), "yinyang", [-50, random.randint(250,750)], 6 + random.randint(-2,2), 10) for i in range(5)] +
    [(19 + i/3, "EMyinyangevil", [1200, 50], 7, 160) for i in range(10)] +
    [(20 + i/2, "yinyang", [1200, 100+i*100], 4, 180) for i in range(10)] +
    [(20 + i/2, "yinyang", [-200, 100+i*100], 4, 0) for i in range(10)] +
    [(24 + i/3, "EMyinyangevil", [1200, 50], 5, 160) for i in range(8)] +
    [(28 + random.random(), "yinyangright", [1200, 100 + random.randint(-10,600)], 10 + random.randint(-2,2), 190) for i in range(10)] +
    [(31 + random.random(), "yinyang", [random.randint(100,1500), -40], 7 + random.randint(-2,2), 110) for i in range(35)] +
    [(33, "boss", 1)]
)
level_2_data = (
    [(2 + random.random(), "EMbox", [random.randint(50,950), -40], 5, 90) for i in range(5)] +
    [(random.randint(4,7), "yinyang", [random.randint(50,900), -40], 7 + random.randint(-2,2), 90) for i in range(50)] +
    [(8 + i/8, "yellowAccelerate", [50+i*50, -40], 4, 90) for i in range(20)] +
    [(10 + i/8, "yellowAccelerate", [950-i*50, -40], 4, 90) for i in range(20)] +
    [(12 + random.random(), "yinyangleft", [-200, 100 + random.randint(-200,600)], 10 + random.randint(-2,2), 350) for i in range(15)] +
    [(14+ i/18, "yellowRotate", [1100, 500], 8, 270-i*20) for i in range(18)] +
    [(16, "yellowRotate", [1100, 500], 8, 270-i*20) for i in range(9)] +
    [(14+ i/18, "yellowRotate", [-100, 500], 8, 270+i*20) for i in range(18)] +
    [(15, "yellowRotate", [-100, 500], 8, 270+i*20) for i in range(9)] +
    [(17 + i/3, "EMyinyangevil", [1200, 50], 6, 160) for i in range(8)] +
    [(19 + i/3, "EMyinyangevilLeft", [-100, 50], 6, 20) for i in range(8)] +
    [(23 + i/3, "EMyinyangevil", [500, -40], 6, 90) for i in range(8)] +
    [(23 + i/3, "EMyinyangevilLeft", [500, -40], 6, 90) for i in range(8)] +
    [(26 + random.random(), "EMbox", [random.randint(50,950), -40], 5, 90) for i in range(5)] +
    [(29 + i/8, "yellowAccelerateFollow", [50+i*50, -40], 4, 90) for i in range(23)] +
    [(29 + i/8, "yellowAccelerateFollow", [950-i*50, -40], 4, 90) for i in range(23)] +
    [(33.5, "boss", 2)]
    
)
level_3_data = (
    [(2 + random.random(), "EMbox", [random.randint(50,950), -40], 5, 90) for i in range(5)] +
    [(3 + i/8, "big", [100+i*250, -200], 5, 90) for i in range(4)] +
    [(4 + i/8, "big", [650-i*250, -200], 8, 90) for i in range(3)] +
    [(5 + i/15, "yinyangright", [1200, 100+i*130], 8, 200) for i in range(8)] +
    [(5.5  + i/10, "yinyangright", [1200, 900-i*150], 9, 220) for i in range(8)] +
    [(6.5  + i/20, "yinyangright", [1200, 100+i*180], 10, 200) for i in range(8)] +
    [(7.5, "big", [50+i*250, -200], 10, 90) for i in range(5)] +
    [(7.5, "big", [900-i*250, -200], 7, 90) for i in range(4)] +
    [(8.3, "big", [50+i*250, -200], 10, 90) for i in range(5)] +
    [(9.5 + random.random(), "yinyang", [random.randint(50,950), -40], 7 + random.randint(-2,2), 90) for i in range(40)] +
    [(10.3 + i/6, "big", [random.randint(-100,1000), -200], 7 + random.randint(-3,3), 90) for i in range(7)] +
    [(10.8 + i/6, "big", [random.randint(-100,1000), -200], 7 + random.randint(-3,3), 90) for i in range(7)] +
    [(12 + i/3, "EMyinyangevil", [1200, 50], 6, 160) for i in range(8)] +
    [(12.5 + i/3, "EMyinyangevilLeft", [-200, 50], 6, 20) for i in range(8)] +
    [(16 + i/10, "yellowAccelerate", [50+i*90, -40], 4, 100) for i in range(20)] +
    [(16 + i/10, "yellowAccelerate", [950-i*90, -40], 4, 80) for i in range(20)] +
    [(18, "bigAccelerate", [100+i*250, -200], 8, 90) for i in range(4)] +
    [(18.5, "bigAccelerate", [50+i*250, -200], 10, 90) for i in range(5)] +
    [(19, "bigAccelerate", [100+i*250, -200], 13, 90) for i in range(4)] +
    [(19.5, "bigAccelerate", [50+i*250, -200], 15, 90) for i in range(5)] +
    [(20 + i/2, "EMyinyangevil", [1200, 50], 5, 160) for i in range(8)] +
    [(20 + random.random(), "EMbox", [random.randint(50,950), -40], 5, 90) for i in range(7)] +
    [(21 + i/3, "EMyinyangevilLeft", [-200, 50], 6, 20) for i in range(8)] +
    [(25.5, "bigAccelerate", [-200, 100+i*300], 8, 0) for i in range(4)] +
    [(26, "bigAccelerate", [1200, 0+i*300], 10, 180) for i in range(5)] +
    [(28 + i/3, "EMyinyangevil", [400, -40], 6, 90) for i in range(10)] +
    [(28 + i/3, "EMyinyangevilLeft", [600, -40], 6, 90) for i in range(10)] +
    [(28 + i/3, "EMyinyangevil", [1200, 50], 5, 160) for i in range(8)] +
    [(28.5 + i/3, "EMyinyangevilLeft", [-200, 50], 6, 20) for i in range(8)] +
    [(34, "boss", 3)]
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
        self.y = 800
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
    if stage == 1:
        backgroundIMG = stage1backdrop
    elif stage == 2 and stageCount > 70:
        backgroundIMG = stage2backdrop
    elif stage == 3 and stageCount > 70:
        backgroundIMG = stage3backdrop
    elif stage == 3:
        backgroundIMG = stage2backdrop
    elif stage == 4 and stageCount < 80:
        backgroundIMG = stage3backdrop
    else:
        backgroundIMG = stage1backdrop

    if not (stage == 4 and stageCount >= 80):
        DISPLAYSURF.blit(backgroundIMG, (0, backgroundY))
        DISPLAYSURF.blit(backgroundIMG, (0, backgroundY-950))
    if stage != 4:
        if stageCount % 60 == 0:
            particles.append(Particle("bushLeft",[100,-600],7,90,len(particles)))
            particles.append(Particle("bushRight",[900,-600],7,90,len(particles)))

    # Boss ==========================
    boss.render()
    if DEBUG and boss.level > 0:
        pygame.draw.rect(DISPLAYSURF, (0,255,0) , boss.rect)
    #enemies collide
    for enemy in enemies:
        if enemy.hitcooldown < 2:
            enemy.hitcooldown += 1
        if enemy.typeBullet[:13] == "EMyinyangevil":
            if enemy.cooldown == 30:
                enemy.cooldown = 0
                enemy.attack()
            elif enemy.cooldown < 30:
                enemy.cooldown += 1

        removedBullet = False
        if pygame.sprite.spritecollide(enemy,player.playerBullets,False,pygame.sprite.collide_rect_ratio(1)) and enemy.hitcooldown == 2 or bombing > 0:
            enemy.hp -= 1
            enemy.hitcooldown = 0
            if enemy.hp <= 0:
                enemyDestroyed = enemy.destroy()
                removedBullet = True
        elif enemy.position[1] > DESPWANRANGE[0] or enemy.position[1] < DESPWANRANGE[1] or enemy.position[0] > DESPWANRANGE[0] or enemy.position[0] < DESPWANRANGE[1]:
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
            pygame.draw.rect(DISPLAYSURF, (0,0,255) , item.rect)
        item.render()
        removed = False
        if pygame.sprite.collide_circle_ratio(3)(item,player):
            itemDestroyed = item.destroy()
            removed = True
            if item.itemType == "life":
                particles.append(Particle("life",item.position[:],10,math.degrees(math.atan2(player.y-item.position[1],player.x-item.position[0])),len(particles)))
                if lives < 8:
                    lives += 1
            elif item.itemType == "bomb":
                particles.append(Particle("bomb",item.position[:],10,math.degrees(math.atan2(player.y-item.position[1],player.x-item.position[0])),len(particles)))
                if bombs < 8:
                    bombs += 1
            elif item.itemType == "points":
                particles.append(Particle("points",item.position[:],10,math.degrees(math.atan2(player.y-item.position[1],player.x-item.position[0])),len(particles)))
                points += 100
        elif item.position[1] > DESPWANRANGE[0]:
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
            for i in range(3):
                particles.append(Particle("shread",bullet.position[:],7,random.randint(0,180),len(particles)))
            bulletDestroyed = bullet.destroy()
            removedBullet = True
        elif boss.level > 0:
            if pygame.sprite.collide_rect(bullet,boss):
                for i in range(3):
                    particles.append(Particle("shread",bullet.position[:],7,random.randint(0,180),len(particles)))
                boss.health -= 1
                bulletDestroyed = bullet.destroy()
                removedBullet = True
                if boss.health < 1:
                    boss.bossReady = False
        elif bullet.position[1] < DESPWANRANGE[1]:
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
        if bullet.position[1] > DESPWANRANGE[0] or bullet.position[1] < DESPWANRANGE[1] or bullet.position[0] > DESPWANRANGE[0] or bullet.position[0] < DESPWANRANGE[1] or bombing > 0:
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
        
    for particle in particles:
        particle.move()
        if DEBUG:
            pygame.draw.rect(DISPLAYSURF, (0,0,255) , particle.rect)
        particle.render()
        removed = False
        if particle.position[1] > DESPWANRANGE[0] or particle.life < 0:
            particleDestroyed = particle.destroy()
            removed = True
        if removed:
            for newID in particles[particleDestroyed:]:
                newID.index = newID.index-1       
     
    if focus == True:
        displayIMGPlayer(playerHitbox)
    if stageCount == 0 and stage > 1:
        particles.append(Particle("transition",[-2000,475],30,0,len(particles)))
    if stage < 4:
        if stageCount <= 100:
            textDisplay = bigText.render(f"Stage {stage}", False, (255,255,255))
            DISPLAYSURF.blit(textDisplay, (stageCount-50,50))
        elif 100 < stageCount <= 150:
            textDisplay = bigText.render(f"Stage {stage}", False, (255,255,255))
            DISPLAYSURF.blit(textDisplay, (50,50))
        elif 150 < stageCount < 250:
            textDisplay = bigText.render(f"Stage {stage}", False, (255,255,255))
            DISPLAYSURF.blit(textDisplay, (50-((stageCount-150)*4),50))
    

############################################################################################################
############################################################################################################
# CLASSES & EXTRA FUNCTIONS
############################################################################################################
############################################################################################################
class Particle(pygame.sprite.Sprite):
    def __init__(self, particleType, pos, velocity, angle, index):
        self.particleType = particleType
        self.position = pos[:]
        self.velocity = velocity
        self.index = index
        self.angle = angle
        self.diameter = 30
        self.life = 5
        if self.particleType == "bushLeft":
            if stage > 2:
                self.img = bamboodarkBushSprite
            else:
                self.img = bambooBushSprite
        elif self.particleType == "bushRight":
            if stage > 2:
                self.img = bamboodarkBushSpriteRight
            else:
                self.img = bambooBushSpriteRight
        elif self.particleType == "bomb":
            self.img = bombSprite
        elif self.particleType == "points":
            self.img = pointsSprite
        elif self.particleType == "life":
            self.img = liveSprite
        elif self.particleType == "transition":
            self.img = transitionSprite
            self.life = 600
        else:
            self.img = particleSprite
        
        self.rect = Rect(self.position[0]-self.diameter/2, self.position[1]-self.diameter/2, self.diameter, self.diameter)

    def move(self):
        self.position[0] += math.cos(math.radians(self.angle))*self.velocity
        self.position[1] += math.sin(math.radians(self.angle))*self.velocity
        self.rect.update([self.position[0]-self.diameter/2, self.position[1]-self.diameter/2], [self.diameter,self.diameter])
        if self.particleType in ["shread", "bomb", "points", "life"]:
            self.life -= 1
        if self.particleType == "transition" and self.position[0] > 1100+self.img.get_width():
            self.life = -1
    
    def render(self):
        self.selfDraw(self.img)
    def selfDraw(self, img):
        DISPLAYSURF.blit(img, (self.position[0] - img.get_width()/2, self.position[1] - img.get_height()/2))
    def destroy(self):
        particles.pop(self.index)
        return self.index

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, typeBullet, playerPos, velocity, angle, index):
        self.typeBullet = typeBullet
        self.position = playerPos[:]
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
        self.position = pos[:]
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
        self.position = startPos[:]
        self.velocity = velocity
        self.index = index
        self.angle = angle
        if self.typeBullet == "yellowAccelerateFollow":
            self.angle = math.degrees(math.atan2(player.y-self.position[1],player.x-self.position[0]))
        if self.typeBullet[:2] == "EM":
            self.hitcooldown = 0
            if self.typeBullet[2:] == "box":
                self.hp = 1
            elif self.typeBullet in ["EMyinyangevil", "EMyinyangevilLeft"]:
                self.hp = 5
                self.cooldown = 0
        if self.typeBullet == "basic":
            self.sprite = basicBullet
        elif self.typeBullet in ["yellowbasic", "yellowAccelerate", "yellowRotate", "yellowAccelerateFollow"]:
            self.sprite = yellowbullet
        elif self.typeBullet == "yellowbeam":
            self.sprite = yellowbeam
        elif self.typeBullet == "bamboo":
            self.sprite = bambooSprite
        elif self.typeBullet == "EMbox":
            self.sprite = boxSprite
        elif self.typeBullet[:3] == "big":
            self.sprite = bigBullet
        elif self.typeBullet[:7] == "yinyang" or self.typeBullet[:13] == "EMyinyangevil":
            self.sprite = evilyinyangSprite
            self.visableRotation = 0
            if self.typeBullet[:13] == "EMyinyangevil":
                self.sprite = eMyinyang
        else:
            self.sprite = basicBullet
        
        if self.typeBullet == "bamboo":
            self.diameter = 28
            self.rect = Rect(self.position[0]-self.diameter/2, self.position[1]-self.diameter/2, self.diameter, self.diameter)
        elif self.typeBullet[:7] == "yinyang" or self.typeBullet in ["EMyinyangevil", "EMbox", "EMyinyangevilLeft"]:
            self.diameter = 40
            self.rect = Rect(self.position[0]-self.diameter/2, self.position[1]-self.diameter/2, self.diameter, self.diameter)
        elif self.typeBullet in ["basic","yellowbasic","yellowAccelerate", "yellowRotate", "yellowAccelerateFollow"]:
            self.diameter = 25
            self.rect = Rect(self.position[0]-self.diameter/2, self.position[1]-self.diameter/2, self.diameter, self.diameter)
        elif self.typeBullet[:3] == "big":
            self.diameter = 128
            self.rect = Rect(self.position[0]-self.diameter/2, self.position[1]-self.diameter/2, self.diameter, self.diameter)

    def move(self):
        self.position[0] += math.cos(math.radians(self.angle))*self.velocity
        self.position[1] += math.sin(math.radians(self.angle))*self.velocity
        self.rect.update([self.position[0]-self.diameter/2, self.position[1]-self.diameter/2], [self.diameter,self.diameter])
        if self.typeBullet[:16] == "yellowAccelerate":
            self.velocity += 0.02
        elif self.typeBullet == "bigAccelerate":
            self.velocity += 0.1
        elif self.typeBullet == "yinyangright" or self.typeBullet ==  "yellowRotate":
            self.angle -= 0.5
        elif self.typeBullet == "yinyangleft":
            self.angle += 0.5
        elif self.typeBullet == "EMyinyangevil":
            self.angle += 0.2
        elif self.typeBullet == "EMyinyangevilLeft":
            self.angle -= 0.2
        if self.typeBullet[:7] == "yinyang":
            self.visableRotation += 10
        elif self.typeBullet[:13] == "EMyinyangevil":
            self.visableRotation += 5

    
    def render(self):
        if self.typeBullet[:7] == "yinyang" or self.typeBullet[:13] == "EMyinyangevil":
            self.selfDraw(pygame.transform.rotate(self.sprite, self.visableRotation))
        else:
            self.selfDraw(self.sprite)
            
        
    def selfDraw(self, img):
        if self.typeBullet == "bamboo":
            DISPLAYSURF.blit(img, (self.position[0] - img.get_width()/2, self.position[1] - img.get_height()))
        else:
            DISPLAYSURF.blit(img, (self.position[0] - img.get_width()/2, self.position[1] - img.get_height()/2))

    def destroy(self):
        for i in range(5):
            particles.append(Particle("shread",self.position[:],7,(0 + i*72)+random.randint(-5,5),len(particles)))
        if self.typeBullet[:2] == "EM":
            if self.typeBullet == "EMbox":
                getPoints = random.randint(0,6)
                if getPoints == 0:
                    items.append(Item("bomb", self.position[:], -3, len(items)))
                else:
                    pointsAmount = random.randint(3,8)
                    for i in range(pointsAmount):
                        items.append(Item(random.choice(["points"]), [self.position[0]+ random.randint(-50,50),self.position[1]+ random.randint(-20,50)], -3, len(items)))
            elif self.typeBullet[:13] == "EMyinyangevil":
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
        if self.typeBullet[:13] == "EMyinyangevil":
            self.addBullet("basic", self.position[:], 8, math.degrees(math.atan2(player.y-200,player.x-500)))
    
    def addBullet(self, btype, pos, vel, angle):
        enemyBullets.append(EnemyBullet(btype, pos, vel, angle,len(enemyBullets)))

#===========================================================================================================
# Boss
#===========================================================================================================

class Boss(pygame.sprite.Sprite):
    def __init__(self, level):
        self.level = level
        self.bossReady = False
        self.health = 999
        self.rect = Rect(-1000,-1000, 0, 0)
        if level > 0:
            self.position = [500, -60]
            self.velocity = 0
            self.health = 999
            self.maxV = [10,10]
            self.diameter = 70
            self.maxSpeed = 5
            self.rect = Rect(self.position[0],self.position[1], 70, 70)
            self.rect.update([self.position[0]-self.diameter/2, self.position[1]-self.diameter/2], [self.diameter,self.diameter])
            if self.level == 1:
                self.health = 800 
            elif self.level == 2:
                self.health = 1500 
            elif self.level == 3:
                self.health = 2000  
    
    def fancyGotoPos(self, target, ogPos, NumBssAtks, startEndTime): 
        angleTowards = math.atan2(ogPos[1]-target[1],ogPos[0]-target[0])
        ogDist = math.sqrt((ogPos[0] - target[0])**2 + (ogPos[1] - target[1])**2) #pythagoras to find hypotenuse
        currDist = math.sqrt((boss.position[0] - target[0])**2 + (boss.position[1] - target[1])**2) #pythagoras to find hypotenuse
        
        speedChangetime = ((self.maxSpeed+1)*self.maxSpeed)/2
        if NumBssAtks > startEndTime[0] and NumBssAtks < startEndTime[1]:
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
            return boss.position[:]
        else:
            return ogPos
    
    def render(self):
        if self.level == 1:
            self.selfDraw(hanSprite)
        elif self.level == 2:
            self.selfDraw(qiSprite)
        elif self.level == 3:
            self.selfDraw(harukiSprite)
        
    def selfDraw(self, img):
        DISPLAYSURF.blit(img, (self.position[0] - img.get_width()/2, self.position[1] - img.get_height()/2))
        
    #==========================
    # Boss Special Attacks
    #==========================
    def bossAttack(self, special):
        if self.level == 1:
            if special == 0:
                for i in range(3):
                    self.addBullet("basic", self.position[:], 8, math.degrees(math.atan2(player.y-self.position[1],player.x-self.position[0]))-30+i*30)
            elif special == 1:
                for i in range(4):
                    self.addBullet("basic", [random.randint(10,990),-30], 5, math.degrees(math.atan2(player.y-self.position[1],player.x-self.position[0])))
            elif special == 2:
                for i in range(2):
                    self.addBullet("basic", [-20,50+i*300], 5, 20+i*5+random.randint(0,15))
                for i in range(2):
                    self.addBullet("basic", [1020,100+i*300], 5, 160-i*5-random.randint(0,15))
        elif self.level == 2:
            if special == 0:
                for i in range(5):
                    self.addBullet("yellowbasic", self.position[:], 5, math.degrees(math.atan2(player.y-self.position[1],player.x-self.position[0]))-30+i*30)
                
            elif special == 1:
                self.addBullet("yellowAccelerate", [700, -15], 1, random.randint(60,120))
                self.addBullet("yellowAccelerate", [500, -15], 1, random.randint(60,120))
                self.addBullet("yellowAccelerate", [300, -15], 1, random.randint(60,120))
                
            elif special == 2:
                for i in range(18):
                    self.addBullet("yellowRotate", self.position[:], 8, math.degrees(math.atan2(player.y-self.position[1],player.x-self.position[0]))+i*20)
        elif self.level == 3:
            if special == 0:
                for i in range(5):
                    self.addBullet("big", self.position[:], 5, math.degrees(math.atan2(player.y-self.position[1],player.x-self.position[0]))-30+i*30)
            elif special == 1:
                for i in range(5):
                    self.addBullet("big", self.position[:], 5, math.degrees(math.atan2(player.y-self.position[1],player.x-self.position[0]))+i*72)
                enemies.append(EnemyBullet("EMyinyangevil", [1200,50],12, 170, len(enemies)))
            elif special == 2:
                for i in range(5):
                    self.addBullet("big", [0+i*300,-200], random.randint(3,5), 90)
                enemies.append(EnemyBullet("EMyinyangevilLeft", [-200,50],12, 10, len(enemies)))
                    
                    
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
        return level_1_data.copy() #Format for each item (time, bullet type,position,velocity,angle/direction)...
    if stage == 2:
        return level_2_data.copy()
    if stage == 3:
        return level_3_data.copy()
    else:
        return []


############################################################################################################
# EXTRA FUNCTIONS
############################################################################################################

def dialogueHandler(dialogueTree, dialogueTreeName, dialogue):
    if dialogue-1 < len(dialogueTree):
        dialogue = doDialogue(dialogueTreeName, dialogue-1, dialogueTree)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    dialogue +=1
        return (dialogue, True)
    return (dialogue, False)

def menuGetColour(id):
    if menuSelect == id:
        return (255,255,0)
    else: 
       return (255,255,255)

def setMusic(song):
    MUSIC.load(f'PygameGame/{song}.mp3')
    MUSIC.play(-1)
    MUSIC.set_volume(0.5)

def setState(state, currstate):
    if state in [0,2] and currstate not in [0,2] and stage <4:
        setMusic("LandOfTheLostFog")
    elif state == 1:
        if stage == 1:
            setMusic("Stage1Theme")
        elif stage == 2:
            setMusic("Stage2Theme")
        elif stage == 3:
            setMusic("Stage3Theme")
    elif state == 2 and stage == 4:
        setMusic("endCredits")
    return state

def doDialogue(level, textID, dialogueTree):
    currDia = dialogueTree[textID]
    textpos = [220,700]
    if textID < len(dialogueTree):
        textDisplay = dialogueText.render(currDia[2], False, (255,255,255))
        DISPLAYSURF.blit(PORTRAITS[currDia[0]][currDia[1]],(textpos[0]-200,textpos[1]-50))
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
            DISPLAYSURF.blit(titleBackdrop, (0, 0))
            DISPLAYSURF.blit(titleBox, (65, 20))
            DISPLAYSURF.blit(titleWords, (120, 50))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if menuSelect > 0:
                            menuSelect -=1
                        else:
                            menuSelect = 1
                    if event.key == pygame.K_DOWN:
                        if menuSelect < 1:
                            menuSelect +=1
                        else:
                            menuSelect = 0
                    if event.key == pygame.K_z:
                        if menuSelect == 0:
                            #reset variables
                            backgroundY = 0
                            pause = False
                            enemyBullets = []
                            enemies.clear()
                            items.clear()
                            particles = []
                            bulletCooldownTimer = 4
                            bombCooldownTimer = 4
                            lives = 5
                            bombs = 3
                            if DEBUG:
                                lives = 99
                                bombs = 99
                            points = 0
                            bombing = 0
                            stage = 1
                            stageCount = 0
                            bossbulletCooldownTimer = 0
                            bosscdthreshold = 20
                            numBossattacks = 0
                            ogPos = [0,0]
                            menuSelect = 0
                            inputCooldown = 10
                            playerInvincability = 0
                            dialogue = [0, False]
                            boss = Boss(0)
                            gameState = setState(1, gameState)
                        if menuSelect == 1:
                            pygame.event.post(pygame.event.Event(pygame.QUIT))
        
            menutext = ["Story", "Exit"]
            for textNum in range(len(menutext)):
                textDisplay = text.render(menutext[textNum], False, menuGetColour(textNum))
                DISPLAYSURF.blit(textDisplay, (700,300+textNum*100))
            
            if inputCooldown < 10:
                inputCooldown += 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
        
        ############################################################################################################
        # MAIN GAMEPLAY
        ############################################################################################################
        case 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause = not pause
                        menuSelect = 0
                    if pause:
                        if event.key == pygame.K_UP:
                            if menuSelect > 0:
                                menuSelect -=1
                            else:
                                menuSelect = 2
                        if event.key == pygame.K_DOWN:
                            if menuSelect < 2:
                                menuSelect +=1
                            else:
                                menuSelect = 0
                        if event.key == pygame.K_z:
                            if menuSelect == 0:
                                pause = not pause
                            elif menuSelect == 1:
                                gameState = setState(0, gameState)
                            elif menuSelect == 2:
                                pygame.quit()
                                sys.exit()
            if pause:
                textDisplay = bigText.render("Paused", False, (255,255,255))
                DISPLAYSURF.blit(textDisplay, (50,50))
                menutext = ["Continue", "Main Menu", "Exit"]
                for textNum in range(len(menutext)):
                    textDisplay = text.render(menutext[textNum], False, menuGetColour(textNum))
                    DISPLAYSURF.blit(textDisplay, (700,300+textNum*100))
            if not pause:
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
                if boss.bossReady:
                    if bombing > 0:
                        boss.health -= 10
                        if boss.health < 1:
                            boss.bossReady = False
                    if bossbulletCooldownTimer == bosscdthreshold:
                        #Attacks===============
                        if boss.level == 1:
                            if numBossattacks % 40 < 15 and 100 < numBossattacks < 150:
                                boss.bossAttack(0)
                                bossbulletCooldownTimer = 0
                            elif numBossattacks and 200 < numBossattacks < 220:
                                boss.bossAttack(1)
                                bossbulletCooldownTimer = 0 
                            elif numBossattacks % 40 < 5 and 220 < numBossattacks < 230:
                                boss.bossAttack(0)
                                bossbulletCooldownTimer = 0 
                            elif numBossattacks % 40 < 5 and 230 < numBossattacks < 250:
                                boss.bossAttack(2)
                                bossbulletCooldownTimer = 0     
                            elif numBossattacks > 250:
                                bosscdthreshold = 20
                                numBossattacks = 1
                        elif boss.level == 2:
                            if numBossattacks % 40 < 15 and 100 < numBossattacks < 350:
                                boss.bossAttack(0)
                                bossbulletCooldownTimer = 0

                            elif numBossattacks and 350 < numBossattacks < 400:
                                boss.bossAttack(1)
                                bossbulletCooldownTimer = 0 
                            elif numBossattacks % 40 < 5 and 400 < numBossattacks < 450:
                                boss.bossAttack(0)
                                bossbulletCooldownTimer = 0 
                            elif numBossattacks % 40 < 5 and 450 < numBossattacks < 650:
                                boss.bossAttack(2)
                                bossbulletCooldownTimer = 0     
                            elif numBossattacks > 650:
                                bosscdthreshold = 20
                                numBossattacks = 1
                        elif boss.level == 3:
                            if numBossattacks % 40 < 15 and 100 < numBossattacks < 200:
                                bosscdthreshold = 60
                                boss.bossAttack(0)
                                bossbulletCooldownTimer = 0

                            elif numBossattacks and 200 < numBossattacks < 300:
                                boss.bossAttack(1)
                                bossbulletCooldownTimer = 0 
                            elif numBossattacks % 40 < 5 and 300 < numBossattacks < 400:
                                boss.bossAttack(0)
                                bossbulletCooldownTimer = 0 
                            elif numBossattacks % 40 < 5 and 500 < numBossattacks < 600:
                                boss.bossAttack(2)
                                bossbulletCooldownTimer = 0     
                            elif numBossattacks > 600:
                                bosscdthreshold = 20
                                numBossattacks = 1

                        numBossattacks +=1
                    if bossbulletCooldownTimer < bosscdthreshold:
                        bossbulletCooldownTimer += 1
                    #Moving=================
                    if boss.level == 1:
                        ogPos = boss.fancyGotoPos([boss.position[0], 120], ogPos, numBossattacks, [0, 100])
                    elif boss.level == 2:
                        ogPos = boss.fancyGotoPos([500, 120], ogPos, numBossattacks, [0, 100])
                        ogPos = boss.fancyGotoPos([200, boss.position[1]], ogPos, numBossattacks, [100, 200])
                        ogPos = boss.fancyGotoPos([800, boss.position[1]], ogPos, numBossattacks, [200, 320])
                        ogPos = boss.fancyGotoPos([500, boss.position[1]], ogPos, numBossattacks, [320, 420])
                    elif boss.level == 3:
                        ogPos = boss.fancyGotoPos([500, 120], ogPos, numBossattacks, [0, 100])
                        ogPos = boss.fancyGotoPos([200, boss.position[1]], ogPos, numBossattacks, [100, 150])
                        ogPos = boss.fancyGotoPos([800, boss.position[1]], ogPos, numBossattacks, [150, 200])
                        ogPos = boss.fancyGotoPos([500, boss.position[1]], ogPos, numBossattacks, [250, 300])
                        ogPos = boss.fancyGotoPos([200, boss.position[1]], ogPos, numBossattacks, [350, 400])
                        ogPos = boss.fancyGotoPos([800, boss.position[1]], ogPos, numBossattacks, [400, 450])
                        ogPos = boss.fancyGotoPos([800, 600], ogPos, numBossattacks, [450, 480])
                        ogPos = boss.fancyGotoPos([200, 100], ogPos, numBossattacks, [480, 510])
                        ogPos = boss.fancyGotoPos([500, 500], ogPos, numBossattacks, [510, 600])

                #==========================
                # Per Loop Updates
                #==========================
                if playerInvincability == 0:
                    if (pygame.sprite.spritecollide(player,enemyBullets,False,pygame.sprite.collide_circle_ratio(1)) or 
                            pygame.sprite.spritecollide(player,enemies,False,pygame.sprite.collide_circle_ratio(1)) or 
                            pygame.sprite.collide_rect(player, boss)):
                        for i in range(5):
                            particles.append(Particle("shread",[player.x,player.y],7,(0 + i*72)+random.randint(-5,5),len(particles)))
                        if bombs > 3:
                            items.append(Item("bomb", [player.x,player.y-100], -3, len(items)))
                        player.x = 500
                        player.y = 800
                        lives -= 1
                        playerInvincability = 120

                        for i in range(5):
                            particles.append(Particle("shread",[player.x,player.y],7,(0 + i*72)+random.randint(-5,5),len(particles)))
                        if lives == 0:
                            menuSelect = 0
                            gameState = setState(2, gameState)
                        bombs = 3
                elif playerInvincability > 0:
                    playerInvincability -=1

                bulletCooldownTimer += 1
                bombCooldownTimer += 1

                updateGraphics()
                stageCount +=1  


                if boss.bossReady:
                    textDisplay = text.render(f"Boss Health: {boss.health}", False, (255,255,255))
                    DISPLAYSURF.blit(textDisplay, (50,50))

                if not boss.bossReady:
                    if stage == 1:
                        if initBoss == "BossInit":
                            numBossattacks = 0
                            setMusic("HanTheme")
                            dialogue = [1, True]
                            dialogueDone = doDialogue("DIALOGUEBOSS1", 0, DIALOGUEBOSS1)
                            playerInvincability = 1

                        if boss.health > 0 and dialogue[0] > 0: # Begin Stage 1 boss
                            dialogue = dialogueHandler(DIALOGUEBOSS1, "DIALOGUEBOSS1",dialogue[0])
                            playerInvincability = 1
                            if not dialogue[1]:
                                boss = Boss(1)
                                boss.bossReady = True
                                dialogue = [0, True]
                        elif boss.health < 1 and dialogue[0] == 0: #End Stage 1 boss
                            dialogue = [1, True]
                            dialogueDone = doDialogue("DIALOGUEBOSS1END", 0, DIALOGUEBOSS1END)
                            playerInvincability = 1

                        if boss.health < 1 and dialogue[0] > 0:
                            dialogue = dialogueHandler(DIALOGUEBOSS1END, "DIALOGUEBOSS1END",dialogue[0])    
                            playerInvincability = 1  
                            bombing = 2
                            if not dialogue[1]:
                                dialogue = [0, False]
                                stage = 2
                                stageCount = 0       
                                boss = Boss(0)
                                setMusic("Stage2Theme")
                    elif stage == 2:
                        if initBoss == "BossInit":
                            numBossattacks = 0
                            setMusic("QiTheme")
                            dialogue = [1, True]
                            dialogueDone = doDialogue("DIALOGUEBOSS2", 0, DIALOGUEBOSS2)
                            playerInvincability = 1

                        if boss.health > 0 and dialogue[0] > 0: # Begin Stage 2 boss
                            dialogue = dialogueHandler(DIALOGUEBOSS2, "DIALOGUEBOSS2",dialogue[0])
                            playerInvincability = 1
                            if not dialogue[1]:
                                boss = Boss(2)
                                boss.bossReady = True
                                dialogue = [0, True]
                        elif boss.health < 1 and dialogue[0] == 0: #End Stage 2 boss
                            dialogue = [1, True]
                            dialogueDone = doDialogue("DIALOGUEBOSS2END", 0, DIALOGUEBOSS2END)
                            bombing = 2
                            playerInvincability = 1
                            boss.bossReady = False

                        if boss.health < 1 and dialogue[0] > 0:
                            dialogue = dialogueHandler(DIALOGUEBOSS2END, "DIALOGUEBOSS2END",dialogue[0])    
                            playerInvincability = 1                    
                            if not dialogue[1]:
                                dialogue = [0, False]
                                stage = 3
                                stageCount = 0       
                                boss = Boss(0)
                                setMusic("Stage3Theme")
                    elif stage == 3:
                        if initBoss == "BossInit":
                            numBossattacks = 0
                            setMusic("HarukiTheme")
                            dialogue = [1, True]
                            dialogueDone = doDialogue("DIALOGUEBOSS3", 0, DIALOGUEBOSS3)
                            playerInvincability = 1

                        if boss.health > 0 and dialogue[0] > 0: # Begin Stage 3 boss
                            dialogue = dialogueHandler(DIALOGUEBOSS3, "DIALOGUEBOSS3",dialogue[0])
                            playerInvincability = 1
                            if not dialogue[1]:
                                boss = Boss(3)
                                boss.bossReady = True
                                dialogue = [0, True]
                        elif boss.health < 1 and dialogue[0] == 0: #End Stage 3 boss
                            dialogue = [1, True]
                            dialogueDone = doDialogue("DIALOGUEBOSS3END", 0, DIALOGUEBOSS3END)
                            bombing = 2
                            playerInvincability = 1
                            boss.bossReady = False

                        if boss.health < 1 and dialogue[0] > 0:
                            dialogue = dialogueHandler(DIALOGUEBOSS3END, "DIALOGUEBOSS3END",dialogue[0])    
                            playerInvincability = 1                    
                            if not dialogue[1]:
                                dialogue = [0, False]
                                stage = 4
                                stageCount = 0
                                boss = Boss(0)
                                menuSelect = 0
                                gameState = setState(2, gameState)

                for i in range(lives):
                    DISPLAYSURF.blit(liveSprite, (20 + i* 50, 880))
                for i in range(bombs):
                    DISPLAYSURF.blit(bombSprite, (940 - i*50, 880))
                if bombing > 0:
                    bombing -=1

                if backgroundY < 950:
                    backgroundY +=3
                else:
                    backgroundY = 0

                textDisplay = text.render(f"Points: {points}", False, (255,255,255))
                DISPLAYSURF.blit(textDisplay, (750,50))

                if DEBUG:
                    textDisplay = text.render(f"BossReady: {boss.bossReady}", False, (255,255,255))
                    DISPLAYSURF.blit(textDisplay, (20,100))
                    textDisplay = text.render(f"StageCount: {stageCount}", False, (255,255,255))
                    DISPLAYSURF.blit(textDisplay, (20,130))
                    textDisplay = text.render(f"BossAttacks: {numBossattacks}", False, (255,255,255))
                    DISPLAYSURF.blit(textDisplay, (20,160))
                    textDisplay = text.render(f"InitBoss: {initBoss}", False, (255,255,255))
                    DISPLAYSURF.blit(textDisplay, (20,190))
                    textDisplay = text.render(f"Dialogue: {dialogue}", False, (255,255,255))
                    DISPLAYSURF.blit(textDisplay, (20,220))
                    textDisplay = text.render(f"Num of entities: {len(items)+len(enemies)+len(enemyBullets)+len(player.playerBullets)+len(particles)}", False, (255,255,255))
                    DISPLAYSURF.blit(textDisplay, (20,250))
                    textDisplay = text.render(f"Game State: {gameState}", False, (255,255,255))
                    DISPLAYSURF.blit(textDisplay, (20,280))
                    textDisplay = text.render(f"Num of Items: {len(items)}", False, (255,255,255))
                    DISPLAYSURF.blit(textDisplay, (650,100))
                    textDisplay = text.render(f"Num of Enemies: {len(enemies)}", False, (255,255,255))
                    DISPLAYSURF.blit(textDisplay, (650,130))
                    textDisplay = text.render(f"Num of EBullets: {len(enemyBullets)}", False, (255,255,255))
                    DISPLAYSURF.blit(textDisplay, (650,160))
                    textDisplay = text.render(f"Num of PBullets: {len(player.playerBullets)}", False, (255,255,255))
                    DISPLAYSURF.blit(textDisplay, (650,190))
                    textDisplay = text.render(f"Num of Particles: {len(particles)}", False, (255,255,255))
                    DISPLAYSURF.blit(textDisplay, (650,220))
        case 2:
            if stage == 4:
                DISPLAYSURF.blit(victoryScreen, (0,0))
            else:
                DISPLAYSURF.blit(gameoverscreen, (0,0))
            if inputCooldown == 10:
                if keys[K_UP]:
                    if menuSelect > 0:
                        menuSelect -= 1
                    else:
                        menuSelect = 1
                    inputCooldown = 0
                elif keys[K_DOWN]:    
                    if menuSelect < 1:
                        menuSelect += 1
                    else:
                        menuSelect = 0
                    inputCooldown = 0
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_z:
                            if menuSelect == 0:
                                gameState = setState(0, gameState)
                            if menuSelect == 1:
                                pygame.event.post(pygame.event.Event(pygame.QUIT))
            
            menutext = ["Title", "Exit"]
            for textNum in range(len(menutext)):
                textDisplay = text.render(menutext[textNum], False, menuGetColour(textNum))
                DISPLAYSURF.blit(textDisplay, (700,300+textNum*100))
            textDisplay = text.render(f"Points: {points}", False, (255,255,255))
            DISPLAYSURF.blit(textDisplay, (100,800))
            
            if inputCooldown < 10:
                inputCooldown += 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
    pygame.display.update()
    fpsClock.tick(FPS)