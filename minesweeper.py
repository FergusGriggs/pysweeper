import pygame, sys, math, time, os, random, string
from pygame.locals import *
TILESIZE=18
TILENUM=30
#TILESIZE=int(input("TILESIZE: "))
#TILENUM=int(input("TILENUM: "))
MINECOUNT=int((TILENUM**2)/9)
screenW=TILESIZE*TILENUM
screenH=TILESIZE*TILENUM+TILESIZE
screen=pygame.display.set_mode((screenW,screenH))
pygame.display.set_caption('pysweeper')
pygame.init()
class tile():
    def __init__(self,imgIndex,val):
        self.imgIndex=imgIndex
        self.val=val
        self.covered=True
        self.updated=False
class Board():
    def __init__(self,size,mineCount,pos,tileSize):
        self.size=size
        self.mineCount=mineCount
        self.pos=pos
        self.boardTiles=[]
        self.images=[]
        self.tileSize=tileSize
        self.lost=False
        self.rect=Rect(self.pos[0],self.pos[1],self.tileSize*self.size,self.tileSize*self.size)
        self.pressing2=False
        self.flagCount=0
        self.font=pygame.font.Font(None,int(tileSize*1.5))
        self.tick=0
        self.timing=False
        self.started=False
    def loadImages(self):
        tileset=pygame.transform.scale(pygame.image.load("tileset.jpg"),(int(self.tileSize*4),int(self.tileSize*3)))
        for i in range(3):
            for j in range(4):
                surf=pygame.Surface((self.tileSize,self.tileSize))
                surf.blit(tileset,(-self.tileSize*j,-self.tileSize*i))
                self.images.append(surf)
    def reset(self):
        self.boardTiles=[[tile(0,0) for i in range(self.size)] for j in range(self.size)]
        spacesPicked=[]
        for i in range(self.mineCount):
            rpos=(random.randint(0,self.size-1),random.randint(0,self.size-1))
            while rpos in spacesPicked:
                rpos=(random.randint(0,self.size-1),random.randint(0,self.size-1))
            spacesPicked.append(rpos)
            self.boardTiles[rpos[0]][rpos[1]].val=1
        self.tick=0
        self.timing=False
        self.lost=False
        self.flagCount=0
        self.started=False
        
    def draw(self):
        for i in range(len(self.boardTiles)):
            for j in range(len(self.boardTiles[i])):
                screen.blit(self.images[self.boardTiles[j][i].imgIndex],(i*self.tileSize+self.pos[0],j*self.tileSize+self.pos[1]))
    def drawStats(self):
        text=self.font.render(str(self.mineCount-self.flagCount),True,(0,0,0))
        screen.blit(self.images[2],(self.pos[0],self.pos[1]-self.tileSize))
        screen.blit(text,(self.pos[0]+self.tileSize,self.pos[1]-self.tileSize))
        if not self.timing and self.started:
            if self.lost:
                text=self.font.render("You Lost!",True,(0,0,0))
            else:
                text=self.font.render("You Won!",True,(0,0,0))
            screen.blit(text,(self.rect.centerx-text.get_width()/2,self.pos[1]-self.tileSize))
    def update(self):
        recurse=False
        for i in range(len(self.boardTiles)):
            for j in range(len(self.boardTiles[i])):
                if not self.boardTiles[i][j].covered:
                    if not self.boardTiles[i][j].updated:
                        if self.boardTiles[i][j].imgIndex==0 or self.boardTiles[i][j].imgIndex==1:
                            if self.boardTiles[i][j].imgIndex==1:
                                self.flagCount-=1
                            if self.boardTiles[i][j].val==1:
                                self.lost=True
                                self.timing=False
                                self.boardTiles[i][j].imgIndex=2
                            else:
                                neighbors=self.getNeighborCount((i,j))
                                if neighbors==0:
                                    if i>0:
                                        self.boardTiles[i-1][j].covered=False
                                        if j>0:
                                            self.boardTiles[i-1][j-1].covered=False
                                        if j<self.size-1:
                                            self.boardTiles[i-1][j+1].covered=False
                                    if i<self.size-1:
                                        self.boardTiles[i+1][j].covered=False
                                        if j>0:
                                            self.boardTiles[i+1][j-1].covered=False
                                        if j<self.size-1:
                                            self.boardTiles[i+1][j+1].covered=False
                                    if j>0:
                                        self.boardTiles[i][j-1].covered=False
                                    if j<self.size-1:
                                        self.boardTiles[i][j+1].covered=False
                                    recurse=True
                                self.boardTiles[i][j].imgIndex=3+neighbors
                            self.boardTiles[i][j].updated=True
        if recurse:
            self.update()
                            
                            
                    
    def getNeighborCount(self,pos):
        neighbors=0
        if pos[0]>0:
            if self.boardTiles[pos[0]-1][pos[1]].val==1:neighbors+=1
            if pos[1]>0:
                if self.boardTiles[pos[0]-1][pos[1]-1].val==1:neighbors+=1
            if pos[1]<self.size-1:
                if self.boardTiles[pos[0]-1][pos[1]+1].val==1:neighbors+=1
        if pos[0]<self.size-1:
            if self.boardTiles[pos[0]+1][pos[1]].val==1:neighbors+=1
            if pos[1]>0:
                if self.boardTiles[pos[0]+1][pos[1]-1].val==1:neighbors+=1
            if pos[1]<self.size-1:
                if self.boardTiles[pos[0]+1][pos[1]+1].val==1:neighbors+=1
        if pos[1]>0:
            if self.boardTiles[pos[0]][pos[1]-1].val==1:neighbors+=1
        if pos[1]<self.size-1:
            if self.boardTiles[pos[0]][pos[1]+1].val==1:neighbors+=1
        return neighbors
        
    def takeInput(self):
        if not self.lost:
            if pygame.mouse.get_pressed()[0]:
                m=pygame.mouse.get_pos()
                if self.rect.collidepoint(m):
                    self.started=True
                    m=(m[0]-self.pos[0],m[1]-self.pos[1])
                    self.boardTiles[m[1]//self.tileSize][m[0]//self.tileSize].covered=False
                    self.update()
            if pygame.mouse.get_pressed()[2]:
                if not self.pressing2:
                    self.pressing2=True
                    m=pygame.mouse.get_pos()
                    if self.rect.collidepoint(m):
                        m=(m[0]-self.pos[0],m[1]-self.pos[1])
                        if self.boardTiles[m[1]//self.tileSize][m[0]//self.tileSize].covered==True:
                            if self.boardTiles[m[1]//self.tileSize][m[0]//self.tileSize].imgIndex==1:
                                self.boardTiles[m[1]//self.tileSize][m[0]//self.tileSize].imgIndex=0
                                self.flagCount-=1
                            else:
                                self.boardTiles[m[1]//self.tileSize][m[0]//self.tileSize].imgIndex=1
                                self.flagCount+=1
            else:
                self.pressing2=False
    def updateClock(self):
        if self.mineCount-self.flagCount==0:
            count=0
            for i in range(len(self.boardTiles)):
                for j in range(len(self.boardTiles[i])):
                    if self.boardTiles[i][j].imgIndex==0:
                        count+=1
            if count==0:
                self.timing=False
        elif self.lost:
            self.timing=False
        elif self.started:
            self.timing=True
        if self.timing:
            self.tick+=deltaTime
        t1=str(int((self.tick/1000)//60))
        t2=str(round((self.tick/1000)%60,1))
        if len(t1)<2:
            t1="0"+t1
        if len(t2)<4:
            t2="0"+t2
        text=self.font.render(t1+":"+t2,True,(0,0,0))
        screen.blit(text,(self.rect.right-text.get_width(),self.pos[1]-self.tileSize))
board=Board(TILENUM,MINECOUNT,(0,TILESIZE),TILESIZE)
board.loadImages()
board.reset()
board.update()
clock=pygame.time.Clock()
while 1:
    deltaTime=clock.tick()
    board.takeInput()
    screen.fill((190,190,190))
    board.draw()
    board.drawStats()
    board.updateClock()
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==KEYDOWN:
            if event.key==K_r:
                board.reset()
    pygame.display.update()
    pygame.display.flip()
