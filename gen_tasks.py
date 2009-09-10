#!/usr/bin/env python
from getopt import getopt, GetoptError
from random import randrange
from sys import argv, exit
from math import ceil

from rt_simulate import taskset_toini
from schedu import Scheduler, Task

def gen_taskset(density, rate_monotonic, schedulable, harmonic):
    """ Generates a task set given the parameters """
    s = Scheduler()
    i = 0
    if harmonic:
        rate_monotonic = True
        base = randrange(5)

    while True:
        if harmonic:
            period = base * randrange(10)
        else:
            period = randrange(10, 20)

        cost = int(ceil(float(period) / density))

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
    print """usage: ./gen_tasks.py [-c conf-file] [-n] [-r] [-d (1..10]
    -c  conf-file:   writes to conf-file (default to test.conf)
    -n           :   creates a non schedulable task set
    -r           :   creates a rate monotonic task set
    -d           :   desired tasks number, 1=max tasks, 10= min tasks
    -h           :   prints this help
    """
    exit(0)

if __name__ == '__main__':
    try:
        opts, args = getopt(argv[1:], "c:nhrd:m")
    except GetoptError:
        usage()
        
    output = "test.conf"
    sched = True
    rm = False
    dens = 5
    harm = False

    for o, a in opts:
        if o == '-h':
            usage()
        if o == '-c':
            output = a
        if o == '-n':
            sched = False
        if o == '-r':
            rm = True
        if o == '-m':
            harm = True
        if o == '-d':
            dens = int(a)
    
    tset = gen_taskset(dens, sched, rm, harm)
    print "taskset\n %s" % str(tset)
    print "writing taskset to %s" % output
    taskset_toini(tset, output)
