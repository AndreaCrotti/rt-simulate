#!/usr/bin/env python
from getopt import getopt
from random import randrange
from sys import argv

from rt_simulate import taskset_toini
from schedu import Scheduler, Task


def gen_taskset(mincost = 1, maxcost = 5, minperiod = 5, maxperiod = 15, schedulable = True):
    """ Generates a task set given the parameters """
    s = Scheduler()
    i = 0
    while True:
        cost = randrange(mincost, maxcost)
        period = randrange(minperiod, maxperiod) # careful to what is passed in input
        name = "t" + str(i)
        s.add_task(Task(name, cost, period))
        i += 1
        
        if s.utilisation_bound() > 1:
            if schedulable:
                s.remove_task(name) # otherwise it's for sure not schedulable
            break
    return s

if __name__ == '__main__':
    opts, args = getopt(argv[1:], "c:n:")
    output = "test.conf"
    name = "test"
    for o, a in opts:
        if o == "c":
            output = a
        if o == "n":
            name = a
    
    tset = gen_taskset()
    tset.name = name
    print "writing taskset to %s" % output
    taskset_toini(tset, output)
