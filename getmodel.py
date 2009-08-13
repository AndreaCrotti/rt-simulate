#!/usr/bin/env/python

import os, sys, getopt, logging
import ConfigParser

VERBOSE = False
GUI = False
CONF = False

# we define the sections and a list of mandatory items for each one
conf_struct = {
    "alg" : ["default"],
    "jobs" : []
    }

def load_conf(config):
    "Load a configuration file into the right data structure"
    c = ConfigParser.ConfigParser()

# usage() and the flags configuration must alwasys be well in sync
if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "vhc:g")
    for o,a in opts:
        if o == "v":
            # the verbosity should be handled with Logging
            # in this way also using the GUI is fine
            VERBOSE = True
        if o == "h":
            usage()
        if o == "c":
            CONF = load_conf(a)
        if o == "g":
            GUI = True

    # then finally start the engine, both frontends are working on the same
    # data and the same algorithms
    if GUI:
        # for the GUI is not mandatory to have the jobs at the beginning
        from gui import main
        # initial configuration passed
        gui.main(CONF)
    else:
        from cli import main
        if not CONF:
            CONF = parse_conf(args)
        cli.main(CONF)
