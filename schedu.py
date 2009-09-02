#!/usr/bin/env python
# TODO: write the logging mechanism
# TODO: write a better error handling (exceptions)

import random
import logging
import sys
from math import pow, ceil

from errors import *

class Task(object):
    """ This class define a taks"""
    def __init__(self, name, cost, deadline, period = None):
        if not period:
            period = deadline

        elif period < deadline:
            err = "period must be greater or equal to deadline"
            logging.error(err)
            # in debug all the info
            logging.debug("error on object" + "\t,".join(map(str, [name, cost, deadline, period])))
            raise InputError(err)
        
        self.task = dict(name = name, cost = cost, deadline = deadline, period = period)
        self.task["wcet"] = cost
        self.remaining = cost # what left to do for the task
            
    def __getitem__(self, x):
        return self.task[x]

    def __str__(self):
        n = self.task["name"]
        rest = ", ".join([str(self.task[x]) for x in ("cost", "deadline", "period")])
        rest += "\t wcet: %d" % self.task["wcet"]
        return ": ".join((n,rest))
        
    def is_schedulable(self):
        return (self.task["wcet"] <= self.task["deadline"])

    def is_deadline(self, x):
        return (x != 0) and (x % self.task["deadline"] == 0)

    def is_done(self):
        return self.remaining <= 0

    def reset(self):
        self.remaining = self["cost"]

class TimeLine(object):
    """Representing the time line of events occurring in the hyperperiod """

    def __init__(self, length):
        self.length = length
        self.timeline = [None for x in range(length)]
        
    def __str__(self):
        return ', '.join(map(str, self.timeline))
    
    def __setitem__(self, idx, val):
        self.timeline[idx] = val

class Scheduler(object):
    """ Scheduler class, takes a list of tasks as input initially (which may also be empty)
    Every time a new task is added the hyperperiod and the scheduling are recalculated """
    
    def __init__(self, tasks):
        self.tasks = tasks
        self.setup()

    def __str__(self):
        return '\n'.join([ str(t) for t in self.tasks ])
    
    def setup(self):
        logging.info("setting up the task\n")
        self.hyper = self.hyper_period()
        self.timeline = TimeLine(self.hyper) # faster methods?
        self.sort_key = self.select_algorithm()
        self.worst_case_analysis()

    def hyper_period(self):
        """Computes the hyper_period"""
        periods = [ x["period"] for x in self.tasks ]
        return lcm_list(periods)

    def select_algorithm(self):
        if any([t["deadline"] != t["period"] for t in self.tasks]):
            logging.info("selecting deadline monotonic")
            return "deadline" # using deadline monotonic
        else:
            logging.info("selecting rate monotonic")
            return "period" # using rate monotonic
    
    def add_task(self, task):
        self.tasks.append(task)
        self.setup() # Too much effort recalculating everything every time??

    # TOO MANY SIDE EFFECTS, rewrite more functionally (erlang maybe?)
    def queue(self):
        """ Returning a sorted priority list of unfinished jobs """
        q = [ task for task in self.tasks if not (task.is_done()) ]
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
        
        cur_task = self.get_next()
        
        for i in range(self.hyper):
            # get a new task only when one deadline is found
            recalc = False
            for t in self.tasks:
                if t.is_deadline(i):
                    # --------------------------------------------------------------------------------------
                    # this check should not be really necessary, if the analysis is correct it never happens
                    # --------------------------------------------------------------------------------------
                    if not(t.is_done()):
                        err = "at time %d error error task %s is not finished before deadline\n" % (i, t["name"]) +\
                              "temp timeline is = %s" % str(self.timeline)
                        logging.error(err)
                        return False
                    t.reset()
            
            cur_task = self.get_next() # should not need every time
            if not(cur_task):
                continue # just go to the next position on the timeline

            self.timeline[i] = cur_task["name"]
            cur_task.remaining -= 1
        return True

    def utilisation_bound(self):
        return sum([float(x["cost"]) / x["period"] for x in self.tasks])
    
    def is_schedulable(self):
        if self.sort_key == "period":
            rm_sched = self.is_sched_rm()
            if rm_sched == None:
                logging.info("necessary to analyze the worst case response")
                return self.worst_case_check()
            else:
                return rm_sched
        else:
            # in the deadline monotonic we only use the wcrt
            return self.worst_case_check()

    def is_sched_rm(self):
        """test if the taskset can be schedulable,
        When ulub < utilisation_bound < 1 we can't return anything
        True: schedulable
        False: not schedulable
        None: don't know"""
        
        u_least = ulub(len(self.tasks))
        u_bound = self.utilisation_bound()
        
        logging.debug("ulub = %f, ubound = %f" % (u_least, u_bound))

        if u_bound > 1:
            logging.info("Task set with U > 1 is never schedulable")
            return False

        elif u_least < ulub(len(self.tasks)):
            logging.info("it's surely schedulable")
            return True
        
        return None 
        
    def worst_case_check(self):
        for t in self.tasks:
            w, d = t["wcet"], t["deadline"]
            if w > d:
                logging.info("task %s is not schedulable" % str(t))
                return False
        return True

    def worst_case_analysis(self):
        """ Worst case analysis checks for every task if the
        worst case response time is less than the deadline and returns
        True only if all tests are passed """
        
        # FIXME: check how would be possible an infinite loop with always growing values
        def wcrt(idx):
            """ Calculate the worst case response time of a particular task.
            If for any task wcrt(i) > di then the task set is surely not schedulable """

            r = [ sum([ self.tasks[x]["cost"] for x in range(idx + 1) ])] # setting r_idx[0]
            while True:
                # ceil must take float numbers
                next_value = self.tasks[idx]["cost"] +\
                             sum([int(ceil(float(r[-1]) / self.tasks[h]["deadline"])) * self.tasks[h]["cost"]\
                                  for h in range(idx) ])
                r.append(next_value)
                if r[-1] == r[-2]: # We are safe that we already have two values
                    return r[-1]

        for i in range(len(self.tasks)):
            # we set the wcet for all the tasks, check will be elsewhere
            logging.info("setting wcet for %d" % i)
            self.tasks[i].task["wcet"] = wcrt(i)

def lcm_list(nums):
    """Calculates the lcm given a list of integers"""
    if len(nums) == 1:
        return nums[0]
    else:
        snd = lcm_list(nums[1:])
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

def ulub(dim):
    """ Least upper bound, only depending on the length"""
    return dim * (pow(2, (1.0 / dim)) - 1)

def gen_harmonic(k, dim):
    """ Generate a n-dimension harmonic test, which must be schedulable and utilisation_bound = 1"""
    t = []
    for i in range(dim - 1):
        name = "t" + str(i)
        t.append(Task(name, 1, pow(2, i)))
    # fix here and use the right equation to find the rest (reaching 1)
    t.append(Task("t" + str(i), 1, pow(2, i)))
