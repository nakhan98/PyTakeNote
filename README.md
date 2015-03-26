# PyTakeNote #
- A simple CLI notetaking app written in Python 3 and SQLite
- Needed an upgrade from my notes.txt file

## Instructions
- Help:
    ./pytakenote.py -h
- List all notes:
    ./pytakenote.py
- Add a note:
    ./pytakenote.py -a 
- Show a note
    ./pytakenote.py -s [Note ID]
- Edit a note:
    ./pytakenote.py -e [Note ID]
- Delete a note:
    ./pytakenote.py -d [Note ID]
- Specify another db file to use (will create if necessary):
    ./pytakenote -c ~/Dropbox/.my_notes.db

## Todos
- Categories
- Search
- <del>Use argparse as current arg handling is fugly</del>
- Simple Encryption?
- System-wide installation script?
