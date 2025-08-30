import matplotlib
import pygame 
from kinematics import get_x_pos, get_x_vel, get_x_acc  
matplotlib.use('Agg')  
import time as time_module 
from threading import Thread
import shelve 

import matplotlib.pyplot as plt
import numpy as np

def get_graph(initial_time, type_chosen):


 def display_graph(x, y, pos, type):
  plt.clf()
  x = np.linspace(x[0], x[1], x[2])
  try: 
     plt.plot(x,y, color='blue')
  except:
     y = np.full_like(x, y)
     plt.plot(x,y, color='blue')
  plt.title(type)
  plt.grid(True)
  plt.scatter(pos[0], pos[1], color='red', s=100, label='Highlighted Points')

  plt.savefig("Images/graphs/temp_figs/temp_fig.png")

  graph_img = pygame.image.load('Images/graphs/temp_figs/temp_fig.png').convert_alpha()
  return graph_img

 graph_screen = pygame.display.set_mode((640, 480))
 icon = pygame.image.load('icon.png').convert_alpha()
 pygame.display.set_icon(icon)
 pygame.display.set_caption('Physlet: Graph')
   
 def update_line(base_x, base_y, t):
      pass
 
 def update_time(par, time_interval):
    global time 
    time = par 
    while True:
        time += 1
        time_module.sleep(time_interval) 
 
 global pos 
 if type_chosen == 'position':
    pos = get_x_pos 
 elif type_chosen == 'velocity':
    pos = get_x_vel
 elif type_chosen == 'acceleration':
    pos = get_x_acc

 with shelve.open('constants') as constants:
       dt = constants['dt']
 time_thread= Thread(target=update_time, args=(initial_time, dt,), daemon=True)
 time_thread.start()

 run = True
 while run:
      t = time 
      graph_screen.blit(display_graph([1,500, 500],pos(np.linspace(1, 500, 500)), [t, pos(t)], type=type_chosen), (0,0))

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
      pygame.display.update()
 pygame.quit()
