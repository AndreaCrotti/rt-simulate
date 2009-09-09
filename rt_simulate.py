#!/usr/bin/env python
import ConfigParser
import sys, getopt, logging
from string import strip

from schedu import *

# TODO: adding colored output, see http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
# and also http://code.activestate.com/recipes/574451/

DEFAULTCONF = "example.conf"
CONF_FILE = DEFAULTCONF
VERBOSE = False
GUI = False

COLORS = {
    "purple" : '\033[95m',
    "blue" : '\033[94m',
    "green" : '\033[92m',
    "yellow" : '\033[93m',
    "red" : '\033[91m',
    "disable" : '\033[0m'
    }

# a very simple logger
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

def taskset_toini(tset, output):
    """ Return the ini conf from a given task set """
    c = ConfigParser.ConfigParser()
    s = "taskset"
    c.add_section(s)
    for t, v in tset.task_dict.items():
        c.set(s, t, v.to_ini())
    return c.write(open(output, 'w'))

def run(tasksets):
    for x in tasksets.items():
        analyze(x)

def analyze(taskset):
    name, tset = taskset
    print "\n\t ANALYZING %s \n%s" % (name, str(tset))
    if not(tset.is_schedulable()):
        print "THIS TASK SET IS NOT SCHEDULABLE\n"

    tset.schedule() # scheduling anyway
    print tset.result()
    if GUI:
        svg.write(tset)

def usage():
    print """usage : ./rt_simulate.py [-c conf-file] [-dvhgi]
-c    get the configuration file
-d    debug mode
-v    verbose mode
-h    print this help
-i    interactive mode
"""

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "dvhc:gi")

    for o, a in opts:
        if o == '-i':
            interactive()
        if o == "-v":
            logging.getLogger().setLevel(logging.INFO)
        if o == "-h":
            usage()
            sys.exit(0)
        if o == "-c":
            CONF_FILE = a
        if o == "-g":
            GUI = True
        if o == "-d":
            logging.getLogger().setLevel(logging.DEBUG)

    if GUI:
        import svg

    l = parse_tasksets(CONF_FILE)
    run(l)
