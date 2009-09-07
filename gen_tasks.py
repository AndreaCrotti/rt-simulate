#!/usr/bin/env/python
import random
import math


from schedu import Scheduler, Task

def gen_harmonic(k, dim):
    """ Generate a n-dimension harmonic test, which must be schedulable and utilisation_bound = 1"""
    t = []
    for i in range(dim - 1):
        name = "t" + str(i)
        t.append(Task(name, 1, pow(2, i)))
    # fix here and use the right equation to find the rest (reaching 1)
    t.append(Task("t" + str(i), 1, pow(2, i)))

def gen_taskset(mincost = 1, maxcost = 10, minperiod = 1, maxperiod = 10):
    """ Generates a task set given the parameters """
    s = Scheduler()
    i = 0
    while True:
        cost = random.randrange(mincost, maxcost)
        period = random.randrange(cost, maxperiod) # careful to what is passed in input
        name = "t" + str(i)
        s.add_task(Task(name, cost, period))
        
        if s.utilisation_bound() > 1:
            s.remove(name)
    
    return s
