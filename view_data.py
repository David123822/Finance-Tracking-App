from graphs import Graph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as GraphLink
import mplcursors
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

graph = Graph()

with sqlite3.connect("data.db") as db:
    cursor = db.cursor()


def view_data(): #the main window for seeing the data
    global viewin, monthOption, yearOption

    viewin = Toplevel()
    window_height = 600
    window_width = 500
    viewin.title("Displaying the data in a visual way")
    viewin.geometry(f"{window_height}x{window_width}")
 
 # the combobox meniu for choosing the month
    monthOption = StringVar()
    months = get_months()

    if not months:
        months = ["No months found"]

    combobox = ttk.Combobox(viewin, values=months, textvariable= monthOption)
    combobox.grid(row=0, column=2, pady=10, sticky="n")

    # the combobox meniu for choosing the year
    yearOption = StringVar()
    years = get_year()

    if not years:
        years = ["No year found"]

    combobox2 = ttk.Combobox(viewin, values=years, textvariable= yearOption)
    combobox2.grid(row=0, column=2, pady=10, padx=10, sticky="s")

# for testing 
    output = Listbox(viewin)#, height= 30, width=40)
    output.grid(row=0, column=0, pady=10)

    month = Listbox(viewin)
    month.grid(row=0, column=1, pady= 10)

    viewin.mainloop()



def get_total_income(month, year):
    ammount = []
    cursor.execute("SELECT ammount FROM Income WHERE month =? AND year=?",(month, year))

    # fetch the row from the result set
    row = cursor.fetchall()

    for item in row:
        ammount.append(item)
    
    total_income_of_the_month = sum(ammount)
    return total_income_of_the_month


def get_expences_data(month):
    #month = monthOption.get()
    labels = []
    ammount = []

    cursor.execute("SELECT label, ammount FROM Expences WHERE month = ?", (month,))

    for row in cursor.fetchall():
        labels.append(row[0])
        ammount.append(row[1])
    
    expences_for_the_month = sum(ammount)
    
    return labels, ammount, expences_for_the_month

def get_months():
    months = set()
    cursor.execute("SELECT DISTINCT month FROM Income")

    rows = cursor.fetchall()
    for row in rows:
        months.add(row[0])

    return list(months)

def get_year():
    years = set()
    cursor.execute("SELECT DISTINCT year FROM Income")

    rows = cursor.fetchall()
    for row in rows:
        years.add(row[0])

    return list(years)


view_data()
