#!/usr/bin/env python

import os, sys, getopt, logging
import ConfigParser

VERBOSE = False
GUI = False
CONF = None

def load_conf(config):
    "Load a configuration file into the right data structure"
    from string import strip
    conf = {}
    c = ConfigParser.ConfigParser()
    c.read(config)
    conf["alg"] = c.get("alg", "default")
    conf["jobs"] = []
    for j, vals in c.items("jobs"):
        conf["jobs"].append(map(strip, vals.split(',')))
    return conf

def parse_conf(args):
    pass

# usage() and the flags configuration must alwasys be well in sync
if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "vhc:g")
    for o, a in opts:
        if o == "-v":
            # the verbosity should be handled with Logging
            # in this way also using the GUI is fine
            VERBOSE = True
        if o == "-h":
            usage()
        if o == "-c":
            CONF = load_conf(a)
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
        if not CONF:
            CONF = parse_conf(args)

    print CONF
    run(CONF)
