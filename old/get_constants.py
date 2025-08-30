import shelve 
import pygame 
import pygame_textinput as pgtext 
import pygame.freetype
import app
import kinematics

def get_constants(screen):
 
 
 def gen_text(text, pos=(10, 10), color=(255, 255, 255), max_width=500):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.get_rect(test_line).width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    y = pos[1]
    for line in lines:
        font.render_to(screen, (pos[0], y), line, color)
        y += font.get_sized_height()
 
 pygame.freetype.init()

 font = pygame.freetype.Font("font/MedodicaRegular.otf",35)
 
 ffont = pygame.font.Font("font/MedodicaRegular.otf",35)

 first_txt = "Enter a function associated with the motion of your object...use (t) for time and (*), (**) for multiplication and exponentiation, respectively"
 second_txt = "Specify whether the function previously given describes the object's (position), (velocity), or (acceleration)"
 third_txt =  "Enter your desired timestep size (in seconds)"
 err1_txt = "Error encountered! Please try again. Make sure to use (t) and not (T) and (*) for multiplication... Ensure common functions completely encased objects as in (cos(t))"
 err2_txt = "Error encountered! Please ensure that you enter types in all lowercase as in (position), (velocity), or (acceleration)"
 err3_txt = "Error encountered! Please ensure that you enter a purely decimal or integer value e.g. (0.64)"



 input_text = pgtext.TextInputVisualizer(font_color=(255,255,255),cursor_color=(255,255,255), font_object=ffont)

 run = True
 get_func = True
 get_func_type = False 
 get_time_step = False 

 error_1 = False 
 error_2 = False
 error_3 = False 

 while run:
    screen.fill((0, 180, 250))
    events = pygame.event.get()


    if get_func == True:
        gen_text(first_txt)
        input_text.update(events)
        screen.blit(input_text.surface, (10, 200))
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print('hi')
                    func = input_text.value 
                    try:
                     kinematics.text_to_function(func, 'position')
                     print('hey')
                     with shelve.open('constants') as constants:
                      constants['input_f'] = func 
                     get_func = False
                     get_func_type = True 
                     input_text.value = ''
                    except:
                     print('oh')
                     get_func = False 
                     error_1 = True 
                     input_text.value = ''
                     print('no')
    elif get_func_type == True:
        gen_text(second_txt)
        input_text.update(events)
        screen.blit(input_text.surface, (10, 200))
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    func_type = input_text.value
                    if func_type in ['position', 'velocity', 'acceleration']:
                     with shelve.open('constants') as constants:
                          constants['f_type'] = func_type 
                     input_text.value = ''    
                     get_time_step = True 
                     get_func_type = False 
                    else:
                        error_2 = True 
                        get_func_type = False
                        input_text.value = ''
    elif get_time_step == True:
        gen_text(third_txt)
        input_text.update(events)
        screen.blit(input_text.surface, (10, 200))
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        time_step = float(input_text.value) 
                        with shelve.open('constants') as constants:
                          constants['dt'] = time_step 
                        run = False 
                    except:
                        error_3 = True 
                        get_time_step = False   
                        input_text.value = ''
    
    elif error_1 == True:
        gen_text(err1_txt)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and get_func == False:
                    get_func = True 
                    error_1 = False 

    elif error_2 == True:
       gen_text(err2_txt)
       for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and get_func == False:
                    get_func_type = True 
                    error_2 = False 

    elif error_3 == True:
       gen_text(err3_txt)
       for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and get_func == False:
                    get_time_step = True 
                    error_3 = False 

    for event in events:
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

 pygame.quit()

 with shelve.open('constants') as constants:
    constants['g'] = 9.81
    constants['grav'] = (6.67430 * 10**(-11))
    print('constants successfully initialized ')
    if constants['chosen_example'] == 1:
        app.app()
     
