import pygame
from kinematics import get_x_pos 
import numpy as np
from threading import Thread, Event 
from multiprocessing import Process 
import time as time_module 
import shelve 
from graph import get_graph

def app():

  pygame.init()
  SCREEN_HEIGHT = 500
  SCREEN_WIDTH = 800
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  icon = pygame.image.load('icon.png').convert_alpha()
  pygame.display.set_icon(icon)
  pygame.display.set_caption('Physlet: Examples')
  
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

  background_img = pygame.image.load('Images/backgrounds/basic-floor.png').convert_alpha()
  cart_img = pygame.image.load("Images/sprites/cart.png").convert_alpha()
  grph_but_img = pygame.image.load("Images/buttons/graph.png").convert_alpha()
  reset_but_img = pygame.image.load("Images/buttons/reset.png").convert_alpha()

  pos_grph_but_img = pygame.image.load("Images/buttons/graph-pos.png").convert_alpha()
  vel_grph_but_img = pygame.image.load("Images/buttons/graph-vel.png").convert_alpha()
  acc_grph_but_img = pygame.image.load("Images/buttons/graph-acc.png").convert_alpha()

  graph_button = Button(600, 20, grph_but_img, scale=0.5)
  reset_button = Button(75, 25, reset_but_img, scale=0.5)
  pos_button = Button(600,70, pos_grph_but_img, scale=0.5 )
  vel_button = Button(600, 95, vel_grph_but_img, scale=0.5)
  acc_button = Button(600, 120, acc_grph_but_img, scale=0.5)

  with shelve.open('constants') as constants:
        dt = constants['dt']

  def update_time(time_interval, stop_event):
    global time 
    time = 0
    while not stop_event.is_set():
        time += 1
        time_module.sleep(time_interval) 
    print('thread exit')


  stop_event = Event() 
  time_p = Thread(target=update_time, args=(dt,stop_event))
  time_p.start()

  run = True
  show_sub_graph = False 
  reset = False 
  while run:
     
     if reset:
         x_not = get_x_pos(time)
         reset = False 
     else:
         try:
            cart_x = get_x_pos(time) - x_not
         except:
             cart_x = get_x_pos(time)  

     screen.blit(background_img, (0, 0))
     screen.blit(cart_img, (cart_x,180))

     if show_sub_graph:
         snap_time = time 
         if pos_button.draw():
              graph_process = Process(target=get_graph, args=(snap_time,'position'))
              graph_process.start()
         elif vel_button.draw():
              graph_process = Process(target=get_graph, args=(snap_time,'velocity'))
              graph_process.start()
         elif acc_button.draw():
              graph_process = Process(target=get_graph, args=(snap_time,'acceleration'))
              graph_process.start()

     if graph_button.draw():
         if show_sub_graph == False:
             show_sub_graph = True 
         elif show_sub_graph == True:
             show_sub_graph = False 
         
        #snap_time = time 
        #graph_process = Process(target=get_graph, args=(snap_time,))
        #graph_process.start()
    
     if reset_button.draw():
         reset = True 

     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
     pygame.display.update()

  stop_event.set()
  try:
      graph_process.terminate()
  except:
      pass 

  pygame.quit()

