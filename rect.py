import pygame

from pygame.locals import *

class Image(object):
	def __init__(self,path,x,y):
		self.image = pygame.image.load(path)
		self.x = x
		self.y = y
		self.midx = self.x + self.image.get_width()/2


	def move(self,other):
	
		if abs(self.midx-other.midx) >= (self.image.get_width()/2 + other.image.get_width()/2):
			self.x += 2
		else:
			self.x -= 2
def main():


	window = pygame.display.set_mode((500,400),0,32)
	bg = pygame.image.load("./resource/background.png")
	img1 = Image("./resource/hero1.png",0,0)
	img2 = Image("./resource/enemy0.png",100,0)
	window.blit(bg,(0,0))
	while True:

		window.blit(img1.image,(img1.x,img1.y))
		window.blit(img2.image,(img2.x,img2.y))
		#move(x1,y1)
		#move(x2,y2)
main()