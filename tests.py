#!/usr/bin/env python3

import unittest
import pytakenote 
import os
import pdb

class test_functions(unittest.TestCase):
    def test_get_current_date_time(self):
        curr_time = pytakenote.get_current_datetime()
        # 2015-03-18 23:48:27
        self.assertRegex(curr_time, r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}", msg="Date should be in the following format: 'yyyy-mm-dd hh:mm:ss'")

class Test_search_db_curr_folder(unittest.TestCase):
    import pytakenote
    def setUp(self):
        #pdb.set_trace()
        pytakenote.db_name = "test_name"
        self.file_path_current = "./%s" % (pytakenote.db_name,)
        self.file_path_home = "%s/%s" % (os.getenv("HOME"), pytakenote.db_name)
    
    def test_search_db_in_current_folder(self):
        open(self.file_path_current, 'w').close()
        pytakenote.search_db_file()
        self.assertEqual(pytakenote.db_filepath, self.file_path_current)

    def tearDown(self):
        os.unlink(self.file_path_current)


class Test_search_db_home_folder(unittest.TestCase):
    import pytakenote
    def setUp(self):
        #pdb.set_trace()
        pytakenote.db_name = "test_name"
        self.file_path_home = "%s/%s" % (os.getenv("HOME"), pytakenote.db_name)
    
    def test_search_db_in_home_folder(self):
        open(self.file_path_home, 'w').close()
        pytakenote.search_db_file()
        self.assertEqual(pytakenote.db_filepath, self.file_path_home)

    def tearDown(self):
        os.unlink(self.file_path_home)


if __name__ == '__main__':
    unittest.main()
