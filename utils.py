from sys import stdin
from termios import tcgetattr, tcsetattr, TCSADRAIN
from tty import setraw
from os import system

def getch():
    file_descriptor = stdin.fileno()
    old_settings = tcgetattr(file_descriptor)
    try:
        setraw(file_descriptor)
        character = stdin.read(1)
    finally:
        tcsetattr(file_descriptor, TCSADRAIN, old_settings)
    return character


def clear(clear_num=40):
    """
        clears the screen by printing too many blank lines
    """
    system('clear')
