import datetime
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


with sqlite3.connect("data.db") as db:
    cursor = db.cursor()

current_time = datetime.date.today()
#month = current_time.month
year = current_time.year
"""
need to insert data into Income, expences, labels and savings so i can work on visualising the data

month will be an important variable and the year as well.

make a tk app that will have the 3 fields inseparate LabelFrames and then clears the data as it is geing submitted

!!Does not need to be pretty!!
"""

def get_income_ID(label, month):
    cursor.execute("SELECT id FROM Income WHERE label=? AND month = ? ",(label,month))

    # fetch the row from the result set
    row = cursor.fetchone()

    # check if the row was found
    if row:
        return row[0] # returns the ID (which is the first column in the result row)
    else:
        return None
    
def add_labels():
    cursor.execute("SELECT DISTINCT label FROM Expences")  # Using DISTINCT to avoid duplicates in the fetched results
    labels = cursor.fetchall()
    
    # Extract labels from the fetched rows
    for label_tuple in labels:
        label = label_tuple[0]
        
        # Check if the label already exists in the Labels table
        cursor.execute("SELECT 1 FROM Labels WHERE label = ?", (label,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO Labels (label) VALUES (?)", (label,))
            print(f"Added {label} into the label table")

    # Commit once after all insertions
    db.commit()


def get_months():
    months = set()
    cursor.execute("SELECT DISTINCT month FROM Income")

    rows = cursor.fetchall()
    for row in rows:
        months.add(row[0])

    return list(months)

def addIncome():
    label = in_name.get()
    month = monthOption.get()
    #year = year
    ammount = in_value.get()
    cursor.execute("INSERT INTO Income (label, month, ammount, year) VALUES (?,?,?,?)", (label, month, ammount, year))
    db.commit()
    print(f"Added {label} to the database")

    in_name.delete(0,END)
    monthOption.set(NONE)
    in_value.set(0.0)

    window.destroy()
    display()
    


def addExpences():
    label = expence_name.get()
    month = ex_month.get()
    ammount = ex_value.get()
    link_to_income = get_income_ID("Salary", month)

    cursor.execute("INSERT INTO Expences (label, month, ammount, link_to_income) VALUES (?,?,?,?)", (label, month, ammount, link_to_income))
    db.commit()

    print(f"Added {label} to the database")

    add_labels()
    #print(f"Added {label} to the Labels table")

    expence_name.delete(0,END)
    ex_month.set(NONE)
    ex_value.set(0.0)


def addsavtodb():
    month = sav_month.get()
    ammount = sav_value.get()
    cursor.execute("INSERT INTO Savings(month, ammount, year) VALUES(?,?,?)",(month, ammount, year))
    db.commit()

    print("Added savings")

    sav_month.set(NONE)
    sav_value.set(0.0)


def display():
    global window, sav_month, sav_value, ex_value, ex_month, expence_name, in_name, monthOption, in_value

    window= Tk()
    window_height = 500
    window_width = 245
    window.geometry(f"{window_height}x{window_width}")
    window.title("Adding data to the database")

    # the income part
    incomeFrame= ttk.LabelFrame(window, text="Income")
    incomeFrame.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    in_name = Entry(incomeFrame)
    in_name.insert(0,"Salary")
    in_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    monthOption = IntVar()
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    comboBox = ttk.Combobox(incomeFrame, values=months, textvariable=monthOption)
    comboBox.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    in_value = DoubleVar()
    spinbox = Spinbox(incomeFrame, from_=0.0, to=100000.0, increment=0.1, textvariable=in_value)
    spinbox.grid(row=3, column=0, padx=5, pady=10, sticky="w")

    Button(incomeFrame, text="Submit", command=addIncome, bg="green", fg="white").grid(row=4, column=0, pady=10)

    # the expence part

    expenceLabel = ttk.LabelFrame(window, text= "Expences")
    expenceLabel.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    expence_name = Entry(expenceLabel)
    expence_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    ex_month = IntVar()
    emonths= get_months()
    if not emonths:
        emonths = ["no data"]
    comboBox = ttk.Combobox(expenceLabel, values=emonths, textvariable=ex_month)
    comboBox.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    ex_value = DoubleVar()
    spinbox = Spinbox(expenceLabel, from_=0.0, to=100000.0, increment=0.1, textvariable=ex_value)
    spinbox.grid(row=3, column=0, padx=5, pady=10, sticky="w")

    Button(expenceLabel, text="Submit", command=addExpences, bg="red", fg="white").grid(row=4, column=0, pady=10)

    # the saving part
    savingLabel = ttk.LabelFrame(window, text= "Savings")
    savingLabel.grid(row=0, column=2, padx=5, pady=5, sticky="w")

    sav_month = IntVar()
    savmonths= get_months()
    if not savmonths:
        savmonths = ["no data"]
    comboBox = ttk.Combobox(savingLabel, values=savmonths, textvariable=sav_month)
    comboBox.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    sav_value = DoubleVar()
    spinbox = Spinbox(savingLabel, from_=0.0, to=1500.0, increment=0.1, textvariable=sav_value)
    spinbox.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    Button(savingLabel, text="Submit", command=addsavtodb, bg="blue", fg="white").grid(row=4, column=0, pady=10)
    window.mainloop()

display()