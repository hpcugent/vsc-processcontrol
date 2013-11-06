# -*- encoding: utf-8 -*-
import sys
import os
import test.processcontrol as p
import unittest

suite = unittest.TestSuite([p.suite()])

try:
    import xmlrunner
    rs = xmlrunner.XMLTestRunner(output="test-reports").run(suite)
except ImportError, err:
    rs = unittest.TextTestRunner().run(suite)

if not rs.wasSuccessful():
    sys.exit(1)
