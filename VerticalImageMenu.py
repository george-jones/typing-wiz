PC = None
PCR = None

class Numbered:
    def __init__(self, gm, inPC, inPCR, imgs, minNum, maxNum):
        global PC, PCR
        PC = inPC
        PCR = inPCR
        self.images = [(im, PCR.imageHeight(im)) for im in imgs]
        self.minNum = minNum
        self.maxNum = maxNum

    def draw(self):
        prevY = 0
        for (im, height) in self.images:			
            PC.drawImage(im, 0, prevY)
            prevY += height
            
    def update(self, delta):
        pass

    def keyDown(self, key):
        val = key - 48
        if val >= self.minNum and val <= self.maxNum:
            return val
        else:
            return -1