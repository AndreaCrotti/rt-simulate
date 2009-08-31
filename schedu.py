#!/usr/bin/env python
# TODO: write the logging mechanism
# TODO: write a better error handling (exceptions)

import random
import logging
from math import pow, floor

from errors import *

class Task(object):
    """ This class define a taks"""
    def __init__(self, name, cost, deadline, period = None):
        if not period:
            period = deadline
        self.check()

        self.task = dict(name = name, cost = cost, deadline = deadline, period = period)
        self.remaining = cost # what left to do for the task
        # two inline functions useful later:
        self.done = lambda : self.remaining <= 0
        self.is_deadline = lambda x: x % self.task["deadline"] == 0
            
    def __getitem__(self, x):
        return self.task[x]

    def __str__(self):
        return str(self.task) + "\tremaining: " + str(self.remaining)

    def check(self, period, deadline):
        if period < deadline:
            raise InputError("period must be greater or equal to deadline")
        
    def reset(self):
        self.remaining = self["cost"]

class TimeLine(object):
    """Representing the time line of events occurring in the hyperperiod """

    def __init__(self, length):
        self.length = length
        self.timeline = [None for x in range(length)]
        
    def __str__(self):
        return ' '.join(map(str, enumerate(self.timeline)))
    
    def __setitem__(self, idx, val):
        self.timeline[idx] = val

class Scheduler(object):
    def __init__(self, tasks):
        self.tasks = tasks
        self.setup()

    def __str__(self):
        return '\n'.join([ str(t) for t in self.tasks ])
    
    def setup(self):
        self.hyper = self.hyper_period()
        self.timeline = TimeLine(self.hyper) # faster methods?
        self.sort_key = self.select_algorithm()

    def hyper_period(self):
        """Computes the hyper_period"""
        periods = [x["period"] for x in self.tasks]
        return list_lcm(periods)

    def select_algorithm(self):
        if any([t["deadline"] != t["period"] for t in self.tasks]):
            return "deadline" # using deadline monotonic
        else:
            return "period" # using rate monotonic
    
    def add_task(self, task):
        self.tasks.append(task)
        self.setup() # Too much effort recalculating everything every time??

    def queue(self):
        """ Returning a sorted priority list of unfinished jobs """
        q = [ task for task in self.tasks if not (task.done())]
        q.sort(key = lambda t: t[self.sort_key]) # sorting here because the algorithm could change adding new tasks
        return q

    def get_next(self):
        q = self.queue()
        if len(q) >= 1:
            return q[0]
        else:
            return None

    def schedule(self):
        """Finally schedule the task set, only possible when the priorities are set"""
        # Timeline must is long as the hyperperiod, we go through it until we schedule everything
        # Timeline is just a list long as the hyperperiod initially set to 0 and then filled with tasks numbers
        # a cycle where at every deadline we check again the priorities (preemption possible)

        # at time 0 all tasks starting
        if not(self.is_schedulable()):
            print "impossible to schedule"
            return
        
        cur_task = self.get_next()
        
        for i in range(self.hyper):
            # get a new task only when one deadline is found
            recalc = False
            for t in self.tasks:
                if t.is_deadline(i):
                    if not(t.done()):
                        print "error error task %s is not finished before deadline" % t["name"]
                    t.reset()
            
            cur_task = self.get_next() # should not need every time
            if not(cur_task):
                continue # just go to the next position on the timeline

            self.timeline[i] = cur_task["name"]
            cur_task.remaining -= 1
        print self.timeline

    def ulub(self):
        """docstring for ulub"""
        dim = len(self.tasks)
        return dim * (pow(dim, (1.0 / dim)) - 1)
        
    def bigU(self):
        return sum([float(x["cost"]) / x["period"] for x in self.tasks])
    
    def is_schedulable(self):
        if self.sort_key == "period":
            
            s = self.is_sched_rm()
            if s == None:
                return self.worst_case_analysis()
            else:
                return s
        else:
            return self.worst_case_analysis()
            # deadline monotonic case

    def is_sched_rm(self):
        """test if the taskset can be schedulable,
        When ulub < bigU < 1 we can't return anything
        True: schedulable
        False: not schedulable
        None: don't know"""
        uAvg = self.bigU()
        if uAvg > 1:
            return False
        elif uAvg < self.ulub():
            return True
        return None
        
    # Analysis with the worst time response case, an iterative way to see if a task set is really schedulable
    def worst_case_analysis(self):
        def wcrt(idx):
            """ Calculate the worst case response time of a particular task.
            If for any task wcrt(i) > di then the task set is surely not schedulable """
            cost = self.tasks[idx]["cost"]

            r = [ self.tasks[x]["cost"] for x in range(idx+1) ] # setting r_idx[0]
            while True:
                next_value = cost +\
                             sum([int(floor(r[-1] / self.tasks[h]["deadline"])) for h in range(idx) ])
                r.append(next_value)
                if r[-1] == r[-2]: # Insert check of list length
                    return sum(r[:-1])

        for i in range(len(self.tasks)):
            w = wcrt(i)
            if w > self.tasks[i]["deadline"]:
                print "task %s not schedulable" % self.tasks[i]["name"]
                return False
            print "task %s has wcrt = %d" % (self.tasks[i]["name"], w)
        return True

def list_lcm(nums):
    """Calculates the lcm given a list of integers"""
    if len(nums) == 1:
        return nums[0]
    else:
        snd = list_lcm(nums[1:])
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

def gen_tasks(n):
    """Generate n tasks"""
    s = [ Task(str(i), random.randrange(5), random.randrange(1, 10)) for i in range(n) ]
    return Scheduler(s)


tasks_rm = [Task("t1", 2, 5), Task("t2", 2, 9), Task("t3", 5, 20)]
test_rm = Scheduler(tasks_rm)
test_rm.schedule()

tasks_dm = [Task("t1", 1, 4, 4), Task("t2", 4, 6, 15), Task("t3", 3, 6, 10)]
test_dm = Scheduler(tasks_dm)
test_dm.schedule()
