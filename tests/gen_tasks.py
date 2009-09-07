#!/usr/bin/env/python
import random
import math

from schedu import Scheduler, Task

def gen_taskset(mincost = 1, maxcost = 5, minperiod = 5, maxperiod = 15, schedulable = True):
    """ Generates a task set given the parameters """
    s = Scheduler()
    i = 0
    while True:
        cost = random.randrange(mincost, maxcost)
        period = random.randrange(minperiod, maxperiod) # careful to what is passed in input
        name = "t" + str(i)
        s.add_task(Task(name, cost, period))
        i += 1
        
        if s.utilisation_bound() > 1:
            if schedulable:
                s.remove_task(name) # otherwise it's for sure not schedulable
            break
    return s

print gen_taskset()
