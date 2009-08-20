#!/usr/bin/env python
# scheduler, every task is a dictionary like (name, cost, deadline, period, priority)
# Implementing rate monotonic / dead line monotonic

import random
from math import pow

class Task(object):
    def __init__(self, name, cost, deadline, **other):
        self.task = dict(name = name, cost = cost, deadline = deadline)
        self.done = False
        self.running = False
        self.remaining = cost # what left to do
        
        if other.has_key("period"):
            # then period != deadline, do something else here
            per = other["period"]
            if per < deadline:
                raise Exception, "not possible"
            else:
                self.task["period"] = other["period"]
            
        if other.has_key("priority"):
            # then fixed priorities
            self.task["priority"] = other["priority"]
        else:
            self.task["priority"] = 0

    def __getitem__(self, x):
        return self.task[x]

    def __str__(self):
        return str(self.task)

class TaskSet(object):
    """Defines a new taskset, takes as input a list of dictionaries"""
    def __init__(self, tasks, dynamic = True):
        """When dynamic false means that the priorities are fixed already"""
        self.tasks = tasks

        self.dim = len(self.tasks)
        if not dynamic:
            # then we choose a static algorithm
            pass
        else:
            # choosing a dynamic algorithm 
            pass

    def __str__(self):
        return ""
    
    def schedule(self):
        """Finally schedule the task set, only possible when the priorities are set"""
        # Timeline is long as the hyperperiod, we go through it until we schedule everything
        # Timeline is just a list long as the hyperperiod initially set to 0 and then filled with tasks numbers
        hyper = self.hyper_period()
        timeline = [0 for x in range(hyper)]
        # a cycle where at every deadline we check again the priorities (preemption possible)
        
        ddlines = [x[1] for x in self.tasks]
        timers = set(())
        for d in ddlines:
            timers = timers.union(range(0, hyper + 1, d))
        # when having the timers it's almost done
        for idx in range(hyper):
            control = 0
        
    def hyper_period(self):
        """Computes the hyper_period"""
        periods = [x[2] for x in self.tasks]
        return lcm(periods)

    def ulub(self):
        """docstring for ulub"""
        return self.dim * (pow(self.dim, (1.0 / self.dim)) - 1)
        
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
