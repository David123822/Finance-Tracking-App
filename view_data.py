from graphs import Graph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as GraphLink
import mplcursors
import sqlite3
from tkinter import *

graph = Graph()

with sqlite3.connect("data.db") as db:
    cursor = db.cursor()



def view_data(): #the main window for seeing the data
    pass
