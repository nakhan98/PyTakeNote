# PyTakeNote #
- A simple CLI notetaking app written in Python 3 and SQLite
- Needed an upgrade from my notes.txt file

## System-wide installation
- wget -O - https://raw.githubusercontent.com/nakhan98/PyTakeNote/master/installer.sh | sudo sh

## Instructions
- Help:
    pytakenote -h
- List all notes:
    pytakenote
- Add a note:
    pytakenote -a 
- Show a note
    pytakenote -s [Note ID]
- Edit a note:
    pytakenote -e [Note ID]
- Delete a note:
    pytakenote -d [Note ID]
- Specify another db file to use (will create if necessary):
    pytakenote -c ~/Dropbox/.my_notes.db

## Todos
- Categories
- Search
- <del>Use argparse as current arg handling is fugly</del>
- Simple Encryption?
- <del>System-wide installation script?</del>
