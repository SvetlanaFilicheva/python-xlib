#!/usr/bin/env python

from __future__ import print_function
import sys
import os
import unittest
import struct

testfolder = os.path.abspath(os.path.dirname(__file__))
package_root = os.path.abspath(os.path.join(testfolder, ".."))
sys.path.append(package_root)

from Xlib.protocol import request, rq, event
import Xlib.protocol.event

def is_big_endian():
    "Check endianess (return True on big-endian system)"
    return struct.unpack('BB', struct.pack('H', 0x0100))[0] != 0


def run_tests():
    "Run all suitable tests"

    if is_big_endian():
        excludes = ['test_events_le', 'test_requests_le', ]
    else:
        excludes = ['test_events_be', 'test_requests_be', ]

    suite = unittest.TestSuite()

    sys.path.append(testfolder)

    for root, dirs, files in os.walk(testfolder):
        test_modules = [
            file.replace('.py', '') for file in files if
                file.startswith('test_') and
                file.endswith('.py')]

        test_modules = [mod for mod in test_modules if mod.lower() not in excludes]
        print('test_modules:')
        print(test_modules)
        for mod in test_modules:

            imported_mod = __import__(mod, globals(), locals())

            suite.addTests(
                unittest.defaultTestLoader.loadTestsFromModule(imported_mod))

    unittest.TextTestRunner(verbosity=3).run(suite)


if __name__ == '__main__':
    run_tests()