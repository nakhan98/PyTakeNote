#!/usr/bin/env python3

import unittest
import pytakenote 

class test_functions(unittest.TestCase):
    def setUp(self):
        print("Testing toplevel pytakenote functions")

    def test_get_current_date_time(self):
        curr_time = pytakenote.get_current_datetime()
        # 2015-03-18 23:48:27
        self.assertRegex(curr_time, r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}", msg="Date should be in the following format: 'yyyy-mm-dd hh:mm:ss'")
    
    def tearDown(self):
        print("Testing finished")

if __name__ == '__main__':
    unittest.main()
