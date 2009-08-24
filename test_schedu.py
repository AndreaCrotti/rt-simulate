#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
from schedu import *

class TestTask(unittest.TestCase):
    def setUp(self):
        t1 = Task("t1", 4, 10)
        t2 = Task("t2", 2, 20)

class TestScheduler(unittest.TestCase):
    def setUp(self):
        pass

class TestTimeline(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()
