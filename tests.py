#!/usr/bin/env python3

import unittest
import os
#import pdb
import pytakenote
import sqlite3

pytakenote.db_name = "test_db"

class Test_other_functions(unittest.TestCase):
    def setUp(self):
        self.location_1 = "./%s" % pytakenote.db_name
        self.location_2 = "%s/%s" % (os.getenv("HOME"), pytakenote.db_name)

    def test_get_current_date_time(self):
        curr_time = pytakenote.get_current_datetime()
        # 2015-03-18 23:48:27
        self.assertRegex(curr_time, r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}", 
                msg="Date should be in the following format: 'yyyy-mm-dd hh:mm:ss'")

    def test_ask_db_location(self):
        self.assertEqual(pytakenote.ask_db_location(lambda: "1"), self.location_1)
        self.assertEqual(pytakenote.ask_db_location(lambda: "2"), self.location_2)



class Test_search_db(unittest.TestCase):
    def setUp(self):
        self.file_path_current = "./%s" % (pytakenote.db_name,)
        open(self.file_path_current, 'w').close()
        self.file_path_home = "%s/%s" % (os.getenv("HOME"), pytakenote.db_name)
        open(self.file_path_home, 'w').close()
    
    def test_search_db_in_current_folder(self):
        pytakenote.search_db_file()
        self.assertEqual(pytakenote.search_db_file(), self.file_path_current)

    def test_search_db_in_home_folder(self):
        os.unlink(self.file_path_current) # delete this file as search_db checks current folder first 
        pytakenote.search_db_file()
        self.assertEqual(pytakenote.search_db_file(), self.file_path_home)

    def tearDown(self):
        try:
            os.unlink(self.file_path_current)
            os.unlink(self.file_path_home)
        except FileNotFoundError:
            pass


class Test_database_functions(unittest.TestCase):
    def setUp(self):
        self.file_path_current = "./%s" % (pytakenote.db_name,)
        open(self.file_path_current, 'w').close()
        pytakenote.search_db_file()
        self.conn, self.cursor = pytakenote.dbconn(self.file_path_current)

    def test_dbconn(self):
        #pdb.set_trace()
        self.assertIs(type(self.conn), sqlite3.Connection)
        self.assertIs(type(self.cursor), sqlite3.Cursor)
        
    def tearDown(self):
        self.conn.close()
        os.unlink(self.file_path_current)


class Test_get_unused_keys(unittest.TestCase):
    def test_get_unused_keys(self):
        db_path = "./%s" % pytakenote.db_name
        try:
            os.unlink(db_path)
        except FileNotFoundError:
            pass
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        create_table_SQL = "CREATE TABLE Notes (id INTEGER PRIMARY KEY, title TEXT, body TEXT, datetime DATETIME);"
        insert_SQL = "INSERT INTO Notes(title) VALUES(\"dummy\");"
        delete_SQL = "DELETE FROM Notes WHERE ID=1;"
        c.execute(create_table_SQL)
        conn.commit()
        c.execute(insert_SQL)
        conn.commit()
        c.execute(insert_SQL)
        conn.commit()
        c.execute(delete_SQL)
        conn.commit()
        unused_key = pytakenote.get_unused_key()
        self.assertEqual(unused_key, 1)


if __name__ == '__main__':
    unittest.main()
