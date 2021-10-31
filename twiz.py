import random
import time

PC = None
PCR = None

game_levels = [
    { 'bg':'bg1', 'letters':['F','J'] },
    { 'bg':'bg2', 'letters':['A','S','D','F','G','H','J','K','L'] },
    { 'bg':'bg3', 'letters':['Q','W','E','R','T','Y','U','I','O','P'] },
    { 'bg':'bg4', 'letters':['Z','X','C','V','B','N','M'] },
    { 'bg':'bg5', 'letters':['A','B','C','D','E','F','G','H','I','J','K','L',
                             'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'] }
]

letter_images = {
    'a':0,
    'b':0,
    'c':0,
    'd':0,
    'e':0,
    'f':0,
    'g':0,
    'h':0,
    'i':0,
    'j':0,
    'k':0,
    'l':0,
    'm':0,
    'n':0,
    'o':0,
    'p':0,
    'q':0,
    'r':0,
    's':0,
    't':0,
    'u':0,
    'v':0,
    'w':0,
    'x':0,
    'y':0,
    'z':0
}

wiz_sequences = {
    'normal':['wizn1', 'wizn2', 'wizn3'],
    'blink':['wizb1', 'wizb2', 'wizb3'],
    'oh':['wizo1', 'wizo2', 'wizo3'],
    'cast':['wizn1', 'wizc1', 'wizc2', 'wizc3', 'wizc2', 'wizc1', 'wizc4', 'wizn1']
}

wiz_actions = {
    'normal':0,
    'blink':1,
    'oh':2,
    'cast':3
}

ball_files = {
    'blue':'blue_ball',
    'red':'red_ball',
    'yellow':'yellow_ball'
}

ball_images = {
    'blue':0,
    'red':0,
    'yellow':0
}

img_dir = 'Res\\Images\\'
blink_chance = 0.04
process_interval = 40
paint_time = 20
width = 900
letterY = 300
numOh = 5
eballs = 10
tank = ((50,190),(185,525))
eballOpacity = [220, 180, 140]
eballRadius = [5, 4, 3]
eballMax = 50
wizIncrement = 5
roundTime = 30

class Game:
    def __init__(self, gm, inPC, inPCR, level, speed):
        global PC, PCR
        PC = inPC
        PCR = inPCR
        self.gm = gm
        self.level = level - 1
        self.speed = speed
        self.letters = []
        self.action = 'normal'
        self.game_level = game_levels[self.level]
        self.bgImage = PCR.loadImage(img_dir + self.game_level['bg'])
        self.tubeBaseImage = PCR.loadImage(img_dir + 'tube_base.png')
        self.tubeGlassImage = PCR.loadImage(img_dir + 'tube_glass.png')
        self.tubeLidImage = PCR.loadImage(img_dir + 'tube_lid.png')
        self.right = 0
        self.wrong = 0
        self.missed = 0

        if self.speed == 1:
            self.letter_speed = 0.5
        elif self.speed == 2:
            self.letter_speed = 1
        elif self.speed == 3:
            self.letter_speed = 3
        elif self.speed == 4:
            self.letter_speed = 6
        elif self.speed == 5:
            self.letter_speed = 10
        
        self.wizImages = {}
        for k,seq in wiz_sequences.iteritems():
            self.wizImages[k] = [PCR.loadImage(img_dir + src) for src in seq]
            
        for k in ball_images.keys():
            ball_images[k] = PCR.loadImage(img_dir + ball_files[k])
            
        for k in letter_images.keys():
            letter_images[k] = PCR.loadImage(img_dir + 'letters\\' + k.lower())      

        self.eballs = []
        self.MakeEnergyBalls(eballs, None)
        self.wizT = 0
        self.wizTi = 0
        self.letterX = width        
        self.initialT = time.clock()
        self.gameOver = False    
        self.bigFont = PCR.sysFont('Arial', 24, False, True)
        self.smallFont = PCR.sysFont('Arial', 14, False, True)
        self.ohSound = PCR.loadSound('Res\\Sound\\ooh')
        self.wandSound = PCR.loadSound('Res\\Sound\\wand')
        
    def MakeEnergyBalls(self, n, theColor):
        possible_colors = ['red', 'blue', 'yellow'];
        possible_v = [-4, -3, -2, -1, 1, 2, 3, 4]
        color = theColor
        for i in range(0, n):
            x = random.randint(tank[0][0], tank[1][0])
            y = random.randint(tank[0][1], tank[1][1])
            if theColor == None:
                color = random.choice(possible_colors)                
            self.eballs.append([
                x,
                y,
                random.choice(possible_v), # x direction
                random.choice(possible_v), # y direction
                color
            ])        

    def draw(self):
        PC.drawImage(self.bgImage, 0, 0)
        PC.drawImage(self.tubeBaseImage, 30, 500)
        
        # draw letters
        for i, letter in enumerate(self.letters):
            if letter != '':
                pos = self.letterX + i*width/3
                PC.drawImageF(letter_images[letter.lower()], pos, letterY)                
        
        # energy things
        for eball in self.eballs:            
            PC.drawImage(ball_images[eball[4]], eball[0]-6, eball[1]-6)
        
        # glass        
        PC.drawImage(self.tubeGlassImage, 39, 150)
        
        # lid
        PC.drawImage(self.tubeLidImage, 30, 120)
        
        # the wiz
        if self.wizT >= len(self.wizImages[self.action]):
            self.wizT = 0
            if self.action == 'oh' and self.numOh > 0:
                self.numOh -= 1
            elif random.random() <= blink_chance:
                self.action = 'blink'
            else:
                self.action = 'normal'
        self.wizPic = self.wizImages[self.action][self.wizT]        
        PC.drawImage(self.wizPic, 85, 10)
        
        if self.gameOver:
            PC.setColour(255, 255, 255, 10)
            PC.fillRect(216, 146, 550, 290)
            PC.fillRect(217, 147, 548, 288)
            PC.fillRect(218, 148, 546, 286)
            PC.fillRect(219, 149, 544, 284)
            
            PC.setColour(255, 255, 255, 255)
            PC.setFont(self.bigFont)
            PC.drawString("Game Over", 403, 200)
            PC.setFont(self.smallFont)
            PC.drawString("Right: %d" % self.right, 410, 258)
            PC.drawString("Wrong: %d" % self.wrong, 410, 293)
            PC.drawString("Missed: %d" % self.missed, 410, 328)
            PC.setFont(self.bigFont)
            PC.drawString("Press Enter to return to the menu.", 230, 400)
        
    def update(self, delta):
        self.wizTi += 1
        if self.wizTi == wizIncrement:
            self.wizTi = 0
            self.wizT += 1
            
        t = time.clock()
        if t - self.initialT > roundTime:
            self.GameOver()
            return
        
        if len(self.letters) == 0:
            self.letters = [self.GetLetter() for x in range(0,3)]
        
        if self.letterX <= 0:
            if self.letters[0] != '':
                self.wizOh()
            self.letters = self.letters[1:]
            self.letters.append(self.GetLetter())
            self.letterX += int(width / 3)
        self.letterX -= self.letter_speed
        
        for eball in self.eballs:
            if eball[0] <= tank[0][0] or eball[0] >= tank[1][0]:
                eball[2] *= -1
            if eball[1] <= tank[0][1] or eball[1] >= tank[1][1]:
                eball[3] *= -1                    
            eball[0] += eball[2]
            eball[1] += eball[3]
                
    def wizOh(self):
        self.wizT = 0
        self.wizTi = 0
        self.missed += 1
        self.numOh = numOh
        # remove an energy ball
        if len(self.eballs) > 0:
            self.eballs = self.eballs[1:]
        self.action = 'oh'
        PC.playSound(self.ohSound)
    
    def wizCast(self, letter):
        self.wizT = 0
        self.wizTi = 0
        self.action = 'cast'
        self.right += 1
        
        # figure out idx
        color = None
        if letter in game_levels[1]['letters']:
            color = 'red'
        elif letter in game_levels[2]['letters']:
            color = 'yellow'
        elif letter in game_levels[3]['letters']:
            color = 'blue'
        
        if len(self.eballs) < eballMax:
            self.MakeEnergyBalls(1, color)
        PC.playSound(self.wandSound)
            
    def GetLetter(self):
        return random.choice(self.game_level['letters'])            

    def keyDown(self, key):
        val = key
        letterRight = -1
        matchLetter = ''
        
        if self.gameOver:
            if val == 13:
                self.gm.gameComplete()
            else:
                print(val)
        else:        
            for i, letter in enumerate(self.letters):
                if letter != '':
                    if ord(letter) == val:
                        letterRight = i
                        matchLetter = letter
                    break
        
        if letterRight >= 0:
            self.letters[letterRight] = ''
            self.wizCast(matchLetter)
        else:
            self.wrong += 1
        
        
    def GameOver(self):
        self.gameOver = True
        self.letters = []
 