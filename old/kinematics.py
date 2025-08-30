from sympy import symbols, diff, integrate, sin, cos, exp, ln, lambdify
import numpy as np
import shelve 



def text_to_function(text, type):
   t = symbols('t')
   func = eval(text)
   if type == 'position':
      pos_func = func
      vel_func = diff(pos_func, t)
      acc_func = diff(vel_func, t)
   elif type == 'velocity':
      pos_func = integrate(func, t)
      vel_func = func 
      acc_func = diff(vel_func, t)
   elif type == 'acceleration':
      acc_func = func
      vel_func = integrate(acc_func, t)
      pos_func = integrate(vel_func, t)
   else:
      raise ValueError("The Type of the given function must be specified to be an acceleration, velocity, or position")   
   kine = [pos_func, vel_func, acc_func]
   return kine 


def get_x_pos(val):
   try:
    with shelve.open('constants') as constants:
     text = constants['input_f']
     type = constants['f_type']
   except:
     raise ValueError("Was unable to fetch the necessary constants.")
   t = symbols('t')
   f = lambdify(t, text_to_function(text=text, type=type)[0], modules = ['numpy'])
   return f(val)
def get_x_vel(val):
   try:
    with shelve.open('constants') as constants:
     text = constants['input_f']
     type = constants['f_type']
   except:
     raise ValueError("Was unable to fetch the necessary constants.")
   t = symbols('t')
   f = lambdify(t, text_to_function(text=text, type=type)[1], modules = ['numpy'])
   return f(val)
def get_x_acc(val):
   try:
    with shelve.open('constants') as constants:
     text = constants['input_f']
     type = constants['f_type']
   except:
     raise ValueError("Was unable to fetch the necessary constants.")
   t = symbols('t')
   f = lambdify(t, text_to_function(text=text, type=type)[2], modules = ['numpy'])
   return f(val)

