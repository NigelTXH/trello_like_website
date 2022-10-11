from tkinter import *
from datetime import datetime

class Timer():
    
    def __init__(self, starting_time):
        self.counter = starting_time
        self.running = False
        self.main = True
        
    
