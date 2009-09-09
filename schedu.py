#!/usr/bin/env python
# TODO: write a better error handling (exceptions)
# TODO: analyze the wcet even on not schedulable tasks
import logging
from copy import deepcopy
from math import ceil
import csv

from errors import *

class Task(object):
    """ Task object """
    def __init__(self, name, cost, deadline, period = None):
        if (cost < 0) or (deadline < 0):
            pos = "must have positive values"
            logging.error(pos)
            raise InputError(pos)

        if not period:
            period = deadline

        elif period < deadline:
            great = "period must be greater or equal to deadline"
            logging.error(great)
            # in debug all the info
            logging.debug("error on object" + "\t,".join(map(str, [name, cost, deadline, period])))
            raise InputError(great)
        
        self.task = dict(name = name, cost = cost, deadline = deadline, period = period)
        self.task["wcet"] = cost
        self.remaining = cost # what left to do for the task
        show_attrs = ("cost", "deadline", "period")
        self.line = lambda sep: sep.join([str(self.task[x]) for x in show_attrs])
        self.runnable = True
            
    def __getitem__(self, x):
        return self.task[x]

    def __str__(self):
        n = self.task['name']
        rest = self.line(', ')
        rest += '\t wcet: %d' % self.task['wcet']
        return ': '.join((n, rest))

    def to_ini(self):
        return self.line(', ')

    def is_schedulable(self):
        return (self.task['wcet'] <= self.task['deadline'])

    def is_deadline(self, x):
        # here the formula is more complicated, we must make sure that:
        # (x - deadline) == k * period, where k can also be zero (to get the first deadline
        return (x != 0) and (((x - self.task['deadline']) % self.task['period']) == 0)

    def is_period(self, x):
        return (x != 0) and (x % self.task['period'] == 0)

    def is_done(self):
        return self.remaining <= 0

    def reset(self):
        self.remaining = self['cost']
        
class TimeLine(object):
    """ Class of the time line of events occurring in the hyperperiod """
    def __init__(self, length):
        self.length = length
        self.timeline = [dict(task = None, deadline = [], period = [], missed = []) 
                         for _ in range(length)]
        self.last = length
        # TODO: auto exporting to csv in the timeline abstraction
        self.header = ["INDEX", "TASK", "DEADLINES", "PERIODS", "MISSED DEADLINES"]

    def __str__(self):
        return '\n'.join([self.line(x) for x in range(self.last)])
    
    def __setitem__(self, idx, val):
        self.timeline[idx]["task"] = val

    def line(self, x):
        res = ': '.join([str(x), str(self.timeline[x]['task'])]) + '\t'
        if self.timeline[x]['deadline']:
            res += "deadlines: " + str(self.timeline[x]['deadline']) + "\t"
        if self.timeline[x]['period']:
            res += "periods end: " + str(self.timeline[x]['period']) + "\t"
        if self.timeline[x]['missed']:
            res += "deadline missed for tasks:" + str(self.timeline[x]['missed'])
        return res

    def set_missed(self, idx, task):
        self.timeline[idx]["missed"].append(task)

    def set_deadline(self, idx, task):
        " Setting the deadline for task"
        self.timeline[idx]["deadline"].append(task)

    def set_period(self, idx, task):
        " Setting the period end for the task task"
        self.timeline[idx]["period"].append(task)

    def time(self, task):
        t = deepcopy(task) # don't want to modify the original task
        for i in range(self.length):
            if t.is_done():
                return i

            if self.timeline[i] == t['name']:
                t['remaining'] -= 1

class Scheduler(object):
    """ Scheduler class, takes a list of tasks as input initially (which may also be empty)
    Every time a new task is added the hyperperiod and the scheduling are recalculated """
    
    def __init__(self, tasks = [], name = "taskset"):
        self.task_dict = dict( (t['name'], t) for t in tasks)
        self.tasks = lambda : self.task_dict.values()
        self.name = name
        self.setup()

    def __str__(self):
        " Task set is only a dict of tasks initially "
        t = '\n'.join([ str(t) for t in self.tasks() ])
        return t

    def __len__(self):
        return len(self.task_dict)

    def result(self):
        h = "HYPERPERIOD: %d" % self.hyper
        u = "TOTAL UTILISATION BOUND: " + str(round(self.utilisation_bound(), 3))
        a = "ALGORITHM CHOSEN: %s" % self.algo
        t = "TIMELINE:\n %s" % str(self.timeline)
        return '\n'.join([h, u, a, t]) + '\n\n'

    def setup(self):
        logging.info("setting up the task\n")
        self.hyper = self.hyper_period()
        self.timeline = TimeLine(self.hyper) # faster methods?
        self.sort_key = self.select_algorithm()
        self.worst_case_analysis()

    def hyper_period(self):
        """Computes the hyper_period"""
        periods = [ x["period"] for x in self.tasks() ]
        return lcm_list(periods)

    def select_algorithm(self):
        if any([t["deadline"] != t["period"] for t in self.tasks() ]):
            logging.info("selecting deadline monotonic")
            self.algo = "deadline monotonic"
            return "deadline" # using deadline monotonic
        else:
            logging.info("selecting rate monotonic")
            self.algo = "rate monotonic"
            return "period" # using rate monotonic
    
    def remove_task(self, task_name):
        # should be only one
        logging.info("removing task %s" % task_name)
        self.task_dict.pop(task_name)

    def add_task(self, task):
        name = task['name']
        if name in self.task_dict.keys():
            print "a task called %s is already present, not adding\n"
            return

        logging.info("adding task %s" % name)
        self.task_dict[name] = task
        self.setup() # Too much effort recalculating everything every time??

    def queue(self):
        """ Returning a sorted priority list of unfinished jobs """
        q = [ task for task in self.tasks() if (not (task.is_done())) and (task.runnable) ]
        q.sort(key = lambda t: t[self.sort_key]) # sorting here because the algorithm could change adding new tasks
        return q

    def next_task(self):
        q = self.queue()
        if len(q) >= 1:
            return q[0]
        else:
            return None

    def schedule(self):
        """Finally schedule the task set, at this point priorities must be set already"""
        cur_task = self.next_task()
        debmsg = "at step %d task %s is %s"
        for i in range(self.hyper):
            for t in self.tasks():
                # reset is done when the period expires
                # but we must check if done when deadline expires
                if t.is_deadline(i):
                    if not(t.is_done()):
                        self.timeline.set_missed(i, t['name'])
                        # we can stop calculating the timeline
                        logging.debug(debmsg % (i, t['name'], "not runnable"))
                        self.timeline.last = i + 1
                        return False
                    self.timeline.set_deadline(i, t['name'])
                    t.runnable = False
                    t.reset()

                if t.is_period(i):
                    self.timeline.set_period(i, t['name'])
                    # in the case period = deadline the variable runnable goes back to true
                    logging.debug(debmsg % (i, t['name'], "runnable"))
                    t.runnable = True
                    
            cur_task = self.next_task() # should not need every time
            if not(cur_task):
                continue # just go to the next position on the timeline

            logging.debug("next task to schedule is %s" % cur_task['name'])
            self.timeline[i] = cur_task['name']
            cur_task.remaining -= 1
        return True
    
    def real_wcet(self, task):
        """ Computes the real wcet of task, given the timeline (works
        also if not schedulable task set """
        return self.timeline.time(task)

    def utilisation_bound(self):
        return sum([float(x["cost"]) / x["period"] for x in self.tasks()])
    
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
        u_least = ulub(len(self))
        u_bound = self.utilisation_bound()
        
        logging.debug("ulub = %f, ubound = %f" % (u_least, u_bound))

        if u_bound > 1:
            logging.info("Task set with U > 1 is never schedulable")
            return False

        elif u_bound < u_least:
            logging.info("it's surely schedulable")
            return True
        
        return None # no information given
        
    def worst_case_check(self):
        for t in self.tasks():
            w, d = t["wcet"], t["deadline"]
            if w > d:
                logging.info("task %s is not schedulable" % str(t))
                return False
        return True

    def worst_case_analysis(self):
        """ Worst case analysis checks for every task if the
        worst case response time is less than the deadline and returns
        True only if all tests are passed """

        def wcrt(idx):
            """ Calculate the worst case response time of a particular task.
            If for any task wcrt(i) > di then the task set is surely not schedulable """

            r = [ sum([ t["cost"] for t in self.tasks() ])] # setting r_idx[0]
            while True:
                # ceil must take float numbers
                next_value = self.tasks()[idx]["cost"] +\
                             sum([int(ceil(float(r[-1]) / self.tasks()[h]["period"])) * self.tasks()[h]["cost"]\
                                  for h in range(idx) ])
                r.append(next_value)
                # Checking if passing the deadline or getting to a fix point
                if (r[-1] > self.tasks()[idx]["deadline"]) or (r[-1] == r[-2]):
                    return r[-1]

        for i in range(len(self.task_dict)):
            # we set the wcet for all the tasks, check will be elsewhere
            logging.info("setting wcet for %d" % i)
            self.tasks()[i].task["wcet"] = wcrt(i)

def create_task():
    getint = lambda x: input("insert %s\n" % x)
    while True:
        name = raw_input("name of the task\n")
        cost = getint("cost")
        deadline = getint("deadline")
        period = getint("period")
        
        try:
            t = Task(name, cost, deadline, period)
        except InputError:
            print "error task not added"
            continue
        else:
            return t

# TODO: use and abuse the automatic completion
def interactive():
    s = Scheduler()
    def new_task():
        t = create_task()
        s.add_task(t)
    
    def rem_task():
        i = raw_input("name of the task")
        s.remove_task(i)
    
    def sched():
        s.schedule()
        print s
        print s.result()

    # Check that lambda is suitable here in this situation
    actions = {
        "a" : [new_task, "add a new task"],
        "d" : [rem_task, "remove an existing task"], # must also modify timeline then
        "s" : [sched, "schedule the task set and show it"]
        }
    
    message = '\n'.join([':\t'.join([k, actions[k][1]]) for k in actions.keys()])

    while True:
        print message
        k = raw_input("what to do? (q to exit)\n")
        if k == 'q':
            return s

        if k in actions.keys():
            actions[k][0]()
        else:
            print "don't understand" # continue is implicit here

def lcm_list(nums):
    """Calculates the lcm given a list of integers"""
    if len(nums) == 0:
        return 0
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
