#!/usr/bin/env/python

import os, sys, getopt, logging
import ConfigParser

# usage() and the flags configuration must alwasys be well in sync
if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "vhc:")
    for o,a in opts:
        if o == "v":
            VERBOSE = True
        if o == "h":
            usage()
        if o == "c":
            load_conf(a)

