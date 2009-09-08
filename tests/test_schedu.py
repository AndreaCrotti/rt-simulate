#!/usr/bin/env python
# encoding: utf-8

# TODO: check how to test the init of every class and exceptions raising

import sys
import os
import unittest
from schedu import *
from errors import *

tests = {
    "rm" : [Task("t1", 2, 5), Task("t2", 2, 9), Task("t3", 5, 20)],
    "rm_easy" : [Task("t1", 1, 5), Task("t2", 3, 4)],
    "dm" : [Task("t1", 1, 4, 4), Task("t2", 4, 6, 15), Task("t3", 3, 6, 10)],

    # Here U = 1 but optimal for the rate monotonic algorithm
    "harmonic" : [Task("t1", 3, 6), Task("t2", 3, 12), Task("t3", 6, 24)]
    }

# TODO check how to test __init__(s)
class TestTask(unittest.TestCase):
    def setUp(self):
        pass

    def testCheck(self):
        self.assertRaises(InputError)

class TestScheduler(unittest.TestCase):
    def setUp(self):
        sched = {}
        for t, val in tests.items():
            sched[t] = Scheduler(val)

    def testUbound(self):
        for x in sched.items():
            pass

class TestTimeline(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()
