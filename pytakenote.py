#!/usr/bin/env python3

'''
# PyTakeNote #
- A simple CLI notetaking app written in Python 3
- Needed an upgrade from my notes.txt file
'''

__author__ = "Nasef Khan (inbox@nakhan.net)"
__license__ = 'GPL3' # see http://www.gnu.org/licenses/gpl.html
__version__ = "0.2.0" 

import sys
#import pdb
import sqlite3
import tempfile
import os
from datetime import datetime
from subprocess import call

#pdb.set_trace()

db_filepath = ""
db_name = ".pytakenote.db"
file_location = os.path.dirname(os.path.abspath(__file__))

class Note:
    def __init__(self, id_=None):
        if id_: # load note from db if note id id_ exists
            self.load(id_)
        else:
            self.create_new()

    def create_new(self):
        self.id_ = get_unused_key() # to re-use deleted ids
        self.title = input("Please enter a title: ")
        self.body = get_body()
        self.date_time = get_current_datetime()
        self.save_to_db()

    def load(self, id_):
        '''load note from db'''
        conn, c = dbconn(db_filepath)
        sql = "SELECT id, title, body FROM Notes WHERE id=?"
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
        conn, c = dbconn(db_filepath)
        sql = "DELETE FROM Notes WHERE id=?"
        c.execute(sql, (self.id_,))
        conn.commit()
        conn.close()

    def check_note(self, id_):
        ''' Check if any data exists at id id_ in table'''
        #pdb.set_trace()
        conn, c = dbconn(db_filepath)
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
        conn, c = dbconn(db_filepath)
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

    def print_all_notes():
        conn, c = dbconn(db_filepath)
        results = c.execute("SELECT id, title, body, datetime FROM Notes;")
        notes = results.fetchall()
        conn.close()
        if not notes:
            print("No notes saved")
            sys.exit(0)
        print("%-3s %-48s %-16s" % ("ID", "Title", "Date"))
        print("-" * 72)
        for note in notes:
            print("%-3d %-48s %-16s" % (note[0], note[1], note[3]))
        #print("\n")


def get_current_datetime():
   return str( datetime.now() )[:-7]


def search_db_file():
    global db_filepath
    if os.path.isfile("./"+db_name):
        db_filepath = "./"+db_name
    elif os.path.isfile( os.getenv("HOME") + "/" + db_name ):
        db_filepath = os.getenv("HOME") + "/" + db_name


def dbconn(sqlite_file=db_filepath):
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return (conn, c)


def ask_db_location():
    print("\nWhere do you wish to save the database file?")
    print("1 - Same location as Python script (%s)" % file_location)
    print("2 - Your home Directory (%s)" % os.getenv("HOME"))
    print("")
    chosen = 0
    while not chosen:
        choice = input(">> ") 
        choice = choice.strip()
        if choice in ("1", "2"):
            chosen = 1
        else:
            print("Enter 1 or 2\n")
    choice = int(choice)
    return ["./"+db_name, os.getenv("HOME") + "/" +  db_name][choice-1]


def create_db(filepath=None):
    if not filepath:
        filepath = ask_db_location()
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


def get_unused_key():
    '''Reuse deleted keys'''
    conn, c = dbconn(db_filepath)
    sql = "SELECT id FROM Notes ORDER BY id ASC ";
    results = c.execute(sql)
    keys = [int(i[0]) for i in results.fetchall()]
    conn.close()
    if not keys:
        return None
    del_keys = [i for i in range(1, keys[-1]+1) if i not in keys]
    if del_keys:
        return del_keys[0]


def main():
    search_db_file()

    if not os.path.isfile(db_filepath):
        print("Creating notetaker Database...")
        if create_db():
            print("Database created succesfully.\n")
            main()
            sys.exit(0)
        else:
            print("Database could not be created...")
            sys.exit(1)

    if len(sys.argv) == 1:
        Note.print_all_notes()
        sys.exit(0)
        

    if sys.argv[1].upper() == "ADD":
        new_note = Note()
    elif sys.argv[1].upper() in ("DEL", "DELETE"):
        if len(sys.argv) != 3:
            print("Error... To delete a note please specify note ID. For example:")
            print("./pytakenote.py delete 2")
            sys.exit(2)
        note = Note(sys.argv[2])
        note.delete()
    elif sys.argv[1].upper() == "EDIT":
        if len(sys.argv) != 3:
            print("Error... To edit a note please specify note ID. For example:")
            print("./pytakenote.py edit 2")
            sys.exit(2)
        note  = Note(sys.argv[2])
        note.edit()
    elif sys.argv[1].upper() == "SHOW":
        if len(sys.argv) != 3:
            print("Error... To show a note please specify note ID. For example:")
            print("./pytakenote.py show 2")
            sys.exit(2)
        note = Note(sys.argv[2])
        note.print_()
    else:
        print("Whaaaat?")

if __name__ == "__main__":
    main()
