#!/usr/bin/env python

# generators for C and spin code

import sys, os, subprocess

def check_exec(executable):
    """Checking if the executable is in the path
    and return the full path"""
    paths = os.getenv('PATH').split(':')
    for p in paths:
        if executable in os.listdir(p):
            return os.path.join(p, executable)
    return False

def gen_c(rt_structure):
    """Generating C code equivalent"""
    pass

def gen_spin(rt_structure):
    """
    
    Arguments:
    - `rt_structure`:
    """
    pass

