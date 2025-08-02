import shelve 
import pygame 
import pygame_textinput as pgtext 
import app
import os
import sys 

def get_constants():
 pygame.init()

 SCREEN_HEIGHT = 500
 SCREEN_WIDTH = 800

 screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
 icon = pygame.image.load('icon.png').convert_alpha()
 pygame.display.set_icon(icon)
 pygame.display.set_caption('Physlet: Kinematics Initialization')

 first_text_img = pygame.image.load('Images/text/get_kinematics_1.png').convert_alpha()
 second_text_img = pygame.image.load('Images/text/get_kinematics_2.png').convert_alpha()
 third_text_img = pygame.image.load('Images/text/get_kinematics_3.png').convert_alpha()

 input_text = pgtext.TextInputVisualizer()

 run = True
 get_func = True
 get_func_type = False 
 get_time_step = False 

 while run:
    screen.fill((0, 180, 250))
    
    events = pygame.event.get()

    if get_func == True:
        screen.blit(first_text_img, (0, 0))
        input_text.update(events)
        screen.blit(input_text.surface, (10, 200)) 
    
    if get_func_type == True:
        screen.blit(second_text_img, (0, 0))
        input_text.update(events)
        screen.blit(input_text.surface, (10, 200))

    if get_time_step == True:
        screen.blit(third_text_img, (0, 0))
        input_text.update(events)
        screen.blit(input_text.surface, (10, 200))

    for event in events:
        if event.type == pygame.QUIT:
            run = False 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and get_func == True:
                func = input_text.value 
                with shelve.open('constants') as constants:
                    constants['input_f'] = func 
                get_func = False
                get_func_type = True 
                input_text.value = ''

            elif event.key == pygame.K_RETURN and get_func_type == True:
                func_type = input_text.value 
                with shelve.open('constants') as constants:
                    constants['f_type'] = func_type 
                input_text.value = ''    
                get_time_step = True 
                get_func_type = False 
            
            elif event.key == pygame.K_RETURN and get_time_step == True:
                time_step = float(input_text.value) 
                with shelve.open('constants') as constants:
                    constants['dt'] = time_step 
                run = False 
                pass 
    pygame.display.update()

 pygame.quit()

 with shelve.open('constants') as constants:
    constants['g'] = 9.81
    constants['grav'] = (6.67430 * 10**(-11))
    print('constants successfully initialized ')
    if constants['chosen_example'] == 1:
        app.app()
        #script_path = os.path.abspath("app.py")
        #subprocess.run([sys.executable, script_path])

