import pygame, simpleGE, random, json

class Rubble(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("debris1.png")
        self.position = (320, 400)
        self.setSize(55,55)
        self.minSpeed = 3
        self.maxSpeed = 8
        self.reset()
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
            
class Rubble2(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("debris2.png")
        self.position = (320, 400)
        self.setSize(50,110)
        self.minSpeed = 3
        self.maxSpeed = 8
        self.reset()
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
            
class Arrow(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("arrow.png")
        self.position = (320, 400)
        self.setSize(75,20)
        self.minSpeed = 3
        self.maxSpeed = 8
        self.reset()
        
    def reset(self):
        self.y = random.randint(230, self.screenHeight)
        self.x = 0
        self.dx = random.randint(self.minSpeed, self.maxSpeed)
        
    def checkBounds(self):
        if self.right > self.screenWidth:
            self.reset()


class Gold(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("gold.png")
        self.position = (200, 300)
        self.center = (0, 0)
        self.setSize(35,35)
        self.reset()
        
    def reset(self):
        self.y = random.randint(220, self.screenHeight)
        self.x = random.randint(240, self.screenWidth)

class Potion(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("potion.png")
        self.position = (200, 300)
        self.setSize(50,50)
        self.reset()
        
    def reset(self):
        self.y = random.randint(220, self.screenHeight-10)
        self.x = random.randint(10, self.screenWidth-10)

class Knight(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.walkAnim = simpleGE.SpriteSheet("playerwalk.png", (64, 64), 4, 9, .1)
        
        self.walkAnim.startCol = 1
        self.animRow = 2
        self.moveSpeed = 8
        self.x = 210
        self.y = 400
        self.boundAction = self.STOP
        
        self.hitboxOffsetX = 0
        self.hitboxOffsetY = 0
        self.hitboxWidth = 64
        self.hitboxHeight = 100
        
        self.updateHitbox()
        self.checkBounds()
        
    def process(self):
        self.dx = 0
        self.dy = 0
        walking = False
        self.setSize = (100, 100)
        
        if self.isKeyPressed(pygame.K_UP):
            self.animRow = 0
            self.dy = -self.moveSpeed
            walking = True
        if self.isKeyPressed(pygame.K_LEFT):
            self.animRow = 1
            self.dx = -self.moveSpeed
            walking = True
        if self.isKeyPressed(pygame.K_DOWN):
            self.animRow = 2
            self.dy = self.moveSpeed
            walking = True
        if self.isKeyPressed(pygame.K_RIGHT):
            self.animRow = 3
            self.dx = self.moveSpeed
            walking = True
        
        if walking:
            self.copyImage(self.walkAnim.getNext(self.animRow))
        else:
            self.copyImage(self.walkAnim.getCellImage(0, self.animRow))
    
    def checkBounds(self):
        if self.visible:
            scrWidth = self.screen.get_width()
            scrHeight = self.screen.get_height()
            
            offRight = offLeft = offTop = offBottom = offScreen = False
            
            if self.x > scrWidth-10:
                offRight = True
            if self.x < 10:
                offLeft = True
            if self.y > scrHeight-10:
                offBottom = True
            if self.y < 225:
                offTop = True
                
            if offRight or offLeft or offTop or offBottom:
                offScreen = True
            
            if self.boundAction == self.STOP:
                if offLeft:
                    self.x = 10
                if offRight:
                    self.x = scrWidth-10
                if offTop:
                    self.y = 225
                if offBottom:
                    self.y = scrHeight-10

    def updateHitbox(self):
        self.rect = pygame.Rect(
            self.x + self.hitboxOffsetX,
            self.y + self.hitboxOffsetY,
            self.hitboxWidth,
            self.hitboxHeight
        )

class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "High Score: "
        self.center = (320, 50)
        self.size = (200, 75)
        
class LblHiScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "High Score: 0"
        self.center = (320, 50)
        self.size = (200, 75)

class LblHealth(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Health: 3"
        self.center = (320, 70)

class Game(simpleGE.Scene):    
    def __init__(self, hiScore):
        super().__init__()
        self.setImage("background1.png")
        
        self.sndHurt = simpleGE.Sound("Hurt.wav")
        self.sndGold = simpleGE.Sound("Gold.wav")
        self.sndBGM = simpleGE.Sound("8bit.mp3")
        
        self.sndBGM.play()
        
        self.numRubbles = 4
        self.numRubble2s = 3
        self.numArrows = 2
        self.numGolds = 1
        
        self.health = 3
        self.score = 0
        self.hiScore = hiScore
        
        self.lblScore = LblScore()
        self.lblHiScore = LblHiScore()
        self.lblHiScore.text = f"High Score: {self.hiScore:.1f}"
        
        self.timer = simpleGE.Timer()
        self.start
        
        self.lblHealth = LblHealth()
        
        self.knight = Knight(self)
        
        self.rubbles = []
        for i in range(self.numRubbles):
            self.rubbles.append(Rubble(self))
        
        self.rubble2s = []
        for i in range(self.numRubble2s):
            self.rubble2s.append(Rubble2(self))
            
        self.arrows = []
        for i in range(self.numArrows):
            self.arrows.append(Arrow(self))
            
        self.golds = []
        for i in range(self.numGolds):
            self.golds.append(Gold(self))
        
        self.sprites = [self.knight,
                        self.rubbles,
                        self.rubble2s,
                        self.golds,
                        self.lblScore,
                        self.lblHealth,
                        self.arrows]
        
    def process(self):
        timedScore = self.timer.getElapsedTime()
        
        for rubble in self.rubbles:
            if rubble.collidesWith(self.knight):
                rubble.reset()
                self.sndHurt.play()
                self.health -= 1
                self.lblHealth.text = f"Health: {self.health}"
        
        for rubble2 in self.rubble2s:
            if rubble2.collidesWith(self.knight):
                rubble2.reset()
                self.sndHurt.play()
                self.health -= 1
                self.lblHealth.text = f"Health: {self.health}"
                
        for arrow in self.arrows:
            if arrow.collidesWith(self.knight):
                arrow.reset()
                self.sndHurt.play()
                self.health -= 1
                self.lblHealth.text = f"Health: {self.health}"
                
        for gold in self.golds:
            if gold.collidesWith(self.knight):
                gold.reset()
                self.sndGold.play()
                self.score += 2
                self.lblScore.text = f"High Score: {self.score}"
                
        combinedScore = self.score + timedScore
        self.lblScore.text = f"High Score: {combinedScore:.1f}"      
        
        if combinedScore > self.hiScore:
            self.hiScore = combinedScore
            self.lblHiScore.text = f"High Score: {self.hiScore:.1f}"
        
        if self.health <= 0:
            print(f"High Score: {combinedScore:.1f}")
            self.stop()
            print(f"Final Score: {combinedScore:.1f}")            
            
class Instructions(simpleGE.Scene):
    def __init__(self, prevScore, hiScore):
        super().__init__()
        
        self.prevScore = prevScore
        self.hiScore = hiScore
        
        self.setImage("background1.png")
        self.response = "Quit"
        
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
        "You are Tiberius",
        "Avoid obstacles and collect gold.",
        "Use arrow keys to move.",
        "Survive for as long as you can!",]
        
        self.directions.center = (220, 180)
        self.directions.size = (400, 320)
        self.directions.bgColor = ((0xE0,0xE0,0xE0))
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (520, 90)
        self.btnPlay.size = (150, 80)
        self.directions.bgColor = ((0xE0,0xE0,0xE0))
        
        self.btnSave = simpleGE.Button()
        self.btnSave.text = "Save"
        self.btnSave.center = (520, 190)
        self.btnSave.size = (150, 80)
        self.directions.bgColor = ((0xE0,0xE0,0xE0))
        
        self.btnLoad = simpleGE.Button()
        self.btnLoad.text = "Load"
        self.btnLoad.center = (520, 290)
        self.btnLoad.size = (150, 80)
        self.directions.bgColor = ((0xE0,0xE0,0xE0))
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (520, 390)
        self.btnQuit.size = (150, 80)
        self.directions.bgColor = ((0xE0,0xE0,0xE0))
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = f"Previous Score: {self.prevScore:.1f}"
        self.lblScore.center = (220, 400)
        self.lblScore.size = (350, 80)
        self.directions.bgColor = ((0xE0,0xE0,0xE0))
        
        self.lblHiScore = simpleGE.Label()
        self.lblHiScore.text = f"High Score: {self.hiScore:.1f}"
        self.lblHiScore.center = (220, 420)
        self.lblHiScore.size = (350, 30)
        self.directions.bgColor = ((0xE0,0xE0,0xE0))
        
        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.btnSave,
                        self.btnLoad,
                        self.lblScore,
                        self.lblHiScore
                        ]
        
    def saveGame(highScore):
        data = {"hiScore": highScore}
        gameName = 'CastleQuestSave.dat'
        file = open(gameName, 'w')
        json.dump(data, file, indent=4)
        file.close()
        print("game saved")

    def loadGame():
        gameName = 'CastleQuestSave.dat'
        with open(gameName, 'r') as outFile:
            game = json.load(outFile)
        return game
        
    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()
        
        if self.btnSave.clicked:
            self.response = "Save"
            self.stop()
        
        if self.btnLoad.clicked:
            self.response = "Load"
            self.stop()
    
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
            
    def updateHiScore(self, hiScore):
        self.hiScore = hiScore
        self.lblHiScore.text = f"High Score: {self.hiScore:.1f}"
                    
def main():
    
    keepGoing = True
    lastScore = 0
    hiScore = 0
    
    while keepGoing:
        instructions = Instructions(lastScore, hiScore)
        instructions.start()
        
        if instructions.response == "Play":
            game = Game(hiScore)
            game.start()
            lastScore = game.score + game.timer.getElapsedTime()
            hiScore = game.hiScore
        
        elif instructions.response == "Save":
            Instructions.saveGame(hiScore)
        
        elif instructions.response == "Load":
            savedGame = Instructions.loadGame()
            hiScore = savedGame["hiScore"]
        
        else:
            keepGoing = False
            Instructions.saveGame(hiScore)
    
if __name__ == "__main__":
    main()