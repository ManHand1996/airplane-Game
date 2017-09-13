#-*- oding:utf-8 -*-

import pygame
from pygame.locals import *
import time
import random

import sys

class Base(object):
	def __init__(self, window_temp, image_path,x, y):
		self.x = x 
		self.y = y
		self.window = window_temp
		if image_path != '':
			self.image = pygame.image.load(image_path)
		else:
			self.image = None
class BasePlane(Base):

	def __init__(self, window_temp,x, y,plane_type_temp):
		Base.__init__(self, window_temp, '', x, y)
		
		self.bullet_list = []
		self.enemy_list = []
		self.boom_image_list = []

		self.airplane_type_dic = {0:'hero',1:'enemy0',2:'enemy1',3:'enemy2'}
		self.plane_type = plane_type_temp
		
		self.hit = False
		self.img_index = 0#boom image_index
		self.times = 0

		self.changeImage = 0
		self.load_boom_image()
		self.HP = self.set_HP()

	def set_HP(self):
		if self.plane_type == 0 or self.plane_type == 1:
			return 100
		elif self.plane_type == 1:
			return 200
		else:
			return 500

	def display(self):
				
		#heroplane 动画显示
		self.changeImage += 1
		if self.changeImage % 50 < 25:
			self.image = pygame.image.load('./resource/'+str(self.airplane_type_dic[self.plane_type])+'.png')
		else:
			self.image = pygame.image.load('./resource/'+str(self.airplane_type_dic[self.plane_type])+'_hit.png')
	
		if self.changeImage > 10000:f
			self.changeImage = 0
		#heroplane 动画显示



		#if plane is hitted boom
		if self.isHit() == True:
			self.air_crash()
		else:
			self.window.blit(self.image,(self.x,self.y))
	
		#子弹越界销毁对象并重新创建新的子弹对象
		for bullet in self.bullet_list:
			self.bullet_hit(bullet)
			if bullet.is_bullet_overstep() and self.bullet_index(bullet):
				self.bullet_list.remove(bullet)
			
			bullet.display()
			bullet.move()



	def is_over(self):
		if self.img_index == 3:
			return True
		else:
			return False
	#if bullet in bullet_list return True 
	#remove(x) bug- catch and return False
	def bullet_index(self,bullet):
		try:
			self.bullet_list.index(bullet)
			
		except ValueError:
			print('valueError')
			return False
		else:
			return True

	#remove bullet when this bullet hit enemy
	def bullet_hit(self,bullet):
		for enemy in self.enemy_list:
			if bullet.bingo(enemy) and self.bullet_index(bullet):
				self.bullet_list.remove(bullet)
				enemy.HP -= 100
				if enemy.HP == 0:
					enemy.hit = True					
					self.enemy_list.remove(enemy)




	def add_enemy(self,enemy):
		self.enemy_list.append(enemy)

	#if enemy plane or hero clear remove all bullet 
	def isHit(self):
		if self.hit == True:
			self.bullet_list.clear()
		return self.hit

	def load_boom_image(self):
		for i in range(1,5):
			path = './resource/'+self.airplane_type_dic[self.plane_type]+'_down'+str(i)+'.png'
			self.boom_image_list.append(pygame.image.load(path))

	# airplane boom
	def air_crash(self):
		if self.img_index <= 3:
			self.window.blit(self.boom_image_list[self.img_index],(self.x,self.y))
			self.times += 1
			if self.times == 12:
				self.times = 0
				self.img_index += 1



class BaseBullet(Base):
	def __init__(self, window_temp,airplane_temp, image_path):		
		Base.__init__(self,window_temp,image_path,0,0)
		self.x = airplane_temp.x + airplane_temp.image.get_width()//2 - self.image.get_width()//2 # airplane image mid_x
		self.y = airplane_temp.y 
		
	def display(self):
		self.window.blit(self.image,(self.x,self.y))
		

	#when bullet hit targe_plane return True
	def bingo(self,target_plane):
		
		#range of hit area x,y
		area_x = self.x + self.image.get_width()- target_plane.x
		area_y = self.y + self.image.get_height() - target_plane.y

		condition_x = area_x >= 0 and area_x <= target_plane.image.get_width()
		
		condition_y = area_y >= 0 and area_y <= target_plane.image.get_height()	
		
		if condition_x and condition_y:
			return True
		else:
			return False

class EnemyPlane(BasePlane):
	
	def __init__(self, window_temp, x, y,plane_type_temp):
		
		BasePlane.__init__(self,window_temp,x,y,plane_type_temp)
		self.direction_flag = False
		
	def move(self):
		#随机移动
		if self.x > 450:
			self.direction_flag = True

		if self.x < -30:
			self.direction_flag = False

		if not self.direction_flag:
			self.x += 4 #moveing speed
		else:
			self.x -= 4

		self.y += 1
	
		 
	def display(self):		
		BasePlane.display(self)

	def fire(self):
		#control bullet speed!
		#add bullet
		bullet_speed = random.randint(1,100)
		if (bullet_speed == 5):
			self.bullet_list.append(EnemyBullet(self.window, self))
		
	def is_overstep(self):
		if self.y > 800:
			return True
		else:
			return False


class HeroPlane(BasePlane):
	
	def __init__(self, window_temp, x, y,plane_type_temp):
		
		BasePlane.__init__(self,window_temp,x,y,plane_type_temp)

		self.key_set = {pygame.K_UP:0, pygame.K_DOWN:0, pygame.K_LEFT:0, pygame.K_RIGHT:0}
		#self.changeImage = 0

	def display(self):


		BasePlane.display(self)	

	def move(self):
		#1.根据按键修改偏移量，让飞机移动

		self.x += (self.key_set[pygame.K_RIGHT] - self.key_set[pygame.K_LEFT])
		self.y +=  (self.key_set[pygame.K_DOWN] - self.key_set[pygame.K_UP])
		
		#2.判断边界
		if self.x <= 0:
			self.x = 0
		elif self.x >= 380:
			self.x = 380

		if self.y >= 676:
			self.y = 676
		elif self.y <= 0:
			self.y = 0

	def fire(self):
		#添加子弹
		self.bullet_list.append(HeroBullet(self.window,self))


	def key_control(self):
		
		#键盘，鼠标等的事件
		for event in pygame.event.get():
			
			#判断是否点击了退出按钮
			if event.type == QUIT:
				sys.exit()
			
			#判断键盘按键
			elif event.type == KEYDOWN:
				
				if  event.key == pygame.K_SPACE:
					if not self.isHit():
						self.fire()
				
				elif event.key in self.key_set:
					self.key_set[event.key] = 6
						
			elif event.type ==KEYUP:
			
				if event.key in self.key_set:
					self.key_set[event.key] = 0
			



class HeroBullet(BaseBullet):
	
	def __init__(self, window_temp,airplane_temp):		
		BaseBullet.__init__(self,window_temp,airplane_temp,'./resource/bullet.png')

	def display(self):
		BaseBullet.display(self)
		
	def move(self):
		self.y -= 10 

	def is_bullet_overstep(self):
		if self.y < 0:
			return True
		else:
			return False

	#def change bullet image 

class EnemyBullet(BaseBullet):
	 
	def __init__(self, window_temp,airplane_temp):
		BaseBullet.__init__(self,window_temp,airplane_temp,'./resource/bullet'+str(airplane_temp.plane_type)+'.png')
		
		self.y = airplane_temp.y + airplane_temp.image.get_height()
	def display(self):
		BaseBullet.display(self)

	def move(self):
		self.y += 5

	def is_bullet_overstep(self):
		if self.y > 800:
			return True
		else:
			return False


#----------------------------------------------------------------------------------
#
#add class to manage game initalize
#
#----------------------------------------------------------------------------------

class GameManage(object):

	def __init__(self):
		
		self.g_window = pygame.display.set_mode((480,800),0,32)
		self.g_background = pygame.image.load("./resource/background.png")
		self.g_enemy_plane_list = []
		self.pause_img_list = []
		self.pause_img = None
		self.g_hero_plane = None
		self.g_scores = 0
		self.pause = False
		self.game_font = None
		self.text_surface = None

	def initalize(self):
		
		pygame.init()

		self.pause_img_list.append(pygame.image.load('./resource/game_pause_nor.png'))
		self.pause_img_list.append(pygame.image.load('./resource/game_resume_nor.png'))
		self.pause_img = self.pause_img_list[0]
		loading_img_list = []

		self.g_hero_plane = HeroPlane(self.g_window,190,676,0)
		self.g_window.blit(self.g_background,(0,0))
		
		pygame.display.set_caption('AircraftBattle')
		self.game_font = pygame.font.Font('freesansbold.ttf',35)

		#loading pucture
		for i in range(0,4):
			loading_img_list.append(pygame.image.load('./resource/game_loading'+str(i+1)+'.png')) 
			self.g_window.blit(loading_img_list[i],(100,100))
			time.sleep(0.5)
			pygame.display.update()

	def create_enemy_plane(self):
		enemy_type = random.randint(1,3)
		x = random.randint(0,400)
		y = -100

		if len(self.g_enemy_plane_list) >= 0 and len(self.g_enemy_plane_list) <= 4:
		
			new_enemy = EnemyPlane(self.g_window, x, y, enemy_type)
			self.g_enemy_plane_list.append(new_enemy)
			new_enemy.add_enemy(self.g_hero_plane)
			self.g_hero_plane.add_enemy(new_enemy)
	
	def count_score(self,plane):

		if plane.plane_type == 1:
			self.g_scores += 100
		elif plane.plane_type == 2:
			self.g_scores += 200
		elif plane.plane_type == 3:
			self.g_scores += 500

		self.g_enemy_plane_list.remove(plane)



	def control(self):

		mouse_x,mouse_y = pygame.mouse.get_pos()

		for event in pygame.event.get():

			self.pause_game(event,mouse_x)
			#判断是否点击了退出按钮

			if event.type == QUIT:
				sys.exit()
			
			if not self.pause:
			#判断键盘按键
				if event.type == KEYDOWN:
					
					if  event.key == pygame.K_SPACE:
						if not self.g_hero_plane.isHit():
							self.g_hero_plane.fire()
					
					elif event.key in self.g_hero_plane.key_set:
						self.g_hero_plane.key_set[event.key] = 6
							
				elif event.type == KEYUP:
				
					if event.key in self.g_hero_plane.key_set:
						self.g_hero_plane.key_set[event.key] = 0


	def pause_game(self,event,x):

		if x > 438 and x < 800:
			if event.type == MOUSEBUTTONDOWN and not self.pause:
				self.pause_img = self.pause_img_list[1]
				print('stop')
				self.pause = not self.pause
			elif event.type == MOUSEBUTTONDOWN and self.pause:
				self.pause_img = self.pause_img_list[0]
				print('start')
				self.pause = not self.pause


	def display(self):

		self.text_surface = self.game_font.render(str(self.g_scores),True,(0,0,0))
		self.g_window.blit(self.g_background,(0,0))
		self.g_window.blit(self.text_surface,(0,0))
		self.g_window.blit(self.pause_img,(438,0))
		
def main():

	game = GameManage()
	game.initalize()
	
	
	while True:
		pygame.init()
		while not game.pause:
			game.control()
			game.display()
			
			#game.g_window.blit(game.pause_img,(438,0))
			#--------------------
			game.create_enemy_plane()

			for enemy in game.g_enemy_plane_list:

				if enemy.is_overstep():
					game.g_enemy_plane_list.remove(enemy)

				enemy.display()
				if not enemy.isHit():
					enemy.move()
					enemy.fire()
				#else:
					#g_enemy_plane_list.remove(enemy)
				if enemy.img_index == 3:
					game.count_score(enemy)

			if game.g_hero_plane.isHit():
				print('score:%d'%game.g_scores)
				#restart()
				game.g_hero_plane.hit = False
				#time.sleep(1)
			game.g_hero_plane.display()
			game.g_hero_plane.move()	
			
			pygame.display.update() #讲需要显示的内容从内存读取到显示器中--显示	
			time.sleep(0.001)		
			
			

		while game.pause:
			game.control()
			
			pygame.display.update() #讲需要显示的内容从内存读取到显示器中--显示	
			time.sleep(0.001)		
	
	
if __name__ == '__main__':

	main()

































