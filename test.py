#-*- oding:utf-8 -*-

import pygame
from pygame.locals import *
import time
import random

import sys
#1.抽象类

#2.封装

#3.继承
class Base(object):
    def __init__(self, g_window_temp, image_path,x, y):
        self.x = x 
        self.y = y
        self.g_window = g_window_temp 
        self.image = pygame.image.load(image_path)

class BasePlane(Base):

    def __init__(self, g_window_temp, image_path, bullet_image_path,x, y,plane_type_temp):
        Base.__init__(self, g_window_temp, image_path, x, y)
        
        self.bullet_list = []
        self.bullet_image_path = str(bullet_image_path)
        self.enemy_list = []

        self.airplane_type_dic = {0:'hero',1:'enemy0',2:'enemy1',3:'enemy2'}
        self.plane_type = plane_type_temp
        
        self.hit = False
        self.boom_image_list = []
        self.img_index = 0
        self.times = 0

        self.load_boom_image()


    def __del__(self):
        for image in self.airplane_type_dic:
            del image

        del self.image

    def display(self):
        
        #if plane is hitted boom
        if self.isHit() == True:
            self.air_crash()
                #del self and other resources
        else:
            self.g_window.blit(self.image,(self.x,self.y))
    
        #子弹越界销毁对象并重新创建新的子弹对象
        for bullet in self.bullet_list:
            
            if bullet.judge():
                self.bullet_list.remove(bullet)
            
            bullet.display()
            bullet.move()
            #if selfplane bullet hit enemy :enemy boom
            for enemy in self.enemy_list:
                if bullet.bingo(enemy):
                    #print('boom')
                    enemy.hit = True
                    self.enemy_list.remove(enemy)
    
    def add_enemy(self,enemy):
        self.enemy_list.append(enemy)

    def isHit(self):
        if self.hit == True:
            self.bullet_list.clear()
        return self.hit

    def load_boom_image(self):
        for i in range(1,5):
            path = './resource/'+self.airplane_type_dic[self.plane_type]+'_down'+str(i)+'.png'
            self.boom_image_list.append(pygame.image.load(path))

    def air_crash(self):
        if self.img_index <= 3:
            self.g_window.blit(self.boom_image_list[self.img_index],(self.x,self.y))
            self.times += 1
            if self.times == 12:
                self.times = 0
                self.img_index += 1
            if self.img_index == 3:

                print('boom!!!!!')


class BaseBullet(Base):
    def __init__(self, g_window_temp,airplane_temp, image_path):        
        Base.__init__(self,g_window_temp,image_path,0,0)
        self.x = airplane_temp.x + airplane_temp.image.get_width()//2 - self.image.get_width()//2 #往后更改获取对象图片的大小
        self.y = airplane_temp.y 
        
    def display(self):
        self.g_window.blit(self.image,(self.x,self.y))
        

    #when bullet hit targe_plane return True
    def bingo(self,target_plane):

        condition_x = (self.x + self.image.get_width()- target_plane.x )>= 0 and (self.x + self.image.get_width() - target_plane.x) <= target_plane.image.get_width()
        condition_y = (self.y + self.image.get_height() - target_plane.y )>= 0 and (self.y + self.image.get_height() - target_plane.y) <= target_plane.image.get_height()   
        
        if condition_x and condition_y:
            return True
        else:
            return False

class EnemyPlane(BasePlane):
    
    def __init__(self, g_window_temp, image_path, bullet_image_path, x, y,plane_type_temp):
        
        BasePlane.__init__(self,g_window_temp,image_path,bullet_image_path,x,y,plane_type_temp)
        self.direction_flag = False
    def move(self):
        #随机移动
        if self.x > 450:
            self.direction_flag = True

        if self.x < -30:
            self.direction_flag = False

        if not self.direction_flag:
            for i in range(random.randint(1,2)):
                self.x += 1 #moveing speed

        if self.direction_flag:
            for i in range(random.randint(1,2)):
                self.x -= 1
        #添加向下飞行功能 : pass

        self.y += 0.5

        
         
    def display(self):      
        BasePlane.display(self)

    def fire(self):
        #control bullet speed!
        #add bullet
        bullet_speed = random.randint(1,100)
        if bullet_speed == 5 or bullet_speed == 32:
            self.bullet_list.append(EnemyBullet(self.g_window, self,self.bullet_image_path))


class HeroPlane(BasePlane):
    
    def __init__(self, g_window_temp, image_path, bullet_image_path, x, y,plane_type_temp):
        
        BasePlane.__init__(self,g_window_temp, image_path, bullet_image_path,x,y,plane_type_temp)

        self.key_set = {pygame.K_UP:0, pygame.K_DOWN:0, pygame.K_LEFT:0, pygame.K_RIGHT:0}
        self.changeImage = 0

    def display(self):
        
        #heroplane 动画显示
        self.changeImage += 1
        if self.changeImage % 50 < 25:
            self.image = pygame.image.load('./resource/hero1.png')
        else:
            self.image = pygame.image.load('./resource/hero2.png')
    
        if self.changeImage > 10000:
            self.changeImage = 0
        #heroplane 动画显示

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
        self.bullet_list.append(HeroBullet(self.g_window,self,self.bullet_image_path))


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
            

#子弹：1.敌方子弹（e1,e2,e3,e3.1） 2.我方子弹（1）

class HeroBullet(BaseBullet):
    
    def __init__(self, g_window_temp,airplane_temp,image_path):     
        BaseBullet.__init__(self,g_window_temp,airplane_temp,image_path)

    def display(self):
        BaseBullet.display(self)
        
    def move(self):
        self.y -= 10 

    def judge(self):
        if self.y < 0:
            return True
        else:
            return False

class EnemyBullet(BaseBullet):
     
    def __init__(self, g_window_temp,airplane_temp,image_path):
        BaseBullet.__init__(self,g_window_temp,airplane_temp,image_path)
        self.y = airplane_temp.y + airplane_temp.image.get_height()
    def display(self):
        BaseBullet.display(self)

    def move(self):
        self.y += 5

    def judge(self):
        if self.y > 800:
            return True
        else:
            return False


def count_score(plane):
    global g_scores
    

    if plane.plane_type == 1:
        g_scores += 100
    elif plane.plane_type == 2:
        g_scores += 200
    elif plane.plane_type == 3:
        g_scores += 500

    g_enemy_plane_list.remove(plane)

def create_enemy_plane():
    global g_enemy_plane_list,g_hero_plane
    
    bullet_type = random.randint(1,2)
    enemy_type = random.randint(1,3)
    bullet_image = './resource/bullet'+str(bullet_type)+'.png'
    plane_image = './resource/enemy'+str(enemy_type-1)+'.png'
    x = random.randint(0,400)
    #y = random.randint(0,)
    y = 0

    if len(g_enemy_plane_list) >= 0 and len(g_enemy_plane_list) <= 4:
        new_enemy = EnemyPlane(g_window, plane_image, bullet_image, x, y, enemy_type)
        g_enemy_plane_list.append(new_enemy)
        new_enemy.add_enemy(g_hero_plane)
        g_hero_plane.add_enemy(new_enemy)
    #add_enemy()

def star_game():
    global g_window, g_background, g_enemy_plane_list, g_scores,g_hero_plane
    
    g_scores = 0
    g_window = pygame.display.set_mode((480,800),0,32)          #创建窗口
    pygame.display.set_caption('AircraftBattle')            #设置标题
    g_background = pygame.image.load("./resource/background.png")   #设置背景
    g_hero_plane = HeroPlane(g_window,"./resource/hero1.png",'./resource/bullet1.png',190,676,0)
    g_enemy_plane_list = []
    
def main():

    star_game()
    while True:
            
        #设定指定窗口显示的位置--设置
        
        g_window.blit(g_background,(0,0))#在哪个窗口的坐标开始
        
        create_enemy_plane()

        for enemy in g_enemy_plane_list:
            enemy.display()
            if not enemy.isHit():
                enemy.move()
                enemy.fire()
            if enemy.img_index == 3:
                count_score(enemy)

        if g_hero_plane.isHit():
            print('score:%d'%g_scores)
            #time.sleep(1)
        g_hero_plane.display()
        g_hero_plane.move() 
        g_hero_plane.key_control()      #控制飞机移动
        
        pygame.display.update()     #讲需要显示的内容从内存读取到显示器中--显示 
        
        time.sleep(0.001)
    
if __name__ == '__main__':

    main()

































