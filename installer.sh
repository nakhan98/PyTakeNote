#!/bin/sh
# Downloads and installs latest stable build of PyTakeNote from Github
# license = 'GPL3' # see http://www.gnu.org/licenses/gpl.html
#set -e

user=`id -u`
if [ $user -ne 0 ]; then
    printf "Please run this as root\n"
    exit 1
fi

python3 -V > /dev/null 2>&1
if [ $? -ne 0 ]; then
    printf "Error: Python 3 doesn't appear to be installed on this system!\n"
    printf "Please install it and run this installer again.\n"
    exit 1
fi

SRC_DIR=/usr/local/PyTakeNote
BIN_DIR=/usr/local/bin
#SRC_DIR=/tmp/PyTakeNote_
#BIN_DIR=/tmp/bin
printf "Downloading PyTakeNote...\n"
wget --quiet https://raw.githubusercontent.com/nakhan98/PyTakeNote/master/pytakenote.py -O /tmp/pytakenote.py 
if [ $? -ne 0 ]; then
    printf "Error encountered while download PyTakenote. Please try again later." 
    exit 1;
fi

if [ ! -d $SRC_DIR ]; then
    mkdir -p $SRC_DIR
fi

mv /tmp/pytakenote.py $SRC_DIR;
printf "Creating symlinks...\n"
ln -fs $SRC_DIR/pytakenote.py $BIN_DIR/pytakenote
ln -fs $SRC_DIR/pytakenote.py $BIN_DIR/takenote
chmod +x $SRC_DIR/pytakenote.py 
printf "Installation completed!\nRun 'pytakenote' or simply 'takenote' at the command line!\n"
