#!/usr/bin/env python
"""
Created on Fri Jan  1 18:04:49 2016

@author: george
"""
from math import *

hidden_value = "this is secret"

def dangerous_function(filename):
	print open(filename).read()

#make a list of safe functions
safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 
'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']
#use the list to filter the local namespace
safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ])
#add any needed builtins back in.
safe_dict['abs'] = abs

user_func = raw_input("type a function: y = ")

for x in range(1,10):
	# add x in
	safe_dict['x']=x
	print "x = ", x , ", y = ", eval(user_func,{"__builtins__":None},safe_dict)