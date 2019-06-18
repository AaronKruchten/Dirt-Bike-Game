# framework created by Lukas Peraza
# taken from https://github.com/LBPeraza/Pygame-Asteroids/blob/
#master/pygamegame.py


from random import *
from math import *
import pygame
import time
import pickle
import subprocess
from tkinter import *
from tkinter import messagebox, simpledialog
import HomeScreenList

#from dialogs import *


class PygameGame(object):


    def init(self):
        # initializes variables only runs first time program is run
        # for all other restarts of the game we call reset
        self.mode = 'HomeScreen'
        self.gameWidth = self.width*5
        self.points = randomLine(self)
        self.gameWin = 'None'
        self.gameSpeed = 1 
        reset(self)
    
        
    
    def mousePressed(self, x, y):
        gamex1,gamey1 = 320,350
        gamex2,gamey2 = gamex1+ 220,gamey1 +100
        
        instructionsX1,instructionsX2,instructionsY1 = 50,270,350
        instructionsY2 = 450
        selectionBox2 = (420,120,360,160)
        selectionBox3 = (420,300,360,160)

        newGamex1 = 420
        newGamex2 = newGamex1 + 360
        newGamey1 = 120
        newGamey2 = newGamey1 + 160 
        newGamey3 = 300
        newGamey4 = newGamey3 + 160
        
        hx,hy,hx2,hy2 = 0,0,100,100
        
        editorX,editorY = 590,350
        editorX2,editorY2 = editorX + 220,editorY +100
        
        # load in a user created map
        if loadLevelMousePressed(self,x,y):
            pass
        
        # play button
        elif (gamex2 >= x >= gamex1 and 
            gamey2 >= y >= gamey1 and self.mode == 'HomeScreen'):
            self.mode = 'DialogBox'
        # start new game not loading in different map
        elif (newGamex2 >= x >= newGamex1 and 
            newGamey2 >= y >= newGamey1 and self.mode == 'DialogBox'):
            self.mode,self.points = 'game',randomLine(self)
            reset(self)
       
        # load instructions
        elif (instructionsX2 >= x >= instructionsX1 and 
            instructionsY2 >= y >= instructionsY1 and self.mode=='HomeScreen'):
            self.mode = 'instructions'
        
        # return to home screen from any screen
        elif hx2 >= x >= hx and hy2 >= y >= hy:
            self.gameWin = False
            reset(self)
            self.mode = 'HomeScreen'
        # level editor button on home screen
        elif (editorX2 >= x >= editorX 
            and editorY2 >= y >= editorY and self.mode == 'HomeScreen'):
            levelEditorMousePressed(self,x,y)
        
        # controls level editor mouse presses
        elif self.mode == 'LevelEditor':
            levelEditor(self,x,y)

        speedSelector(self,x,y)






    def keyPressed(self, keyCode, modifier):
        upArrowValue,downArrowValue,rightArrowValue,spaceBar = 273,274,275,32
        leftArrowValue = 276
        if self.mode == 'game':
            
            # increase speed
            if upArrowValue in self._keys.keys():
                
                # accelerate and turn off drag
                if self._keys[upArrowValue] == True:
                    self.increaseSpeed,self.decreaseSpeed = True,False
                    self.drag,self.reverseDrag = False,False
            # brake
            if spaceBar in self._keys.keys():
                if self._keys[spaceBar] == True:self.braking = True
            
            # reverse
            if downArrowValue in self._keys.keys():
                if self._keys[downArrowValue] == True:
                    self.decreaseSpeed,self.increaseSpeed = True,False
                    self.reverseDrag = False
            
            # rotate right
            if rightArrowValue in self._keys.keys():
                if self._keys[rightArrowValue] == True:
                    self.rotateRight = True
                    if self.holdingRightPreviously == False:
                        self.slowTimer,self.indexChanger = 0,1
                        self.holdingRightPreviously = True
            # rotate left
            if leftArrowValue in self._keys.keys():
                if self._keys[leftArrowValue] == True:self.rotateLeft = True  
        
        # control level editor key pressed
        if self.mode == 'LevelEditor':levelEditorKeyPressed(self)

        

    def keyReleased(self, keyCode, modifier):
        upArrowValue,downArrowValue,rightArrowValue,spaceBar = 273,274,275,32
        leftArrowValue = 276
        
        # control game mode key release
        if self.mode == 'game':
           keyReleasedHelper(self) 
           
        # level editor key release
        if self.mode == 'LevelEditor':
            
            # move right
            if rightArrowValue in self._keys.keys():
                if self._keys[rightArrowValue] == False:
                    self.speed = 0
            
            #move left
            if leftArrowValue in self._keys.keys():
                if self._keys[leftArrowValue] == False:
                    self.speed = 0





    def timerFired(self, dt):
        # is called repeadetly controls the game
        if self.mode == 'game':
            if (self.gameOver == False and 
                (self.gameWin == None or self.gameWin == False)):
                for i in range(self.gameSpeed):
                    callHelpers(self) # calls a bunch of helpers
                    controlTimer(self)
                    rotate(self)
       
                # computes vertical speed

                if abs(self.actualFrontHeight - self.actualBackHeight) >= 10:
                    speedMultiplier = 8
                    straightLineDegrees = 180
                    verticalComponent=sin(-1*self.angle*pi/straightLineDegrees)
                    self.verticalSpeed = (verticalComponent*
                        self.speed*speedMultiplier)
                # computes if the player has been holding right for too long
                if self.holdingRightPreviously == True:
                    self.slowTimer += 1
                frontWheely(self)

        # prevents game from rotating left when unecessary
        if self.falling == True and self.rotateRight == True:
            self.rotateLeft = False
        
        if self.mode == 'LevelEditor':
            levelEditorTimerFired(self)

        
    
    def redrawAll(self, screen):
        upArrowValue,downArrowValue,rightArrowValue,spaceBar = 273,274,275,32
        black = (0,0,0)
        yellow = (255,230,7)
        brown = (102,51,0)
        white = (0,0,0)
        red = (229,55,11)
        maxindex = 1000
        lst = self.points[self.index:self.index+maxindex]
        
        # draw home screen
        if self.mode == 'HomeScreen':
            drawHomeScreen(self,screen)
            self.indexChanger = 20
          
        # draw game
        if self.mode == 'game':
            obstacle = lst[self.frontWheelIndex][-1]
            drawClouds(self,screen)
            drawAi(self,screen)
            pygame.draw.polygon(screen,brown,[(0,500),(0,self.height),
                (self.width,self.height),(self.width,500)])
            heightAdjust = 5
            sun_radius = 150
            pygame.draw.circle(screen,yellow,(self.width,0),sun_radius)
            screen.blit(self.DirtBiker,(self.width//4,self.YBikerPostion+2))
            drawBoard(self,screen)
            # drag game over
            if self.gameWin == True:drawEndGame(self,screen)
            if self.gameOver == True:gameLost(self,screen)
            
            # warns player they have been holding right for too long
            if self.drag2 == True:
                myfont = pygame.font.SysFont('timesnewroman',25)
                warning = 'Slowing Down (You are leaning too far right)'
                textSurface = myfont.render(warning,False,red)
                screen.blit(textSurface,(200,250))
            drawFinishLine(self,screen)
            
            # tells player to press space at speed bump obstacle
            if obstacle == 'bump' and self._keys.get(spaceBar,False) == False:
                myfont = pygame.font.SysFont('timesnewroman',40)
                text = myfont.render('PRESS SPACE!',False,red)
                screen.blit(text,(self.width//2-text.get_width()//2,200))

        # draw dialog box
        if self.mode == 'DialogBox':drawDialogBox(self,screen)
        # draw level editor
        if self.mode == 'LevelEditor':drawLevelEditor(self,screen)
        # draw instructions
        if self.mode == 'instructions':drawInstructions(self,screen)
       

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=1000, height=600, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (200, 255, 255)
        
        pygame.init()

# this function was written by lukas peraza
# taken from taken from https://github.com/LBPeraza/Pygame-Asteroids/blob/
#master/pygamegame.py


    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False  

            blue = (138,210,226)
            screen.fill(blue)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()



def callHelpers(self):
    # controls the game and physics of the player
    calculateWheelPositions(self)
    changeSpeed(self)
    controlAi(self)
    changeIndex(self)
    bounce(self)
    gravity(self)
    increaseheight(self)
    angle(self)
    outsideBoard(self)
    playerLose(self)

def controlTimer(self):
    # controls both ai and player timers
    self.timer += 1
    self.aiTimer += 1
    timer_reset = 25
    if self.timer >= timer_reset: self.timer = 0
    if self.aiTimer >= timer_reset: self.aiTimer = 0
    if self.timer == 24 and self.gravity == False:
        self.gravity = True
        self.gravityValue = 0
    if self.aiTimer == 24 and self.aiGravity == False:
        self.aiGravity = True
        self.aiGravityValue = 0

def levelEditorTimerFired(self):
    # cotrols timer fired for the level editor
    space = 5
    self.index += self.indexChanger//space
    self.indexChanger //= 2
    if self.indexChanger == -1: self.indexChanger = 0
    if self.index <= 1: 
        self.index = 1
        self.indexChanger = 10
    self.indexChanger += self.speed*self.maxindex//1000
    margin = 50
    if self.index >= self.maxindex - margin:
        self.speed = -1    



def changeIndex(self):
    # changes the index according to the player's speed
    # player doesn't move but the level moves according to the player's speed
    # this function moves the level
    
    space = 5
    # player is moving forwards
    if self.indexChanger >= 1:
        
        self.index += self.indexChanger//space
        self.finishLine -= self.indexChanger//space *space
        self.indexChanger //= 2
    # player is moving backwards
    if self.indexChanger < 0:
        self.finishLine -= self.indexChanger//2 *space
        self.index += self.indexChanger//2
        self.indexChanger //= 2
        
        # cant go past the beginning of the level
        if self.index <= 1: self.index = 1
        if self.indexChanger == -1: self.indexChanger = 0
    
    self.indexChanger += self.speed




def keyReleasedHelper(self):
    upArrowValue,downArrowValue,rightArrowValue,spaceBar = 273,274,275,32
    leftArrowValue = 276
    
    # stop accelerating
    if upArrowValue in self._keys.keys():
        if self._keys[upArrowValue] == False:
            self.increaseSpeed = False
            self.drag = True
    
    # stop braking
    if spaceBar in self._keys.keys():
        if self._keys[spaceBar]== False:
            self.braking = False
            
    # stop deccelerating
    if downArrowValue in self._keys.keys():
        if self._keys[downArrowValue] == False:
            self.decreaseSpeed = False
            if upArrowValue in self._keys.keys():
                if self._keys[upArrowValue] == False:
                    self.reverseDrag = True
            

    #stop rotating right
    if rightArrowValue in self._keys.keys():
        if self._keys[rightArrowValue] == False:
            self.rotateRight = False
            self.holdingRightPreviously = False
            
    # stop rotating left
    if leftArrowValue in self._keys.keys():
        if self._keys[leftArrowValue] == False:
            self.rotateLeft = False

def levelEditorKeyPressed(self):
    upArrowValue = 273
    downArrowValue = 274
    rigthArrowValue = 275
    leftArrowValue = 276
    spaceBar = 32
    
    # move right
    if rigthArrowValue in self._keys.keys():
        if self._keys[rigthArrowValue] == True:
            self.speed = 10
    # move left
    if leftArrowValue in self._keys.keys():
        if self._keys[leftArrowValue] == True:
            self.speed = -10




def levelEditorMousePressed(self,x,y):
    # controls mouse pressed for level editor
    self.maxindex = 1000
    self.points =  [[506] for i in range(1000)] 
    self.index = 50
    self.speed = 0
    self.indexChanger = 0
    self.mode = 'LevelEditor'



def loadLevelMousePressed(self,x,y):
    loadLevelx1 = 420
    loadLevelx2 = loadLevelx1 + 360
    loadLevely1 = 300
    loadLevely2 = loadLevely1 + 160
    instructs = 'Please enter the name of the file that you would like to load'
    
    if (loadLevelx2 >= x >= loadLevelx1 and 
            loadLevely2 >= y >= loadLevely1 and self.mode == 'DialogBox'):
            # taken from
            #http://stackoverflow.com/questions/899103/writing-a-
            #list-to-a-file-with-python
            try:
                filename = choose(instructs)
                with open (filename, 'rb') as fp:
                    self.points = pickle.load(fp)
                    self.mode = 'game'
                    reset(self)
            except:
                messagebox.showinfo('Error','Incorrect Filename')
                self.mode = 'DialogBox'



def reset(self):
    #resets variables in code when player loses or starts new game
    self.index = 3
    self.gameWidth = self.width * 5
    self._keys[275] = True
    self._keys[275] = False
    # image taken from 
    #http://www.vectorealy.com/wp-content/uploads/hd/hd-dirt-bike-wheelie
    #-drawing-image.jpg
    
    self.DirtBiker = pygame.image.load('dirtBike.png').convert_alpha()
    # image taken from 
    #http://www.vectorealy.com/wp-content/uploads/hd/hd-dirt-bike-wheelie
    #-drawing-image.jpg
    self.Opponent = pygame.image.load('Opponent_finished.png')
    self.DirtBiker = rot_center(self.DirtBiker,-6)
    self.Opponent = rot_center(self.Opponent,-6)
    self.speed = 0
    self.XBikerPosition = 100
    self.YBikerPostion = 420
    self.bikerWidth,self.bikerHeight = self.DirtBiker.get_size()
    # helpers
    resetAi(self)
    resetPhysics(self)
    initClouds(self)
    resetPlayer(self)

    
    
    


def resetPhysics(self):
    # reset physics related variables
    self.increaseSpeed = False
    self.drag = False     
    self.decreaseSpeed = False
    # image taken from 
    #http://www.vectorealy.com/wp-content/uploads/hd/hd-dirt-bike-wheelie
    #-drawing-image.jpg
    self.image = 'dirtBike.png'
    self.indexChanger = 0
    self.backWheelIndex = 50
    self.frontWheelIndex = self.backWheelIndex + self.bikerWidth//5 
    self.reverseDrag = False
    self.wheelHeightDifference = 0
    self.inclineDrag = False
    self.rotateLeft = False
    self.bounce = True
    self.verticalSpeed = 0
    self.angle = 0
    self.actualFrontHeight = self.YBikerPostion + self.bikerHeight 
    self.actualBackHeight = self.actualFrontHeight + self.bikerHeight
    self.falling = False

def resetAi(self):
    # reset variables specefically for ai
    self.aiSpeed = 8
    self.aiAngle = 0
    self.xAiPosition = 100
    self.yAiPostion = 420
    self.aiIncreaseheight = False
    self.aiGravity = True
    self.aiGravityValue = 15
    self.aiBounce = True
    self.aiFalling = False

def resetPlayer(self):
    # reset player specific variables
    self.frontWheelColliding = False
    self.backWheelColliding = False
    self.climbing = False
    self.timer = 0
    self.aiTimer = 0
    self.increaseheight = False
    self.gravity = True
    self.gravityValue = 15
    self.dragValue = 0
    self.gameOver = False
    self.fastRotateLeft = False
    self.slowTimer = 0
    self.holdingRightPreviously = False
    self.fastRotateRight = False
    self.rotateRight = False
    self.drag2 =  False
   
    self.gameWin = None
    self.braking = False
    pointsFromEndOfList = 110
    self.finishLine = (len(self.points)*5-
        pointsFromEndOfList*5-self.frontWheelIndex)
    self.startTime = time.time()


def drawAi(self,screen):
    # draw opponent
    # image taken from 
    #http://www.vectorealy.com/wp-content/uploads/hd/hd-dirt-bike-wheelie
    #-drawing-image.jpg
    image = pygame.image.load('dirtBike.png').convert_alpha()
    screen.blit(self.Opponent,(self.xAiPosition,self.yAiPostion+2))


def controlAi(self):
    # controls the Ai
    self.xAiPosition += self.aiSpeed - self.indexChanger//2
    # when player holds right too long ai will pass the player
    if self.drag2 == True:
        self.aiSpeed = 10
    # player is faster than the ai
    else:
        self.aiSpeed = 8
    # ai position is calculated placed similar to player except
    # speed is contanst and rotates automatically
    self.aiIndex = self.index + self.xAiPosition//5 - self.XBikerPosition
    difference = self.xAiPosition - self.index
    self.aiBackWheelIndex = 50 + self.aiIndex - self.index + 50
    self.aiFrontWheelIndex = self.aiBackWheelIndex + self.bikerWidth//5 
    angleAi(self)
    speedMultiplier = 8
    straightLineDegrees = 180
    verticalComponent = sin(-1*self.aiAngle*pi/straightLineDegrees)
    self.aiVerticalSpeed = verticalComponent*self.aiSpeed*speedMultiplier
    aiIncreaseheight(self)
    aiBounce(self)
    autoRotate(self)

def aiIncreaseheight(self):
    # increases height when reached the end of a ramp
    # uses timer so that height increases naturally
    if self.aiIncreaseheight == True:
        if self.aiTimer <= 20:
            self.yAiPostion += self.aiVerticalSpeed//4
        if self.aiTimer >= 21:
            self.aiIncreaseheight = False

def angleAi(self):
    # computes the angle of ai depending sof location on board
    image = pygame.image.load('Opponent_finished.png').convert_alpha()
    lst = self.points[self.index:self.index+1000]
    actualHeight = self.yAiPostion
    if self.aiFrontWheelIndex < len(lst) and self.aiBackWheelIndex*-1<len(lst):
        frontWheelHeight = lst[self.aiFrontWheelIndex][0]
        obstacle = lst[self.aiFrontWheelIndex][-1]
        backWheelHeight = lst[self.aiBackWheelIndex][0]
        stopObstacle = lst[self.aiBackWheelIndex][-1]

    # helpers the control angle for specific obstacle
        rampAngleAi(self,obstacle,frontWheelHeight,backWheelHeight,image)
        steepRampAngleAi(self,obstacle,frontWheelHeight,backWheelHeight,image)
        speedBumpAngleAi(self,obstacle,image)
        endGameAi(self,stopObstacle)

def speedBumpAngleAi(self,obstacle,image):
    
    if obstacle == 'bump' and self.yAiPostion >= 380:
        self.yAiPostion = 400
        if self.aiSpeed > 8:
            self.aiAngle += randint(-20,20)
        # ai speed lowers slightly on speedbumps however ai is faster on speed
        # bumps than the player
        self.aiSpeed = 6
    # rotate opponent
    self.Opponent = rot_center(image,self.aiAngle)

def endGameAi(self,stopObstacle):
    # controls if ai makes to the end before player
    if (stopObstacle == 'end' and 
        self.gameWin != True and self.aiBackWheelIndex > 0):
        self.gameWin = False
        self.mode = 'DialogBox'



def steepRampAngleAi(self,obstacle,frontWheelHeight,backWheelHeight,image):
    # controls angle for ai
    if obstacle == 'steepRamp1' and self.yAiPostion >= 70:
        self.aiAngle = 50
        steepRampHelper1Ai(self,frontWheelHeight,backWheelHeight,image)
    if obstacle == 'steepRamp2' and self.yAiPostion >= 70:
        self.aiAngle = 60
        steepRampHelper2Ai(self,frontWheelHeight,backWheelHeight,image)
    if obstacle == 'steepRamp3' and self.yAiPostion >= 70:
        self.aiAngle = 70
        steepRampHelper3Ai(self,frontWheelHeight,backWheelHeight,image)
    # allows player ai to jump one they reach the end of the ramp
    if (obstacle == 'steepTip' and 
        self.aiIncreaseheight == False and self.yAiPostion >= 70):
        self.aiIncreaseheight = True
        self.aiTimer = 0
        self.aiGravity = False
        self.Opponent = rot_center(image,self.aiAngle)
    


def rampHelperAi(self,frontWheelHeight,backWheelHeight,image):
    # controls the ai on ramps
    self.Opponent = rot_center(image,self.aiAngle)
    newYBikerPosition=(backWheelHeight + frontWheelHeight)//2-self.bikerHeight
    if self.yAiPostion > newYBikerPosition:
        self.yAiPostion =(backWheelHeight+frontWheelHeight)//2-self.bikerHeight 
        self.Opponent = rot_center(image,self.aiangle)


def steepRampHelper1Ai(self,frontWheelHeight,backWheelHeight,image):
    # first part of the steep rampf for the ai
    self.Opponent = rot_center(image,self.angle)
    newYBikerPosition = ((backWheelHeight + frontWheelHeight)//2 
        - self.bikerHeight - 50)
    if self.yAiPostion > newYBikerPosition:
        self.yAiPostion = ((backWheelHeight + frontWheelHeight)//2 
            - self.bikerHeight -50)
    self.Opponent = rot_center(image,self.aiAngle)


def steepRampHelper2Ai(self,frontWheelHeight,backWheelHeight,image):
    # second part of the steep ramp

    self.Opponent = rot_center(image,self.aiAngle)
    newYBikerPosition = ((backWheelHeight + frontWheelHeight)//2 
        - self.bikerHeight - 80)
    
    self.yAiPostion = ((backWheelHeight + frontWheelHeight)//2 
        - self.bikerHeight - 80)
    self.Opponent = rot_center(image,self.aiAngle)

def steepRampHelper3Ai(self,frontWheelHeight,backWheelHeight,image):
    # last part of the steep ramp
    self.Opponent = rot_center(image,self.aiAngle)
    newYBikerPosition = ((backWheelHeight + 
        frontWheelHeight)//2 - self.bikerHeight - 120)
    if self.yAiPostion > newYBikerPosition:
        self.yAiPostion = ((backWheelHeight + 
            frontWheelHeight)//2 - self.bikerHeight - 120)
    self.Opponent = rot_center(image,self.aiAngle)

def rampAngleAi(self,obstacle,frontWheelHeight,backWheelHeight,image):
    if obstacle == 'ramp' and self.yAiPostion >= 70:
        if self.aiAngle >= 40: 
            self.aiAngle = self.aiAngle
        else:
            self.aiAngle = 40
        self.Opponent = rot_center(image,self.aiAngle)
        newYBikerPosition = ((backWheelHeight+
            frontWheelHeight)/2-self.bikerHeight-60)
        if self.yAiPostion > newYBikerPosition:
            self.yAiPostion= ((backWheelHeight+frontWheelHeight)/2-
                self.bikerHeight-60)
            self.Opponent = rot_center(image,self.aiAngle)
    if (obstacle == 'tip' and self.aiIncreaseheight == False 
        and self.yAiPostion >= 70):
        self.aiIncreaseheight = True
        self.aiTimer = 0
        self.aiBounce = True
        self.aiGravity = False
        self.Opponent = rot_center(image,self.aiAngle)
    # stip for a small ramp
    # this function works for both the large and small ramos
    if (obstacle == 'stip' and self.aiIncreaseheight == False
     and self.yAiPostion >= 150):
        self.aiIncreaseheight = True
        self.aiTimer = 0
        self.aiBounce = True
        self.aiGravity = False
        self.Opponent = rot_center(image,self.aiAngle)


def aiBounce(self):
    # causes the ai to bounce back up when they reach the ground
    # if ai lands with back tire first
    if self.actualAiBackHeight > 500 and self.aiBounce == True:
        self.aiIncreaseheight = True
        self.aiGravity = False
        self.aiBounce = False
    # if ai lands with front tire first
    if self.actualAiFrontHeight > 500 and self.aiBounce == True:
        self.aiIncreaseheight = True
        self.aiGravity = False
        self.aiBounce = False


def autoRotate(self):
    # controls the rotation of the ai
    # when ai is falling rotate so it lands flat
    if self.aiFalling == True:
        if self.aiAngle > 0:
            self.aiAngle -= 1
        if self.aiAngle < 0:
            self.aiAngle += 1
    # incase front tire is under the ground
    if self.actualAiFrontHeight >= 510:
        self.yAiPostion -= self.actualAiFrontHeight - 510
    # incase back tire is undergground
    if self.actualAiBackHeight >= 510:
        self.yAiPostion -= self.actualAiBackHeight - 510



def drawInstructions(self,screen):
    # draws the instruction screen
    darkRed = (96,0,0)
    black = (0,0,0)
    brown = (102,51,0)
    white = (255,255,255)
    drawClouds(self,screen)
    HomeFont = pygame.font.SysFont('timesnewroman',25)
    Home = HomeFont.render('Home',False,black)
    instructions = ('You are the black dirtbiker. ' +
        'The goal of the game is to reach the end of the level '+  
        'faster than the red biker without crashing. ' +
        'Controls: Use the UP and DOWN arrow keys to move ' +
        'forward and backward. Use the LEFT and RIGHT arrow keys to rotate ' + 
        'the biker to left and right respectively, and use the SPACEKEY to ' +
        'brake. Hints: Whenever you go up a ramp the biker will start to lean '+
        'left. If you hit the ground at a bad angle your bike may not be able '+
        'to withstand the fall. If you lean too far right you will start ' +
        'to slow down. You should BRAKE before reaching SPEEDBUMPS.')
    instructionsText = HomeFont.render(instructions,False,black)

    selectionBox = (0,0,100,100)
    selectionBox2 = (10,10,80,80)

   
    HomeFont = pygame.font.SysFont('timesnewroman',25)
    screen.fill(darkRed,selectionBox)
    screen.fill(white,selectionBox2)
    
    Home = HomeFont.render('Home',False,black)
    instructionsLocation = (self.width//2,self.height//2)
    txtLocation = (100//2-Home.get_width()//2,100//2-Home.get_height()//2)

    screen.blit(Home,txtLocation)
    InstructionsRedBox = (200,100,600,320)
    InstructionsWhiteBox = (210,110,580,300)
    textBox = (215,110,575,380)
    screen.fill(darkRed,InstructionsRedBox)
    screen.fill(white,InstructionsWhiteBox)
    drawText(screen,instructions,black,textBox,HomeFont)
    lst = HomeScreenList.startingList[100:]
    pygame.draw.polygon(screen,brown,[(0,600)]+lst+[(1000,600)])



# taken from http://pygame.org/wiki/TextWrap
# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text


def levelEditor(self,x,y):
    x1 = 760
    x2 = 970
    prev_points = self.points
    if x2 >= x >= x1:
        if 165 >= y >= 125:
            prev_max = self.maxindex
            self.maxindex += 1000
            if self.maxindex <= 100000:
                self.points += [[506] for i in range(1000)]
            else:
                self.maxindex = prev_max
        if 210 >= y >= 170:
            prev_max = self.maxindex
            self.maxindex -= 1000
            if self.maxindex >= 1000 and self.index < self.maxindex:
                self.points = self.points[:len(self.points)-1000]
            else:
                self.maxindex = prev_max
        if 255 >= y >= 215:
            lst = ramp(self,506)
            self.points=self.points[:self.index]+lst + self.points[self.index:]
        if 300 >= y >= 260:
            lst = steepRamp(self,506)
            self.points=self.points[:self.index]+lst+self.points[self.index:]
        if 345 >= y >= 305:
            lst = small(self,506)
            self.points=self.points[:self.index]+lst+self.points[self.index:]
        if 390 >= y >= 350:
            lst = jump(self,506)
            self.points=self.points[:self.index]+lst+self.points[self.index:]
        if 435 >= y >= 395:
            lst = speedBumps(self)
            self.points = self.points[:self.index]+lst+self.points[self.index:]
        if 490 >= y >= 440:
            number = randint(1,5)
            if number == 1:
                lst = ramp(self,506)
            if number == 2:
                lst = steepRamp(self,506)
            if number == 3:
                lst = small(self,506)
            if number == 4:
                lst = jump(self,506)
            if number == 5:
                lst = speedBumps(self)
            self.points=self.points[:self.index]+lst+self.points[self.index:]
        if len(self.points)>= self.maxindex:
            self.points = self.points[:self.maxindex]
    
    ending = ([[506] for i in range(200)] + 
    [[506,'end'] for i in range(10)] + [[506] for i in range(100)])
    x1,x2,y1,y2 = 900,1000,0,100
    if x2 >= x >= x1 and y2 >= y >= y1:
        points = self.points
        self.points += ending
        # taken from 
        #http://stackoverflow.com/questions/899103/writing-a-list-to-a-file-
        #with-python
        try:
            filename = choose('Please enter a name for your level')
            with open(filename, 'wb') as fp: pickle.dump(self.points, fp)
        except:
            self.points = points
            messagebox.showinfo('Error','Invalid filename')

    

def drawLevelEditor(self,screen):
    #variables and colors
    darkRed = (96,0,0)
    black = (0,0,0)
    brown = (102,51,0)
    selectionBox = (0,0,100,100)
    selectionBox2 = (10,10,80,80)
    selectionBox3 = (900,0,100,100)
    selectionBox4 = (910,10,80,80)
    white = (255,255,255)
    
    # draw background
    drawBoard(self,screen)
    screen.fill(brown,(0,500,1000,100))
    
    # draw home/save buttons
    HomeFont = pygame.font.SysFont('timesnewroman',25)
    screen.fill(darkRed,selectionBox)
    screen.fill(white,selectionBox2)
    screen.fill(darkRed,selectionBox3)
    screen.fill(white,selectionBox4)
    Save = HomeFont.render('Save',False,black)
    Home = HomeFont.render('Home',False,black)
    
    # draw directions
    dirs1='Use the left and right arrow keys to increase/decrease the index'
    Directions = HomeFont.render(dirs1,False,black)
    dirs2 = 'Use the mouse to select an obstacle to place at the current index'
    Directions2 = HomeFont.render(dirs2,False,black)
    txtLocation = (100//2-Home.get_width()//2,100//2-Home.get_height()//2)
    txt2Location=((900+1000)//2-Save.get_width()//2,100//2-Save.get_height()//2)
    DirectionsLocation = (self.width//2-Directions.get_width()//2,30)
    Directions2Location = (self.width//2-Directions2.get_width()//2,80)
    screen.blit(Directions,DirectionsLocation)
    screen.blit(Directions2,Directions2Location)
    
    # draw home/save button
    screen.blit(Home,txtLocation)
    screen.blit(Save,txt2Location)
    
    # draw index/max index
    index = HomeFont.render('Current Index: '+str(self.index),False,black)
    maxIndex = HomeFont.render('Max Index: ' + str(self.maxindex),False,black)
    indexTxtLocation = (10,300-index.get_height()//2)
    maxIndexLocation = (10,330-index.get_height()//2)
    screen.blit(index,indexTxtLocation)
    screen.blit(maxIndex,maxIndexLocation)
    
    # draw obstacle selection box
    obstacleBox = (750,120,230,365)
    screen.fill(darkRed,obstacleBox)
    y = 125
    lst = ['Increase Indices','Decrease Indices','Ramp',
    'Steep Ramp','Small Ramp','Jump','Speed Bumps','Random']
    for i in range(8):
        screen.fill(white,(760,y,210,40))
        word = HomeFont.render(lst[i],False,black)
        screen.blit(word,((760+760+210)//2-word.get_width()//2,
            (y+y+40)//2-word.get_height()//2))
        y += 45




# adapted from dialogs tkinter example
#https://www.cs.cmu.edu/~112/notes/dialogs-demo1.py
def choose(msg):
    root = Tk()
    root.withdraw()
    response = simpledialog.askstring('',msg)
    return response



def drawFinishLine(self,screen):
    black = (0,0,0)
    width = 50
    y = 500
    height = 100
    screen.fill(black,(self.finishLine,y,width,height))


def drawDialogBox(self,screen):
    # draws menu that pops up after dying and clicking play
    
    # initalize variables
    brown = (102,51,0)
    darkRed = (96,0,0)
    white = (255,255,255)
    drawClouds(self,screen)
    lst = HomeScreenList.startingList[100:]
    pygame.draw.polygon(screen,brown,[(0,600)]+lst+[(1000,600)])
    yellow = (255,239,0)
    sunRadius = 150
    black=(0,0,0)
    myFont = pygame.font.SysFont('timesnewroman',40)
    selectionBox1 = (400,100,400,380)
    selectionBox2 = (420,120,360,160)
    selectionBox3 = (420,300,360,160)
    selectionBox4 = (0,0,100,100)
    selectionBox5 = (10,10,80,80)
    selectionBox6 = (120,100,200,380)
    
    # draw selectionboxes/sun
    pygame.draw.circle(screen,yellow,(self.width,0),sunRadius)
    screen.fill(darkRed,selectionBox1)
    screen.fill(white,selectionBox2)
    screen.fill(white,selectionBox3)
    screen.fill(darkRed,selectionBox6)
    
    # draw new/load level box and home button
    newLevel = myFont.render('New Level',False,black)
    txt1Location = ((420+780)//2-newLevel.get_width()//2,
        (120+280)//2-newLevel.get_height()//2)
    screen.blit(newLevel,txt1Location)
    oldLevel = myFont.render('Load level',False,black)
    txt2Location = ((420+780)//2-oldLevel.get_width()//2,
        (300+460)//2-oldLevel.get_height()//2)
    screen.blit(oldLevel,txt2Location)
    HomeFont = pygame.font.SysFont('timesnewroman',25)
    screen.fill(darkRed,selectionBox4)
    screen.fill(white,selectionBox5)
    Home = HomeFont.render('Home',False,black)
    txt3Location = (100//2-Home.get_width()//2,100//2-Home.get_height()//2)
    screen.blit(Home,txt3Location)
    
    # draw win/loss
    winFont = pygame.font.SysFont('Castellar',50)
    Win = winFont.render('You Won!',False,darkRed)
    Lose = winFont.render('You Lost!',False,darkRed)
    WinLossLocation = (self.width//2-Lose.get_width()//2,20)
    if self.gameWin == True:
        screen.blit(Win,WinLossLocation)
    if self.gameWin == False:
        screen.blit(Lose,WinLossLocation)
    
    # draw speed selection box
    drawSpeed(self,screen)

def speedSelector(self,x,y):
    # allows player to choose the speed that they want
    veryFastBox = (130,389,310,472)
    normalBox = (130,203,310,286)
    fastBox = (130,296,310,379)

    if normalBox[2] >= x >= normalBox[0] and normalBox[3] >= y >= normalBox[1]:
        self.gameSpeed = 1
        print(1)
    if fastBox[2] >= x >= fastBox[0] and fastBox[3] >= y >= fastBox[1]:
        self.gameSpeed = 2
        print(2)
    if (veryFastBox[2] >= x >= veryFastBox[0] and 
        veryFastBox[3] >= y >= veryFastBox[1]):
        self.gameSpeed = 3



def drawSpeed(self,screen):
    # draws the speed selection boxes
    
    # variables
    black = (0,0,0)
    white = (255,255,255)
    y = 110
    speedBox = [130,y,180,83]
    gray = (181,181,181)
    font = pygame.font.SysFont('timesnewroman',30)
    selectSpeed = font.render('Select Speed',False,black)
    normal = font.render('Normal',False,black)
    fast = font.render('Fast',False,black)
    veryFast = font.render('Very Fast',False,black) 
    font_list = [selectSpeed,normal,fast,veryFast]   
    
    # draw boxes
    color = white
    for i in range(len(font_list)):
        if self.gameSpeed == i: color = gray #box that is selected will be gray
        else: color = white
        screen.fill(color,tuple(speedBox))
        txt_x = 130 + 180//2 - font_list[i].get_width()//2
        txt_y = speedBox[1] + 83//2 - font_list[i].get_height()//2
        location = (txt_x,txt_y)
        screen.blit(font_list[i],location)
        speedBox[1] += 93
        

    

def drawHomeScreen(self,screen):
    
    # draw sun background
    brown,darkRed,white,yellow = (102,51,0),(96,0,0),(255,255,255),(255,239,0)
    drawClouds(self,screen)
    lst = HomeScreenList.startingList[100:]
    pygame.draw.polygon(screen,brown,[(0,600)]+lst+[(1000,600)])
    sunRadius = 150
    pygame.draw.circle(screen,yellow,(self.width,0),sunRadius)
    black=(0,0,0)
   
   
    drawBoxes(self,screen)
    drawTextTwo(self,screen)
    

def drawBoxes(self,screen):
    # draw home screen selection boxes
    darkRed = (96,0,0)
    selectionBox1 = (50,350,220,100)
    selectionBox2 = (320,350,220,100)
    selectionBox3 = (590,350,220,100) 
    screen.fill(darkRed,selectionBox1)
    screen.fill(darkRed,selectionBox2)
    screen.fill(darkRed,selectionBox3)

def drawTextTwo(self,screen):
    # draws text for selection buttons on home screen
    # initialize variables
    brown,darkRed,white,yellow = (102,51,0),(96,0,0),(255,255,255),(255,239,0)
    myFont = pygame.font.SysFont('Castellar',50)
    textSurface = myFont.render('Dirt Bike Racer',False,darkRed)
    txtFont = pygame.font.SysFont('timesnewroman',40)
    screen.blit(textSurface,(self.width//2-textSurface.get_width()//2,100))
    PlayText = txtFont.render('Play',False,white)
    InstructionText = txtFont.render('Instructions',False,white)
    LevelEditorText = txtFont.render('Level Editor',False,white)
    
    # right edge is equal to width plus left edge
    # divide by two to get center
    centerX = ((320) + (320+220))//2
    centerY = ((350) + (350+100))//2
    location = (centerX-PlayText.get_width()//2,
        centerY-PlayText.get_height()//2)
    spacing,width,adjust = 50,220,270
    txtLocationOne = (centerX-adjust- InstructionText.get_width()//2,
        centerY- InstructionText.get_height()//2)
    txtLocationTwo = (centerX+adjust- LevelEditorText.get_width()//2,
        centerY- LevelEditorText.get_height()//2)
    
    # draw boxes
    screen.blit(PlayText,location)
    screen.blit(InstructionText,txtLocationOne)
    screen.blit(LevelEditorText,txtLocationTwo)

def endGame(self,stopObstacle):
    # controls if it is the endgame
    if stopObstacle == 'end':
        self.gameWin = True
        self.mode = 'DialogBox'

def initClouds(self):
    # initializes the starting location of clouds and is called in reset
    cloud1 = [100,100]
    cloud7 = [200,50]
    cloud8 = [900,100]
    cloud9 = [1000,100]
    cloud2 = [400,100]
    cloud3 = [700,100]
    cloud4 = [250,50]
    cloud5 = [550,50]
    cloud6 = [0,50]
    self.cloudlst = [cloud1,cloud2,cloud3,cloud4,cloud4,cloud6]

def angle(self):
    # computes angle for player
    rigthArrowValue = 275
    leftArrowValue = 276
    # image taken from 
    #http://www.vectorealy.com/wp-content/uploads/hd/hd-dirt-bike-wheelie
    #-drawing-image.jpg
    image = pygame.image.load('dirtBike.png').convert_alpha()
    lst = self.points[self.index:self.index+1000]
    
    actualHeight = self.YBikerPostion 
    frontWheelHeight = lst[self.frontWheelIndex][0]
    obstacle = lst[self.frontWheelIndex][-1]
    backWheelHeight = lst[self.backWheelIndex][0]
    stopObstacle = lst[self.backWheelIndex][-1]
    
    # prevents player from going too far back
    if stopObstacle == 'stop' and self.YBikerPostion >= 400:
        self.index += 3
        self.decreaseSpeed = 0
    
    # calls helpers that change angle depending on obstacle
    rampAngle(self,obstacle,frontWheelHeight,backWheelHeight,image)
    steepRampAngle(self,obstacle,frontWheelHeight,backWheelHeight,image)
    speedBumpAngle(self,obstacle,image)
    endGame(self,stopObstacle)

def speedBumpAngle(self,obstacle,image):
    # changes angle if player is on speedbumps
    if obstacle == 'bump' and self.YBikerPostion >= 380:
        # the faster the player is going the worse thae angle changes will be
        self.YBikerPostion = 400
        if self.speed <= 5:
            self.angle += randint(-2,2)
        if self.speed > 5 and self.speed <= 8:
            self.angle += randint(-8,8)
        if self.speed > 8:
            self.angle += randint(-20,20)
    self.DirtBiker = rot_center(image,self.angle)



    


def steepRampAngle(self,obstacle,frontWheelHeight,backWheelHeight,image):
    # controls angle and speed when player is on a steep ramps
    # steep ramp is divided up into three sections each changes player's speed
    # and angle differently.

    if obstacle == 'steepRamp1' and self.YBikerPostion >= 70:
        if self.angle >= 50:
            self.angle = self.angle
        else:
            self.angle = 50
            steepRampHelper1(self,frontWheelHeight,backWheelHeight,image)
    
    if obstacle == 'steepRamp2' and self.YBikerPostion >= 70:
        if self.angle >= 60: 
            self.angle = self.angle
        else:
            self.angle = 60
            steepRampHelper2(self,frontWheelHeight,backWheelHeight,image)
    
    if obstacle == 'steepRamp3' and self.YBikerPostion >= 70:
        if self.angle >= 70:
            self.angle = self.angle
        else:
            self.angle = 70
            steepRampHelper3(self,frontWheelHeight,backWheelHeight,image)
    
    if (obstacle == 'steepTip' 
        and self.increaseheight == False and self.YBikerPostion >= 70):
        self.increaseheight = True
        self.timer = 0
        self.bounce = True
        self.gravity = False
        self.DirtBiker = rot_center(image,self.angle)
    


def rampHelper(self,frontWheelHeight,backWheelHeight,image):
    # computes speed for biker on a normal ramp
    self.DirtBiker = rot_center(image,self.angle)
    newYBikerPosition = (backWheelHeight + frontWheelHeight)//2-self.bikerHeight
    if self.YBikerPostion > newYBikerPosition:
        self.YBikerPostion=((backWheelHeight+frontWheelHeight)//2-
            self.bikerHeight) 
        if self.speed >= 6 and self.rotateRight == False:self.rotateLeft = True
        else: self.rotateLeft = False
        self.DirtBiker = rot_center(image,self.angle)


def steepRampHelper1(self,frontWheelHeight,backWheelHeight,image):
    # computes speed and other locations on a first part of a ramp
    self.DirtBiker = rot_center(image,self.angle)
    newYBikerPosition=(backWheelHeight+frontWheelHeight)//2-self.bikerHeight-50
    if self.YBikerPostion > newYBikerPosition:
        self.YBikerPostion=((backWheelHeight+frontWheelHeight)//2-
            self.bikerHeight-50)
        if self.rotateRight == False:self.rotateLeft = True
        else:self.rotateLeft = False
        self.DirtBiker = rot_center(image,self.angle)


def steepRampHelper2(self,frontWheelHeight,backWheelHeight,image):
    # computes speed and other biker variables on second part of the ramp
    self.DirtBiker = rot_center(image,self.angle)
    newYBikerPosition = ((backWheelHeight + frontWheelHeight)//2 
        - self.bikerHeight - 80)
    if self.YBikerPostion > newYBikerPosition:
        self.YBikerPostion = ((backWheelHeight + frontWheelHeight)//2 - 
            self.bikerHeight - 80)
        if self.rotateRight == False and self.speed <= 2:
            self.fastRotateLeft = True
        else:
            self.fastrotateLeft = False
        self.DirtBiker = rot_center(image,self.angle)

def steepRampHelper3(self,frontWheelHeight,backWheelHeight,image):
    # computes speed and other biker variables on the third part of the ramp
    self.DirtBiker = rot_center(image,self.angle)
    newYBikerPosition = ((backWheelHeight + 
        frontWheelHeight)//2 - self.bikerHeight - 120)
    if self.YBikerPostion > newYBikerPosition:
        self.YBikerPostion = ((backWheelHeight +
            frontWheelHeight)//2 - self.bikerHeight - 120)
        if self.speed <= 4 and self.rotateRight == False:
            self.fastRotateLeft = True
        else:
            self.fastrotateLeft = False
        self.DirtBiker = rot_center(image,self.angle)


def rampAngle(self,obstacle,frontWheelHeight,backWheelHeight,image):
    # computes the angle for the biker when on a ramp
    if obstacle == 'ramp' and self.YBikerPostion >= 70:
        if self.angle >= 40: 
            self.angle = self.angle
        else:
            self.angle = 40
        self.DirtBiker = rot_center(image,self.angle)
        newYBikerPosition = ((backWheelHeight + frontWheelHeight)/2
         - self.bikerHeight - 60)
        if self.YBikerPostion > newYBikerPosition:
            self.YBikerPostion = ((backWheelHeight + frontWheelHeight)/2
             - self.bikerHeight - 60)
            if self.speed >= 6 and self.rotateRight == False:
                self.rotateLeft = True
            else:
                self.rotateLeft = False
            self.DirtBiker = rot_center(image,self.angle)
    
    # if biker is on a normal ramp
    if (obstacle == 'tip' and 
        self.increaseheight == False and self.YBikerPostion >= 70):
        self.increaseheight = True
        self.timer = 0
        self.bounce = True
        self.gravity = False
        self.DirtBiker = rot_center(image,self.angle)
    
    # if biker is on a small ramp
    if (obstacle == 'stip' and self.increaseheight == False 
        and self.YBikerPostion >= 150):
        self.increaseheight = True
        self.timer = 0
        self.bounce = True
        self.gravity = False
        self.DirtBiker = rot_center(image,self.angle)
    

def increaseheight(self):
    # increased the height of the player when jumping off of a ramp
    if self.increaseheight == True:
        if self.timer <= 20:
            self.YBikerPostion += self.verticalSpeed//4
        if self.timer >= 21:
            self.increaseheight = False
    
def outsideBoard(self):
    upArrowValue = 273
    downArrowValue = 274
    rightArrowValue = 275
    leftArrowValue = 276
    # image taken from 
    #http://www.vectorealy.com/wp-content/uploads/hd/hd-dirt-bike-wheelie
    #-drawing-image.jpg
    image = pygame.image.load('dirtBike.png').convert_alpha()
    # computes if the player is outside of the board
    # if the player is it makes corrections by moving the biker's y positions
    # or rotating the player
    if self.actualFrontHeight >= 490:
        self.rotateLeft = True
    elif leftArrowValue in self._keys.keys():
        if self._keys[leftArrowValue] == False:
            self.rotateLeft = False
    if self.actualBackHeight >= 510:
        self.rotateRight = True
    elif rightArrowValue in self._keys.keys():
        if self._keys[rightArrowValue] == False:
            self.rotateRight = False
    if self.YBikerPostion >= 420:
        self.YBikerPostion = 420
        self.angle = 0
    if self.actualBackHeight >= 510:
        value = self.actualBackHeight - 510
        self.actualBackHeight = self.actualBackHeight + value

    

            

def calculateWheelPositions(self):
    # calculate the wheel positions by using the angle of rotation
    # and the position of the biker
    # case on whether the angle is greater than 0 or less than 0
    
    if self.angle <= 0:
        self.actualFrontHeight = (self.YBikerPostion+
            self.bikerHeight-(self.angle/90)*self.bikerWidth//2)
        self.actualBackHeight = (self.YBikerPostion+
            self.bikerHeight + (self.angle/90)*self.bikerWidth//2)
    
    if self.angle > 0:
        self.actualFrontHeight = (self.YBikerPostion + self.bikerHeight - 
            (sin(radians(self.angle)))*self.bikerWidth//2)
        self.actualBackHeight = (self.YBikerPostion +self.bikerHeight + 
            (sin(radians(self.angle)))*self.bikerWidth//2)
    aiWheelPositions(self)
   

def aiWheelPositions(self):
    # computes wheel positions for the ai
    if self.aiAngle <= 0:
        self.actualAiFrontHeight = (self.yAiPostion + 
            self.bikerHeight - (self.aiAngle/90)*self.bikerWidth//2)
        self.actualAiBackHeight = (self.yAiPostion+self.bikerHeight+ 
            (self.aiAngle/90)*self.bikerWidth//2)
    
    if self.aiAngle > 0:
        self.actualAiFrontHeight = (self.yAiPostion + 
            self.bikerHeight - sin(radians(self.aiAngle/90))*self.bikerWidth//2)
        self.actualAiBackHeight = (self.yAiPostion + self.bikerHeight + 
            sin(radians(self.aiAngle/90))*self.bikerWidth//2)




def rotate(self):
    # image taken from 
    #http://www.vectorealy.com/wp-content/uploads/hd/hd-dirt-bike-wheelie
    #-drawing-image.jpg
    image = pygame.image.load('dirtBike.png').convert_alpha()
    lst = self.points[self.index:self.index+1000]
    frontWheelHeight = lst[self.frontWheelIndex][0]
    backWheelHeight = lst[self.backWheelIndex][0]
    
    # when player is holding right rotates right
    if self.rotateRight == True:
        self.angle -= 1;self.DirtBiker = rot_center(image,self.angle)
        
        if self.actualFrontHeight > frontWheelHeight:
            self.angle += 1;self.DirtBiker = rot_center(image,self.angle)
    
    # rotate left if player is pressing left or on a ramp
    if self.rotateLeft == True:
        self.angle += 1;self.DirtBiker = rot_center(image,self.angle)
        
        if self.actualBackHeight > backWheelHeight:
            self.angle -= 1;self.DirtBiker = rot_center(image,self.angle)
    
    # triggered on top of a steep ramp
    if self.fastRotateLeft == True:
        self.angle += 2;self.DirtBiker = rot_center(image,self.angle)
    

# taken from https://www.pygame.org/wiki/RotateCenter
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image,angle)
    rot_rect = orig_rect.copy()
   
    return rot_image





def bounce(self):
    # image taken from 
    #http://www.vectorealy.com/wp-content/uploads/hd/hd-dirt-bike-wheelie
    #-drawing-image.jpg
    image = pygame.image.load('dirtBike.png').convert_alpha()
    # bounces up when player hits the ground at a high speed
    
    # if player is leaning backward or left
    if self.actualBackHeight> 500 and self.bounce == True:
        self.increaseheight = True
        self.gravity = False
        self.bounce = False
        self.angle += -1*self.verticalSpeed//2
        self.DirtBiker = rot_center(image,self.angle)
    
    # if player is leanign forward
    if self.actualFrontHeight > 500 and self.bounce == True:
        self.increaseheight = True
        self.gravity = False
        self.bounce = False
        self.angle += self.verticalSpeed//2
        self.DirtBiker = rot_center(image,self.angle)
    


def frontWheely(self):
    # slows down the player if they have been holding right for too long
    if self.holdingRightPreviously == True and self.slowTimer >= 50:
        self.WheelyTimer = 0
        self.drag2 = True
    else:
        self.drag2 = False




def gravity(self):
    lst = self.points[self.index:self.index+1000]
    frontWheelHeight = lst[self.frontWheelIndex][0]
    backWheelHeight = lst[self.backWheelIndex][0]
    
    # figures out if the player is falling
    if (self.actualBackHeight <= backWheelHeight and 
        self.actualFrontHeight <= frontWheelHeight):
        self.falling = True
    else: 
        self.falling = False
    
    # if the player is falling lowers the y positons till they are not
    #falling anymore
    if self.falling == True and self.gravity == True:
        self.YBikerPostion += self.gravityValue
        if self.gravityValue <= 2: self.gravityValue += .2
        if  2 < self.gravityValue <= 5: self.gravityValue += 1
        if 5 < self.gravityValue < 15: self.gravityValue += 1.5
        if self.gravityValue >= 15: self.gravityValue = 15
    
    inclineDragHelper(self,lst)
    aiGravity(self,lst)
    



def aiGravity(self,lst):    
    # gravity for the opponent
    if self.aiFrontWheelIndex < len(lst) and self.aiBackWheelIndex*-1<len(lst):
        aiBackWheelHeight = lst[self.aiBackWheelIndex][0]
        aiFrontWheelHeight = lst[self.aiFrontWheelIndex][0]
        
    # figures out if ai is falling
        if (self.actualAiBackHeight <= aiBackWheelHeight 
                and self.actualAiFrontHeight <= aiFrontWheelHeight):
            self.aiFalling = True
        else:
            self.aiFalling = False

    # if ai is falling lowers Y position till they are no longer falling
    if self.aiFrontWheelIndex < len(lst) and self.aiBackWheelIndex*-1<len(lst):
        
        if self.aiGravity == True and self.aiFalling == True:
            self.yAiPostion += self.aiGravityValue
            if self.aiGravityValue <= 2: self.aiGravityValue += .2
            if 2 < self.aiGravityValue <= 5: self.aiGravityValue += 1
            if 5 < self.aiGravityValue < 15: self.aiGravityValue += 1.5
            if self.aiGravityValue >= 15: self.aiGravityValue = 15

   


def inclineDragHelper(self,lst):
    # if a player is on a ramp they should go backwards
    if (lst[self.backWheelIndex][-1] == 'ramp' or 
        lst[self.backWheelIndex][-1]=='steepRamp1' or
         lst[self.backWheelIndex]=='steepRamp2' or
        lst[self.backWheelIndex][-1] == 'steepRamp3' or 
        lst[self.backWheelIndex][-1] == 'steepTip' or 
        lst[self.backWheelIndex][-1] == 'tip'):
       # slow down on ramps
        self.inclineDrag = True
    else: self.inclineDrag = False


def randomLine(self):
    # creates a list of random points as terrain
    lst = [[506] for i in range(0,400,5)]
    x,y,i = 0,500,400
    # generates a random list when player clicks new level
    rampNumber,steepRampNumber,smallNumber = [1,2],[3,4],[5,6]
    jumpNumber,speedBumpNumber = [7,8],9
    while i <= self.gameWidth:
        randNumber = randint(1,1000)
        # adds obstacle to list and increases index by length of len of obstacle
        if randNumber in rampNumber:lst += ramp(self,y); i += 69
        if randNumber in steepRampNumber:lst += steepRamp(self,y); i += 46
        if randNumber in smallNumber:lst += small(self,y); i += 49
        if randNumber in jumpNumber:lst += jump(self,y); i += 129
        if randNumber == speedBumpNumber:lst += speedBumps(self);i += 200
        else:lst += [[y]];i += 1
    ending = ([[506] for i in range(200)] + [[506,'end'] for i in range(10)] 
    + [[506] for i in range(100)])
    return lst + ending


def gameLost(self,screen):
    # changes mode if game is lost because player dies or is beaten to end
    self.gameWin = False
    self.mode = 'DialogBox'



def ramp(self,y):
    # ramp 
    upSlope = [[y-i,'ramp'] for i in range(0,100,5)]
    upSlope1 = [[y-i,'ramp'] for i in range(100,300,5)]
    
    tip = [[y-300,'tip'] for j in range(0,40,5)]
    # equalizing the length of each obstacle
    stop = [[y-300,'stop']*5]
    ramp = upSlope+ upSlope1 + tip + stop 
    
    return ramp

def steepRamp(self,y):
    # creates steep Ramp list
    upSlope1 = [[y-i,'steepRamp1'] for i in range(0,100,5)]
    upslope2 = [[y-i,'steepRamp2'] for i in range(100,200,10)]
    upslope3 = [[y-i,'steepRamp3'] for i in range(200,300,15)]
    tip = [[y-300,'steepTip'] for i in range(0,40,5)]
    stop = [[y-300,'stop']*5]
    steepRamp = upSlope1 + upslope2 + upslope3 + tip + stop 
    
    return steepRamp


def small(self,y):
    # creates a small ramp list
    upSlope = [[y-i,'ramp'] for i in range(0,100,5)]
    upSlope1 = [[y-i,'ramp'] for i in range(100,200,5)]
    tip = [[y-200,'stip'] for j in range(0,40,5)]
    stop = [[y-200,'stop']*5]
    small = upSlope + upSlope1 + tip + stop
    return small

def jump(self,y):
    
    #creates a jump
    
    # uses small ramp
    smallLst = small(self,y)
    # pointy part of the jump

    flat = [[y,'point'] for i in range(0,200,5)]
    pointy = [[y-100,'point'] for i in range(0,200,5)]
    pointyList = interleaveLists(flat,pointy)
    jump = smallLst + pointyList
    
    return jump

def speedBumps(self):
    # creates speed bumps
    up = [[500-2*i,'bump'] for i in range(5)]
    down = [[490+2*i,'bump'] for i in range(5)]
    speedBumps = []
    for i in range(20):
        speedBumps += up + down
    
    return speedBumps


def interleaveLists(lst1,lst2):
    # interleaves lists used for the jump obstacle
    new_lst = []
    for i in range(len(lst1)):
        new_lst += [lst1[i]] + [lst2[i]]
    return new_lst



def testInterleaveLists():
    lst1 = [[1],[3],[5],[7]]
    lst2 = [[2],[4],[6],[8]]
    assert(interleaveLists(lst1,lst2) == [[1],[2],[3],[4],[5],[6],[7],[8]])




def playerLose(self):
    lst = self.points[self.index:self.index+1000]
    index = (self.frontWheelIndex + self.backWheelIndex)//2
    obstacle = lst[self.frontWheelIndex:][0][-1]
    
    # if the player over rotates
    if (-30 >= self.angle  or self.angle >= 90) and self.falling == False:
        self.gameWin = False
        self.gameOver = True
        self.YBikerPostion = 420
    # player lands on pointy part of a jump obstacle
    if obstacle == 'point':
        if self.actualBackHeight >= 400 or self.actualFrontHeight >= 400:
            self.gameOver = True
    # if opponent gets too far in front of the player game ends
    if self.aiFrontWheelIndex > len(lst) and self.aiFrontWheelIndex >0:
        self.gameOver = True
        self.gameWin = False
        self.YBikerPostion = 420




def drawBoard(self,screen):
    # uses xbiker position to draw course
    #colors
    black,yellow,brown,green = (0,0,0),(255,239,0),(102,51,0),(64,84,1)
    brown,darkRed,white = (102,51,0),(96,0,0),(255,255,255)
    
    maxPossibleIndicesOnScreen = 1000
    endIndex = self.index + maxPossibleIndicesOnScreen
    self.endIndex = endIndex
    points = self.points[self.index:self.index+1000]
    new_lst,x = [],0
    
    # changes list from just y values to x and y values so that
    # pygame can draw polygon of it
    for point in points:
        y = point[0]
        new_lst += [tuple([x,y])]
        x += 5
    # draws board
    pygame.draw.polygon(screen,brown,[(0,506)]+new_lst+
        [(1000,506),(1000,506),(1000,506)])
    selectionBox,selectionBox2 = (0,0,100,100),(10,10,80,80)
    
    HomeFont = pygame.font.SysFont('timesnewroman',25)
    screen.fill(darkRed,selectionBox)
    screen.fill(white,selectionBox2)
    
    Home = HomeFont.render('Home',False,black)
    instructionsLocation = (self.width//2,self.height//2)
    txtLocation = (100//2-Home.get_width()//2,100//2-Home.get_height()//2)
    screen.blit(Home,txtLocation)

    
def drawClouds(self,screen):
    # draw clouds
    #https://en.wikipedia.org/wiki/File:Cartoon_cloud.svg
    cloudImage = pygame.image.load('cloud.png').convert_alpha()
    space = 5
    margin = 200
    # clouds initialize in initclouds
    for cloud in self.cloudlst:
        cloud[0] = cloud[0] - self.indexChanger//space
        if cloud[0] <= margin *-1:
            cloud[0] += self.width+margin
    
        screen.blit(cloudImage,cloud)


   

   

def changeSpeed(self):
    # changes the speed of the player according to the keys being  presses
    # increase speed
    if self.increaseSpeed == True:
        self.speed += 2
        if self.speed >= 10: self.speed = 10
    # slow the player down when up key is released
    if self.drag == True:
        self.dragValue -= .2
        if self.dragValue <= -1:
            self.dragValue = 0
            self.speed -= 1
        if self.speed <= 0:
            self.speed = 0
    # decrease speed this occurs if player is pressing down or on a ramp
    if self.decreaseSpeed == True:
        self.speed -= 2
        if self.speed <= -4: self.speed = 4
    changeSpeedTwo(self)
    

def changeSpeedTwo(self):
    # prevents player from going too fast backwards
    if self.reverseDrag == True:
        self.speed += 1
        if self.speed >= 0: self.speed = 0
    
    # slows player down on ramps
    if self.inclineDrag == True:
        self.speed -= 1
        if self.speed <= -2: self.speed = -2
    
    #if player has been pressing right for too long
    print(self.gravityValue)
    if self.drag2 == True and self.speed >0:
        self.speed -= 2
        if self.speed <= 6:
            self.speed = 6
    # braking
    if self.braking == True:
        self.speed -= 5
        if self.increaseSpeed == True:
            if self.speed <= 5:self.speed = 5
        if self.increaseSpeed == False:
            if self.speed <= 0:self.speed = 0
       

def main():
    game = PygameGame()
    game.run()


main()
