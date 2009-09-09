#!/usr/bin/env python
from getopt import getopt, GetoptError
from random import randrange
from sys import argv, exit

from rt_simulate import taskset_toini
from schedu import Scheduler, Task

MAXOFF = 5
DEF_RM = False
DEF_SCHED = True

def gen_taskset(mincost = 1, maxcost = 5, minperiod = 5, maxperiod = 15, density = 5,
                rate_monotonic = DEF_RM, schedulable = DEF_SCHED):
    """ Generates a task set given the parameters """
    s = Scheduler()
    i = 0
    while True:
        cost = randrange(mincost, maxcost)
        period = randrange(minperiod, maxperiod) # careful to what is passed in input

        if rate_monotonic:
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

def usage():
    print """usage: ./gen_tasks.py [-c conf-file] [-n]
    -c  conf-file:   writes to conf-file (default to test.conf)
    -n           :   creates a non schedulable task set
    -r           :   creates a rate monotonic task set
    -h           :   prints this help
    """
    exit(0)

if __name__ == '__main__':
    try:
        opts, args = getopt(argv[1:], "c:nhr")
    except GetoptError:
        usage()
        
    output = "test.conf"
    sched = DEF_SCHED
    rm = DEF_RM

    for o, a in opts:
        if o == "-h":
            usage()
        if o == "-c":
            output = a
        if o == "-n":
            sched = False
        if o == "-r":
            rm = True
    
    tset = gen_taskset(schedulable = sched, rate_monotonic = rm)
    print "taskset\n %s" % str(tset)
    print "writing taskset to %s" % output
    taskset_toini(tset, output)
