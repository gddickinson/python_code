# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 09:51:29 2020

@author: g_dic
"""

## Functions are first-class objects
## functions can be passed around and used as arguments


def say_hello(name):
    return f"Hello {name}"

def be_awesome(name):
    return f"Yo {name}, together we are the awesomest!"

def greet_bob(greeter_func):
    return greeter_func("Bob")

## without parentheses only a reference to the function is passed
#print(greet_bob(say_hello))

## Inner functions
## inner functions have local scope - only availale within the parent() function

def parent():
    print("Printing from the parent() function")

    def first_child():
        print("Printing from the first_child() function")

    def second_child():
        print("Printing from the second_child() function")

    second_child()
    first_child()
    
#parent()

## Returning Functions From Functions
## Referneces to functions returned so that they can be called outside the local scope

def parent(num):
    def first_child():
        return "Hi, I am Emma"

    def second_child():
        return "Call me Liam"

    if num == 1:
        return first_child
    else:
        return second_child

first = parent(1)
second = parent(2)


#print(first())
#print(second())


## Simple Decorators
## decorators wrap a function, modifying its behavior

## Example 1
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

def say_whee():
    print("Whee!")

say_whee = my_decorator(say_whee)

#say_whee()

## Example 2
from datetime import datetime

def not_during_the_night(func):
    def wrapper():
        if 7 <= datetime.now().hour < 22:
            func()
        else:
            pass  # Hush, the neighbors are asleep
    return wrapper

def say_whee():
    print("Whee!")

say_whee = not_during_the_night(say_whee)

#say_whee()


## Using the @symbol
## Replaces the say_whee = my_decorator(say_whee) command to simplify syntax

def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_whee():
    print("Whee!")


## Decorating functions with arguments
def do_twice(func):
    def wrapper_do_twice():
        func()
        func()
    return wrapper_do_twice


@do_twice
def greet(name):
    print(f"Hello {name}")


#greet("World") #raises error as inner function wrapper_do_twice does not accept arguments

#Solution uses *args and **kwargs in inner wrapper to allow arbitary number of positional word arguments
def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice

@do_twice
def greet(name):
    print(f"Hello {name}")

#greet("World")


## returning values from decorated functions
##  make sure the wrapper function returns the return value of the decorated function
@do_twice
def return_greeting(name):
    print("Creating greeting")
    return f"Hi {name}"

@do_twice
def return_greeting(name):
    print("Creating greeting")
    return f"Hi {name}"


#hi_adam = return_greeting("Adam")
#print(hi_adam) #error - decorator ate the return value

## solution - add *args and *kwargs to return value
def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice

@do_twice
def return_greeting(name):
    print("Creating greeting")
    return f"Hi {name}"


#hi_adam = return_greeting("Adam")
#print(hi_adam) #error - decorator ate the return value

# For better wrapping use the @functools.wraps decorator to preserve information about the original function

import functools

def do_twice(func):
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice


@do_twice
def say_something(text):
    print(text)

#say_something('Hello')


## More examples
## Boilerplate example
import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper_decorator

## created new file decorators storing examples
from decorators import timer, debug

@timer
def waste_some_time(num_times):
    for _ in range(num_times):
        sum([i**2 for i in range(10000)])
        


#waste_some_time(1)
#waste_some_time(999)


@debug
def make_greeting(name, age=None):
    if age is None:
        return f"Howdy {name}!"
    else:
        return f"Whoa {name}! {age} already, you are growing up!"

#make_greeting("Benjamin")
#make_greeting(name="Dorrisile", age=116)


## Apply a decorator to a standard library function
import math
math.factorial = debug(math.factorial)

def approximate_e(terms=18):
    return sum(1 / math.factorial(n) for n in range(terms))

#print(approximate_e(5))


## Registering plugins
## Decorators don’t have to wrap the function they’re decorating. They can also simply register that a function exists and return it unwrapped

import random
PLUGINS = dict()

def register(func):
    """Register a function as a plug-in"""
    PLUGINS[func.__name__] = func
    return func

@register
def say_hello(name):
    return f"Hello {name}"

@register
def be_awesome(name):
    return f"Yo {name}, together we are the awesomest!"

def randomly_greet(name):
    greeter, greeter_func = random.choice(list(PLUGINS.items()))
    print(f"Using {greeter!r}")
    return greeter_func(name)


#print(PLUGINS)
#print(randomly_greet('Bob'))


class Counter:
    def __init__(self, start=0):
        self.count = start

    def __call__(self):
        self.count += 1
        print(f"Current count is {self.count}")


#counter = Counter()
#counter()
#counter()


import functools

class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__!r}")
        return self.func(*args, **kwargs)

@CountCalls
def say_whee():
    print("Whee!")





