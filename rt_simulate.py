#!/usr/bin/env python
import ConfigParser
import sys, getopt, logging
from string import strip

from schedu import *

DEFAULTCONF = "example.conf"
CONF_FILE = DEFAULTCONF
VERBOSE = False
GUI = False
CONF = None

logging.basicConfig(stream = sys.stdout)

def parse_tasksets(config):
    "Load a configuration file into the right data structure"
    c = ConfigParser.ConfigParser()
    c.read(config)
    whole = {}
    for s in c.sections():
        tset = Scheduler()
        for j, v in c.items(s):
            vals = map(int, map(strip, v.split(',')))
            try:
                task = Task(j, *vals) # automatically handle the different possible input type with *
            except InputError:
                logging.info("task %s is not correct" % (":".join([s, j])))
            else:
                tset.add_task(task)
        whole[s] = tset
    return whole

def taskset_toini(tset):
    """ Return the ini conf from a given task set """
    c = ConfigParser.ConfigParser()
    s = "taskset"
    c.add_section(s)
    for t, v in tset.task_dict.items():
        c.set(s, t, v.to_ini())
    return c

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "dvhc:g", ["debug", "verbose", "help", "conf", "gui"])

    for o, a in opts:
        if o == "-v":
            logging.getLogger().setLevel(logging.INFO)
        if o == "-h":
            usage()
        if o == "-c":
            CONF_FILE = a
        if o == "-g":
            GUI = True
        if o == "-d":
            logging.getLogger().setLevel(logging.DEBUG)

    # then finally start the engine, both frontends are working on the same
    # data and the same algorithms
    from cli import run
        
    l = parse_tasksets(CONF_FILE)
    run(l)
