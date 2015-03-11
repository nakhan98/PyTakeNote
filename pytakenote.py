#!/usr/bin/env python3

'''
# PyTakeNote #
- A simple CLI notetaking app written in Python 3
- Needed an upgrade from my notes.txt file
'''

__author__ = "Nasef Khan (inbox@nakhan.net)"
__license__ = 'GPL3' # see http://www.gnu.org/licenses/gpl.html'
__version__ = "0.1.0" 


import sys
#import pdb
import sqlite3
import tempfile
import os
from datetime import datetime
from subprocess import call

db_filepath = ""
db_name = ".pytakenote.db"
file_location = os.path.dirname(os.path.abspath(__file__))


def search_db_file():
    global db_filepath
    if os.path.isfile("./"+db_name):
        db_filepath = "./"+db_name
    elif os.path.isfile( os.getenv("HOME") + "/" + db_name ):
        db_filepath = os.getenv("HOME") + "/" + db_name


def dbconn(db_filepath):
    conn = sqlite3.connect(db_filepath)
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


def create_db():
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


def print_all_notes():
    conn, c = dbconn(db_filepath)
    results = c.execute("SELECT id, title, body, datetime FROM Notes;")
    notes = results.fetchall()
    if not notes:
        print("No notes saved")
        sys.exit(0)
    print("%-3s %-48s %-16s" % ("ID", "Title", "Date"))
    print("-" * 72)
    for note in notes:
        print("%-3d %-48s %-16s" % (note[0], note[1], note[3]))
    #print("\n")


def get_title():
    title = input("Please enter a title: ")
    return title


def get_body():
    tf = tempfile.NamedTemporaryFile(delete=False)
    tf.write("Enter you note here... (you can delete this line)".encode())
    tf.close()
    editor = os.getenv("EDITOR")
    if editor:
        call([editor, tf.name])
    else:
        call(["nano", tf.name])
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


def add_note( id_=None, title="", body="", current_datetime = str(datetime.now())[:-7] ):
    conn, c = dbconn(db_filepath)
    if id_:
        sql = "INSERT INTO Notes(id, title, body, datetime) values(?, ?, ?, ?)"
        c.execute(sql, (id_, title, body, current_datetime))
    else:
        sql = "INSERT INTO Notes(title, body, datetime) values(?, ?, ?)"
        c.execute(sql, (title, body, current_datetime))
    conn.commit()
    conn.close()


def delete_note(id_):
    conn, c = dbconn(db_filepath)
    note = c.execute("SELECT * FROM Notes WHERE id=?", (id_,))
    note = note.fetchall()
    if not note:
        print("No note exists by that ID")
        sys.exit(2)

    try:
        sql = "DELETE FROM Notes WHERE id=?"
        c.execute(sql, (id_,))
    except Exception as err:
        print("Error: " + str(err))
    finally:
        print("Note deleted")
        conn.commit()
        conn.close()
    

def edit_note(id_):
    conn, c = dbconn(db_filepath)
    notes = c.execute("SELECT title, body FROM Notes WHERE id=?", (id_,))
    notes = notes.fetchall()
    if not notes:
        print("No note exists by that ID")
        conn.close()
        sys.exit(2)
    note = notes[0]
    title, body, = note
    _ = input("Edit title [%s]? " % title)
    _ = _.strip()
    if _ != "":
        title = _
    print(title)
    tf = tempfile.NamedTemporaryFile(delete=False)
    body_bytes = body.encode()
    tf.write(body_bytes)
    tf.close()
    editor = os.getenv("EDITOR")
    if editor:
        call([editor, tf.name])
    else:
        call(["nano", tf.name])

    with open(tf.name, "rt") as f:
        body = f.read().rstrip()
    os.unlink(tf.name)

    c.execute("UPDATE Notes SET title=?, body=? WHERE id=?", (title, body, id_))
    conn.commit()
    conn.close()


def show_note(id_):
    conn, c = dbconn(db_filepath)
    notes = c.execute("SELECT title, body FROM Notes WHERE id=?", (id_,))
    notes = notes.fetchall()
    conn.close()
    if not notes:
        print("No note exists by that ID")
        sys.exit(2)
    note = notes[0]
    title, body, = note
    print("Title: %s" % title)
    print("Body: %s" % body)


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
        print_all_notes()
        sys.exit(0)
        

    if sys.argv[1].upper() == "ADD":
        title = get_title()
        body = get_body()
        deleted_key = get_unused_key()
        if deleted_key:
            add_note(id_=deleted_key, title=title, body=body)
        else:
            add_note(title=title, body=body)
    elif sys.argv[1].upper() in ("DEL", "DELETE"):
        if len(sys.argv) != 3:
            print("Error... To delete a note please specify note ID. For example:")
            print("./pytakenote.py delete 2")
            sys.exit(2)
        try:
            id_to_delete = int(sys.argv[2])
        except:
            print("Error... The ID is an integer")
        else:
            delete_note(id_to_delete)
    elif sys.argv[1].upper() == "EDIT":
        if len(sys.argv) != 3:
            print("Error... To edit a note please specify note ID. For example:")
            print("./pytakenote.py edit 2")
            sys.exit(2)
        try:
            id_to_edit = int(sys.argv[2])
        except:
            print("Error... Please enter an integer")
        else:
            edit_note(id_to_edit)
    elif sys.argv[1].upper() == "SHOW":
        if len(sys.argv) != 3:
            print("Error... To show a note please specify note ID. For example:")
            print("./pytakenote.py show 2")
            sys.exit(2)
        try:
            id_to_show = int(sys.argv[2])
        except:
            print("Error... Please enter an integer")
        else:
            show_note(id_to_show)


if __name__ == "__main__":
    main()
