# Typing Wiz pycap game v1.0
# Written by George Jones

appIni = { "mCompanyName": "GeorgeJonesSoftware",
		"mFullCompanyName": "GeorgeJonesSoftware",
		"mProdName": "Typing Wiz",
		"mProductVersion": "1.0",
		"mTitle": "Typing Wiz",
		"mRegKey": "TypingWiz",
		"mWidth": 900,
		"mHeight": 600,
		"mAutoEnable3D": 1,
		"mVSyncUpdates": 1 }

import Pycap as PC
import VerticalImageMenu
import twiz

PCR = None
gm = None
theSong = None

menuFiles = ['titlepage_top', 'titlepage_middle', 'titlepage_middle2', 'titlepage_bottom']
menuImages = []

class Background:
	def __init__(self, img):
		self.setImage(img)
		
	def draw(self):
		PC.drawImage(self.image, 0, 0)
		
	def setImage(self, img):
		self.image = img
		
class GameMaster:
	def __init__(self):
		self.menuStep = 0
		self.level = 0
		self.speed = 0
		self.songTimer = 0
		self.current = VerticalImageMenu.Numbered(self, PC, PCR, [menuImages[0], menuImages[1], menuImages[3]], 1, 5)
		PC.playSound(theSong)

	def update(self, delta):
		self.songTimer += delta	
		if self.songTimer == 8275: # what a magical number!
			self.songTimer = 0			
			PC.playSound(theSong)
		if self.current:
			self.current.update(delta)
			
	def draw(self):		
		if self.current:
			self.current.draw()
	
	def keyDown(self, key):
		if self.current:
			res = self.current.keyDown(key)
			if res > -1:
				if self.menuStep == 0:
					self.level = res
					self.menuStep = 1
					self.current = VerticalImageMenu.Numbered(self, PC, PCR, [menuImages[0], menuImages[2], menuImages[3]], 1, 5)
				elif self.menuStep == 1:
					self.speed = res					
					self.menuStep = -1
					self.current = twiz.Game(self, PC, PCR, self.level, self.speed)

	def gameComplete(self):
		self.menuStep = 0
		self.current = VerticalImageMenu.Numbered(self, PC, PCR, [menuImages[0], menuImages[1], menuImages[3]], 1, 5)
					
					
def loadBase():
	import PycapRes
	global PCR
	global theSong
	
	PCR = PycapRes	
	
	for src in menuFiles:
		menuImages.append(PCR.loadImage('Res\\Images\\' + src))
		
	theSong = PCR.loadSound('Res\\Sound\\wizsong')

def init():	
	global gm	
	gm = GameMaster()
	
def update(delta):
	# Tell the engine that we need to call the draw function
	gm.update(delta)
	PC.markDirty()

def draw():	
	gm.draw()

def keyDown(key):	
	gm.keyDown(key)
	