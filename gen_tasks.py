#!/usr/bin/env/python
import random
import math

def gen_harmonic(k, dim):
    """ Generate a n-dimension harmonic test, which must be schedulable and utilisation_bound = 1"""
    t = []
    for i in range(dim - 1):
        name = "t" + str(i)
        t.append(Task(name, 1, pow(2, i)))
    # fix here and use the right equation to find the rest (reaching 1)
    t.append(Task("t" + str(i), 1, pow(2, i)))

def gen_taskset(mincost = 1, maxcost = 10, minperiod = 1,
                minU = 0.5, maxU = 1.0):
    """ Generates a task set given the parameters """
    # U is the shifted random number in my other window
    u = maxU/2 + minU

