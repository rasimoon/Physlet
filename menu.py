import pygame
import subprocess
import sys
import os
import shelve 
import get_constants
from multiprocessing import freeze_support

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load('icon.png').convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption('Physlet')



logo_img = pygame.image.load('Images/logo.png').convert_alpha()
logo_width = logo_img.get_width()
logo_height = logo_img.get_height() 
logo_img = pygame.transform.scale(logo_img, (int(logo_width* 2), int(logo_height * 2)))

ex_img = pygame.image.load('Images/buttons/examples.png').convert_alpha()
sand_img = pygame.image.load('Images/buttons/sandbox.png').convert_alpha()
opt_img = pygame.image.load('Images/buttons/options.png').convert_alpha()

wip_img = pygame.image.load('Images/text/wip.png').convert_alpha()


class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False 

    def draw(self):
           pos = pygame.mouse.get_pos()
           execute = False 
           if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True  
                execute = True 
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False 

           screen.blit(self.image, (self.rect.x, self.rect.y))
           return execute 
        

examples_button = Button(275, 100, ex_img, scale=1)
sandbox_button = Button(275, 225, sand_img, scale=1)
options_button = Button(275, 350, opt_img, scale=1)

if __name__ == '__main__':
   freeze_support()
   
   run = True
   main_menu = True 
   examples = False
   sandbox = False 
   options = False
   work_in_progress = False 
   get_kinematics = False 

   while run:
    
    screen.fill((0, 180, 250))
    lox = 190
    loy = 0
    
    events = pygame.event.get()

    if main_menu:
      screen.blit(logo_img, (lox, loy))
      if examples_button.draw():
        examples = True 
        main_menu = False 
      elif sandbox_button.draw():
        main_menu = False 
        sandbox = True 
        work_in_progress = True 
      elif options_button.draw():
        main_menu = False 
        options = True 
        work_in_progress = True 
    
    if examples:
        kin1_img = pygame.image.load("Images/buttons/kin-1.png").convert_alpha()
        kin2_img = pygame.image.load("Images/buttons/kin-2.png").convert_alpha()

        kinematics1_button = Button(50, 10, kin1_img, scale=0.8)
        kinematics2_button = Button(50, 100, kin2_img, scale=0.8)
    
        if kinematics1_button.draw():
         examples = False 
         run = False  
         pygame.quit()
         with shelve.open('constants') as constants:
            constants['chosen_example'] = 1
         get_constants.get_constants()
         break
         #script_path = os.path.abspath("get_constants.py")
         #subprocess.run([sys.executable, script_path]) 
         

        if kinematics2_button.draw():
          work_in_progress = True  

        for event in events:
           if event.type == pygame.KEYDOWN:
              examples = False 
              main_menu = True 
          
    if work_in_progress:
        examples = False 
        screen.blit(wip_img, (0,0))
        for event in events:
         if event.type == pygame.KEYDOWN:
            work_in_progress = False 
            if sandbox or options == True:
               sandbox = False
               options = False 
               main_menu = True 
            else:
               examples = True 

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()


