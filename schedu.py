#!/usr/bin/env python
# scheduler, every task is a triple (ci, deadline, period)
# Implementing rate monotonic / dead line monotonic

import random
import math

class TaskSet(object):
    """Defines a new taskset, takes as input a list of triples"""
    def __init__(self, tasks):
        if not(self.checkSet(tasks)):
            raise "taskset not correct"

        self.tasks = tasks
        self.dim = len(self.tasks)
        # creating a dictionary
        t = ["tau" + str(i) for i in range(self.dim)]
        self.task_dict = dict(zip(t, self.tasks))
        self.priorities = dict(zip(t, [0] * self.dim))
        self.dit = {}
        keys = ['ci', 'di', 'ti']
        # FIXME is that really needed??
        for el, values in t, self.tasks :
            self.dit[el] = {}
            for i in range(len(keys)):
                self.dit[el][keys[i]] = values[i]
        
    
    def checkSet(self, tasks):
        """checking that the taskset is sound"""
        # FIXME very ugly sorted(list)...
        bools = [ sorted(list(x)) == list(x) for x in tasks ]
        return bools[0] == True and len(set(bools)) == 1

    def ulub(self):
        """docstring for ulub"""
        return self.dim * (math.pow(self.dim, (1.0 / self.dim)) - 1)
        
    def bigU(self):
        return sum([float(x[0]) / x[2] for x in self.tasks])
    
    def is_schedulable(self):
        """test if the taskset can be schedulable,
        When ulub < bigU < 1 we can't return anything"""
        uAvg = self.bigU()
        if uAvg > 1:
            return False
        elif uAvg < self.ulub():
            return True
        
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
        
    def major(self):
        """calculates the major cycle"""
        
            

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
print prova.task_dict
print prova.priorities
