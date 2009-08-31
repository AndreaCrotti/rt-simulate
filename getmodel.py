#!/usr/bin/env python
import ConfigParser
import sys, getopt, logging

from schedu import *

DEFAULTCONF = "example.conf"
CONF_FILE = DEFAULTCONF
VERBOSE = False
GUI = False
CONF = None

logging.basicConfig(stream = sys.stdout)

def load_tasksets(config):
    "Load a configuration file into the right data structure"
    from string import strip
    c = ConfigParser.ConfigParser()
    c.read(config)
    whole = {}
    for s in c.sections():
        tset = []
        for j, v in c.items(s):
            vals = map(int, map(strip, v.split(',')))
            try:
                task = Task(j, *vals) # automatically handle the different possible input type with *
            except InputError:
                print "task %s is not correct" % (":".join([s, j]))
            else:
                tset.append(task)

        whole[s] = Scheduler(tset)
    return whole

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "dvhc:g", ["debug", "verbose", "help", "conf", "gui"])
    for o, a in opts:
        if o == "-v":
            # the verbosity should be handled with Logging
            # in this way also using the GUI is fine
            logging.setLevel(logging.INFO)
        if o == "-h":
            usage()
        if o == "-c":
            CONF_FILE = a
        if o == "-g":
            GUI = True

    # then finally start the engine, both frontends are working on the same
    # data and the same algorithms
    if GUI:
        from gui import run
    else:
        from cli import run
        
        l = load_tasksets(CONF_FILE)
        for k, v in l.items():
            print k, v

        run(l)
