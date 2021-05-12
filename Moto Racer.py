import pygame, random, sys
from pygame import *
# +++++++++++++++++++++++++    Variables     ++++++++++++++++++
screen = pygame.display.set_mode((450,600))
pygame.display.set_caption('Moto Racer - by Anurag')
icon = pygame.image.load('res/images/logo.ico')
pygame.display.set_icon(icon)
IMAGES = {}
SOUNDS = {}
obsy = obs2y = -250
bikex = 190
obs_list = []
obstacles = []
running =True
score = 0
with open('res/sysres','r') as r:
    highscore = int(r.readline())

# ++++++++++++++++++++++++    Functions  ++++++++++++++++++++
def welcomeScreen():
    global obstacles, obs_list,score
    score = 0
    bikex=190
    screen.blit(IMAGES['welcome'],(0,0))
    screen.blit(IMAGES['play'],(160,300))
    screen.blit(IMAGES['exit'],(160,400))
    hight = font3.render(f'HighScore : {highscore}',1,(0,0,230))
    screen.blit(hight,(125,250))
    screen.blit(IMAGES['bike'][0],(350,450))
    running = True
    obstacles.clear()
    obs_list.clear()
    while True:
        m_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and ((m_pos[0]>=160 and m_pos[1]>= 300) and (m_pos[0]<=260 and m_pos[1]<=340)):
                welOutro()
            if event.type == MOUSEBUTTONDOWN and ((m_pos[0]>=160 and m_pos[1]>= 400) and (m_pos[0]<=260 and m_pos[1]<=440)):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                welOutro()
            
        pygame.display.flip()
        pygame.display.update()       

def welOutro():
    outro = True
    bikey = 450
    vel=1
    pygame.mixer.music.play(-1)
    while True:
        screen.blit(IMAGES['welcome'],(0,0))
        screen.blit(IMAGES['bike'][0],(350,bikey))
        pygame.display.flip()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
        if bikey + IMAGES['bike'][0].get_height()-10 >=0 :
            bikey -= vel
        if bikey + IMAGES['bike'][0].get_height()-10 <=2 :
            bikey -= vel
            mainGame()
        vel+=0.1          

def mainGame():
    global obsy,bikex,running,score
    
    road1 = -200
    road2 = -1000
    vehicleVel = 5
    scoreIncrement = 1
    screen.blit(IMAGES['bike'][0], (bikex,500))
    obstacles.append(IMAGES['obs'][random.randint(0,4)])
    while running:
        
        screen.blit(IMAGES['road'],(0,road1))
        screen.blit(IMAGES['road'],(0,road2))
        road1+=vehicleVel
        road2+=vehicleVel
        if road1>=700:
            road1=-900
        if road2>=700:
            road2=-900

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
        keys = pygame.key.get_pressed()
        
        if keys[K_LEFT]:
            screen.blit(IMAGES['bike'][1], (bikex,475))
            bikex-=5
        elif keys[K_RIGHT]:
            screen.blit(IMAGES['bike'][2], (bikex,475))
            bikex+=5
        else:
            screen.blit(IMAGES['bike'][0], (bikex,475))
        
        if obsy>600:
            obstacles.clear()
            obstacles.append(IMAGES['obs'][random.randint(0,4)])
            obsy=-250
        get_obs(obstacles[0],obsy)
        obsy+=vehicleVel
        crashed = crashTest()
        score+=scoreIncrement
        showscore(score)
        if score == 200:
           
            vehicleVel=6
            scoreIncrement = 2
        if score == 500 or score == 501:
           
            vehicleVel = 8
            scoreIncrement = 4
        if 1000<score<1005:
           
            vehicleVel = 10
            scoreIncrement = 6
        if 2000 < score < 2010:
           
            vehicleVel = 12
            scoreIncrement = 8
        if 5000 < score < 5020:
            
            vehicleVel = 15
            scoreIncrement=10
            
        if crashed:
            
            gameOver()
            running = False
        
def get_obs(obs,obsy):
    try:
        if obsy==-250:
            # obs = IMAGES['obs'][random.randint(0,4)]        
            obs_x = random.randint(80,296)
            obs_list.clear()
            obs_list.append(obs_x)
        screen.blit(obs, (obs_list[0], obsy))
        pygame.display.update()
    except IndexError:
        obs_x = random.randint(80,270)
        obs_list.append(obs_x)
        screen.blit(obs, (obs_list[0], obsy))
        pygame.display.update()

def crashTest():
    global obstacles,obs_list,obsy,bikex
    if 0< obsy < 500:
        if obsy + obstacles[0].get_height() >475:
            if (bikex < obs_list[0] + obstacles[0].get_width()) and (bikex > obs_list[0]):
                return True
            elif (bikex +IMAGES['bike'][0].get_width() < obs_list[0] + obstacles[0].get_width()) and (bikex > obs_list[0]):
                return True
    if 75>bikex or bikex>366-IMAGES['bike'][0].get_width():
        bikex=190 
        return True
    else:
        return False

def gameOver():
    global crashtext,mess,score,highscore
    with open('res/sysres','r') as scorefile:
        highscore = int(scorefile.readline())
        if score>highscore:
            highscore = score
    with open('res/sysres','w') as scorefile:
        scorefile.write(f'{highscore}')  
    while True:
        screen.blit(crashtext,(60,250))
        screen.blit(mess,(120,330))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                welcomeScreen()
        pygame.display.update()

def showscore(score):
    global font2
    scoretext = font2.render(f'Score : {score}',1,(200,0,0))
    screen.blit(scoretext,(5,570))
    pygame.display.update()

# ++++++++++++++++++++++++++    Execute   +++++++++++++++++++++
if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    FPSCLOCK.tick(2)

    IMAGES['bike'] = [
        pygame.image.load('res/images/bike.png'),
        pygame.transform.rotate(pygame.image.load('res/images/bike.png'), 10),
        pygame.transform.rotate(pygame.image.load('res/images/bike.png'), 350)

    ]            
    IMAGES['road'] = pygame.image.load('res/images/road.png')
    IMAGES['welcome'] = pygame.image.load('res/images/welsc.jpg')
    IMAGES['play'] = pygame.image.load('res/images/play.png')
    IMAGES['exit'] = pygame.image.load('res/images/exit.png')
    IMAGES['obs'] = [
        pygame.image.load('res/images/bigtruckobs.png'),
        pygame.image.load('res/images/truckobs.png'),
        pygame.image.load('res/images/carobs.png'),
        pygame.image.load('res/images/pickupobs.png'),
        pygame.image.load('res/images/blockobs.png')]
    SOUNDS['bike'] = pygame.mixer.music.load('res/gfx/bikesound.mp3')
    font = pygame.font.SysFont('Gill Sans',60,True)
    font1 = pygame.font.SysFont('Gill Sans',32,True)
    font2 = pygame.font.SysFont('Berlin Sans FB', 20)
    font3 = pygame.font.SysFont('Berlin Sans FB', 30,True)
    crashtext = font.render('CRASHED!!',1,(200,90,90))
    mess = font1.render('Press Space.',1,(200,90,50))
    welcomeScreen()
