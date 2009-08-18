#!/usr/bin/env python
# scheduler, every task is a triple (ci, deadline, period)
# Implementing rate monotonic / dead line monotonic

import random
import math

class TaskSet(object):
    """Defines a new taskset, takes as input a list of triples"""
    def __init__(self, tasks, priorities = {}):
        self.tasks = tasks
        if not(self.checkSet()):
            # FIXME: give the exact error, maybe move to parser?
            print "wrong taskset, error in definition"
            return False

        self.dim = len(self.tasks)
        if priorities:
            # then we choose a static algorithm
            pass
        else:
            # choosing a dynamic algorithm 
            pass
    
    def checkSet(self):
        """checking that the taskset is sound"""
        # FIXME: very ugly sorted(list)...
        bools = [ sorted(list(x)) == list(x) for x in self.tasks ]
        return bools[0] == True and len(set(bools)) == 1

    def schedule(self):
        """Finally schedule the task set, only possible when the priorities are set"""
        # Timeline is long as the hyperperiod, we go through it until we schedule everything
        # Timeline is just a list long as the hyperperiod initially set to 0 and then filled with values
        
        
        

    def ulub(self):
        """docstring for ulub"""
        return self.dim * (math.pow(self.dim, (1.0 / self.dim)) - 1)
        
    def bigU(self):
        return sum([float(x[0]) / x[2] for x in self.tasks])
    
    def is_sched_rm(self):
        """test if the taskset can be schedulable,
        When ulub < bigU < 1 we can't return anything
        1: schedulable
        0: not schedulable
        -1: don't know"""
        uAvg = self.bigU()
        if uAvg > 1:
            return 0
        elif uAvg < self.ulub():
            return 1
        return (-1)
        
    def rate_monotonic(self):
        """Assigns priorities in rate monotonic, shorter period -> higher priority"""
        pass
    
    def deadline_monotonic(self):
        pass
    
    # Implementing the worst case execution analysis
    def worstCase(self):
        """Analyze the task set to check if schedulable or not"""
        # while True:
        pass
        
    def choose_algorithm(self):
        """Analyze the task set to decide which algorithms works better"""
        

    def major(self):
        """calculates the major cycle"""
        pass
            

# some useful functions
def lcm(nums):
    """Calculates the lcm given a list of integers"""
    if len(nums) == 1:
        return nums[0]
    else:
        snd = lcm(nums[1:])
        fst = nums[0]
        return ((fst * snd) / (gcd(fst, snd)))

def gcd(a, b):
    """gcd of two numbers"""
    if a < b:
        return gcd(b, a)
    elif a == b:
        return a
    else:
        if b == 0:
            return a
        else:
            return gcd(b, a % b)


def ulub(tasks):
    """returns the least upper bound"""
    m = [(float(c[0]) / c[2]) for c in tasks]
    return (sum(m))


def test_ulub(n):
    """test n tasks"""
    s = []  
    for i in range(n):
        s.append((random.randrange(5), random.randrange(1,10), random.randrange(1,10)))
    return s


tset = [(2,3,4), (3,5,7)]
prova =  TaskSet(tset)
