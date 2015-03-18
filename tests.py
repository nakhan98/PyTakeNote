#!/usr/bin/env python3

import unittest
from pytakenote import *

class test_functions(unittest.TestCase):
    def setUp(self):
        print("Testing toplevel pytakenote functions")

    def test_get_current_date_time(self):
        curr_time = get_current_datetime()
        self.assertEqual(str, type(curr_time))
        self.assertIn(":", curr_time)
    
    def tearDown(self):
        print("Testing finished")

if __name__ == '__main__':
    unittest.main()
