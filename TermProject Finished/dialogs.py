from random import *
from math import *
import pygame
import time
import pickle
import subprocess
from tkinter import *
from tkinter import messagebox, simpledialog
#from dialogs import *



def choose():
    root = Tk()
    root.withdraw()
    response = simpledialog.askstring('','Please enter a Filename')
    return response

print(choose())