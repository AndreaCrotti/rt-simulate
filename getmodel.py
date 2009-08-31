#!/usr/bin/env python

import os, sys, getopt, logging
import ConfigParser

from schedu import *

DEFAULTCONF = "example.conf"
CONF_FILE = DEFAULTCONF
VERBOSE = False
GUI = False
CONF = None

logging.basicConfig(stream = sys.stdout)

def load_conf(config):
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
                print "task is not correct"
                break
            else:
                tset.append(task)

        whole[s] = Scheduler(tset)
    return whole

def parse_conf(args):
    pass

# usage() and the flags configuration must alwasys be well in sync
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
        # for the GUI is not mandatory to have the jobs at the beginning
        from gui import run
        # initial configuration passed
    else:
        from cli import run
        
        l = load_conf(CONF_FILE)
        for k, v in l.items():
            print k, v
