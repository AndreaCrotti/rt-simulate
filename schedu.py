#!/usr/bin/env python
# scheduler, every task is a dictionary like (name, cost, deadline, period, priority)
# Implementing rate monotonic / dead line monotonic

# TODO: 

import random
from math import pow

class Task(object):
    """ This class define a taks"""
    def __init__(self, name, cost, deadline, **other):
        self.task = dict(name = name, cost = cost, deadline = deadline)
        self.running = False
        self.remaining = cost # what left to do for the task
        self.done = lambda : self.remaining <= 0
        self.is_deadline = lambda x: x % self.task["deadline"] == 0
        
        if other.has_key("period"):
            # then period != deadline, do something else here
            per = other["period"]
            if per < deadline:
                raise Exception, "not possible"
            else:
                self.task["period"] = other["period"]
        else:
            self.task["period"] = self.task["deadline"]
            
        if other.has_key("priority"):
            # then fixed priorities
            self.task["priority"] = other["priority"]
        else:
            self.task["priority"] = 0

    def __getitem__(self, x):
        return self.task[x]

    def __str__(self):
        return str(self.task) + "\tremaining: " + str(self.remaining)

    def __cmp__(self, y):
        """ Reversing here the order"""
        return (- cmp(self.task['priority'], y.task['priority']))

    def reset(self):
        self.remaining = self["cost"]

class TimeLine(object):
    """Representing the time line of events occurring in the hyperperiod """

    def __init__(self, length):
        self.length = length
        self.timeline = [None for x in range(length)]
        
    def __str__(self):
        return str(self.timeline)

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
        return lcm(periods)

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
        return self.queue()[0]

    def schedule(self):
        """Finally schedule the task set, only possible when the priorities are set"""
        # Timeline is long as the hyperperiod, we go through it until we schedule everything
        # Timeline is just a list long as the hyperperiod initially set to 0 and then filled with tasks numbers
        # a cycle where at every deadline we check again the priorities (preemption possible)

        # at time 0 all tasks starting
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

            self.timeline[i] = cur_task["name"]
            cur_task.remaining -= 1
        print self.timeline

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
        
    # Analysis with the worst time response case, an iterative way to see if a task set is really schedulable
    def worst_case_analysis(self):
        def wcrt(idx):
            """ Calculate the worst case response time of a particular task.
            If for any task wcrt(i) > di then the task set is surely not schedulable """
            from math import floor

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
                print "task %d not schedulable" % idx
            print "task %d has wcrt = %d" % (i, w)
            

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


def gen_tasks(n):
    """test n tasks"""
    s = [ Task(str(i), random.randrange(5), random.randrange(1, 10)) for i in range(n) ]
    return Scheduler(s)


t1 = Task("uno", 2, 4, priority = 2)
t2 = Task("due", 3, 5, priority = 4)
prova =  Scheduler([t1, t2])

tasks = [Task("t1", 2, 5), Task("t2", 2, 9), Task("t3", 5, 20)]
test_wc = Scheduler(tasks)
