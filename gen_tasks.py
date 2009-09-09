#!/usr/bin/env python
from getopt import getopt
from random import randrange
from sys import argv

from rt_simulate import taskset_toini
from schedu import Scheduler, Task

MAXOFF = 5

def gen_taskset(mincost = 1, maxcost = 5, minperiod = 5, maxperiod = 15, density = 5,
                rm = False, schedulable = True):
    """ Generates a task set given the parameters """
    s = Scheduler()
    i = 0
    while True:
        cost = randrange(mincost, maxcost)
        period = randrange(minperiod, maxperiod) # careful to what is passed in input
        if rm:
            deadline = period
        else:
            deadline = period + randrange(MAXOFF)
        name = "t" + str(i)

        s.add_task(Task(name, cost, period, deadline))
        i += 1
        
        if s.utilisation_bound() > 1:
            if schedulable:
                s.remove_task(name) # otherwise it's for sure not schedulable
            break
    return s

if __name__ == '__main__':
    opts, args = getopt(argv[1:], "c:n:")
    output = "test.conf"
    sched = True

    for o, a in opts:
        if o == "c":
            output = a
        if o == "n":
            sched = False
    
    tset = gen_taskset(schedulable = sched, rm = False)
    print "taskset\n %s" % str(tset)
    print "writing taskset to %s" % output
    taskset_toini(tset, output)
