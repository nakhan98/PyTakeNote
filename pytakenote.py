#!/usr/bin/env python3

'''
# PyTakeNote #
- A simple CLI notetaking app written in Python 3
- Needed an upgrade from my notes.txt file
'''

__author__ = "Nasef Khan (inbox@nakhan.net)"
__license__ = 'GPL3' # see http://www.gnu.org/licenses/gpl.html
__version__ = "0.3.0" 

import sys
import sqlite3
import tempfile
import os
import argparse
from datetime import datetime
from subprocess import call
import ipdb

db_name = ".pytakenote.db"

class Note:
    def __init__(self, db, id_=None):
        self.db = db
        if id_: # load note from db if note id id_ exists
            self.load(id_)
        else:
            self.create_new()

    def create_new(self):
        self.id_ = get_unused_key(self.db) # to re-use deleted ids
        self.title = input("Please enter a title: ")
        self.body = get_body()
        self.date_time = get_current_datetime()
        self.save_to_db()

    def load(self, id_):
        '''load note from db'''
        conn, c = dbconn(self.db)
        sql = "SELECT id, title, body FROM Notes WHERE id=?"
        #ipdb.set_trace()
        id_ = str(id_)
        data = c.execute(sql, (id_)).fetchone()
        conn.close()
        if data:
            self.id_, self.title, self.body = data
        else:
            print("No note exists with that ID")
            sys.exit(1)

    def edit(self):
        _ = input("Edit title [%s]? " % self.title)
        _ = _.strip()
        if _ != "":
            self.title = _
        self.body = get_body(self.body)
        self.date_time = get_current_datetime()
        self.save_to_db()
    
    def delete(self):
        conn, c = dbconn(self.db)
        sql = "DELETE FROM Notes WHERE id=?"
        c.execute(sql, (self.id_,))
        conn.commit()
        conn.close()

    def check_note(self, id_):
        ''' Check if any data exists at id id_ in table'''
        #pdb.set_trace()
        conn, c = dbconn(self.db)
        sql = "SELECT id FROM Notes WHERE id=?"
        result = c.execute(sql, (id_,)).fetchone()
        conn.close()
        if result:
            return True
        else:
            return False

    def print_(self):
        print("Title: %s" % self.title)
        print("Body: %s" % self.body)

    def save_to_db(self):
        conn, c = dbconn(self.db)
        if self.id_:
            if self.check_note(self.id_): # note being edited
                sql = "UPDATE Notes SET title=?, body=?, datetime=? WHERE id=?"
                c.execute(sql, (self.title, self.body, self.date_time, self.id_))
            else: # new note being saved as lowest deleted id
                sql = "INSERT INTO Notes(id, title, body, datetime) values(?, ?, ?, ?)"
                c.execute(sql, (self.id_, self.title, self.body, self.date_time))
        else:
            sql = "INSERT INTO Notes(title, body, datetime) values(?, ?, ?)"
            c.execute(sql, (self.title, self.body, self.date_time))
        conn.commit()
        conn.close()

    def print_all_notes(db):
        conn, c = dbconn(db)
        results = c.execute("SELECT id, title, body, datetime FROM Notes;")
        notes = results.fetchall()
        conn.close()
        if not notes:
            print("No notes saved")
            sys.exit(0)
        print("%-3s %-48s %-16s" % ("ID", "Title", "Date"))
        print("-" * 72)
        for note in notes:
            print("%-3d %-48s %-16s" % (note[0], shorten_string(note[1]), note[3]))
        #print("\n")


def get_current_datetime():
   return str( datetime.now() )[:-7]


def shorten_string(string):
    ''' To stop titles overrunning'''
    if len(string) > 49:
        string = string[:45] + "..."
    return string 


def search_db_file():
    if os.path.isfile("./"+db_name):
        db_filepath = "./"+db_name
        return db_filepath
    elif os.path.isfile( os.getenv("HOME") + "/" + db_name ):
        db_filepath = os.getenv("HOME") + "/" + db_name
        return db_filepath


def dbconn(sqlite_file):
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return (conn, c)


def create_db(filepath):
    create_table_sql = "CREATE TABLE Notes (id INTEGER PRIMARY KEY, title TEXT, body TEXT, datetime DATETIME);"
    conn, c = dbconn(filepath)
    try:
        ret_cur = c.execute(create_table_sql)
        conn.commit()
    except Exception as err:
        print("Error: " + str(err))
        conn.close()
        return False
    else:
        _ = ret_cur.fetchall()
        conn.close()
        return True


def open_editor(filepath):
    editor = os.getenv("EDITOR")
    if editor:
        call([editor, filepath])
    else:
        call(["nano", filepath])


def get_body(content=None):
    if not content:
        content = "Enter you note here... (you can delete this line)"
    tf = tempfile.NamedTemporaryFile(delete=False)
    tf.write(content.encode())
    tf.close()
    open_editor(tf.name)
    with open(tf.name, "rt") as f:
        body = f.read().rstrip()
    os.unlink(tf.name)
    return body


def get_unused_key(db):
    '''Reuse deleted keys'''
    conn, c = dbconn(db)
    sql = "SELECT id FROM Notes ORDER BY id ASC ";
    results = c.execute(sql)
    keys = [int(i[0]) for i in results.fetchall()]
    conn.close()
    if not keys:
        return None
    del_keys = [i for i in range(1, keys[-1]+1) if i not in keys]
    if del_keys:
        return del_keys[0]


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()

    parser.add_argument("-c", "--db", "--config", type=str,  
            default=os.getenv("HOME") + "/" + db_name,
            help="Specify a location of a config/db file to use")
    group.add_argument("-l", "--list", action="store_true", 
            help="Print out all notes")
    group.add_argument("-a", "--add", action="store_true", 
            help="Add a note")
    group.add_argument("-d", "--delete", "--remove", type=int, 
            help="Delete a note (specify an ID)")
    group.add_argument("-e", "--edit", type=int, 
            help="Edit a note (specify an ID)")
    group.add_argument("-s", "--show", type=int, 
            help="Show a note (specify an ID)")

    args = parser.parse_args(argv)

    #ipdb.set_trace()
    db = args.db

    if not os.path.isfile(args.db):
        print("Creating notetaker Database...")
        create_db(db)
        print("Database created succesfully.\n")
        main(argv)
        sys.exit(0)
    
    if args.list:
        Note.print_all_notes(db)
    elif args.add:
        Note(db)
    elif args.delete:
        note = Note(db, args.delete)
        note.delete()
    elif args.edit:
        note = Note(db, args.edit)
        note.edit()
    elif args.show:
        note = Note(db, args.show)
        note.print_()
    else:
        Note.print_all_notes(db)



if __name__ == "__main__":
    main(sys.argv[1:])
