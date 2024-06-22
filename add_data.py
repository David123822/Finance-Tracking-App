import datetime
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

current_time = datetime.date.today()
month = current_time.month
year = current_time.year

def add_data(): # display the window to add data
    global addwin, in_name, in_value, ex_value, select

    addwin = Toplevel()
    window_height = 345
    window_width = 245
    addwin.geometry(f"{window_height}x{window_width}")
    addwin.title("Adding the income and the expences")
    
    menu_bar = top_menu(addwin) # adding the manu at the top
    
    # the income part

    labelframe = ttk.LabelFrame(addwin, text="Income")
    labelframe.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    label_in_labelframe = ttk.Label(labelframe, text="Label")
    label_in_labelframe.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    in_name = Entry(labelframe)
    in_name.insert(0,"Salary")
    in_name.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    
    label_in_labelframe2 = ttk.Label(labelframe, text="Amount")
    label_in_labelframe2.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    
    in_value = DoubleVar()
    spinbox = Spinbox(labelframe, from_=0.0, to=100000.0, increment=0.1, textvariable=in_value)
    spinbox.grid(row=3, column=0, padx=5, pady=10, sticky="w")

    Button(labelframe, text="Submit", command=addIncome, bg="green", fg="white").grid(row=4, column=0, pady=10)
    
    # the expences part
    labelframe2 = ttk.LabelFrame(addwin, text="Expences")
    labelframe2.grid(row=0, column=2, padx=10, pady=10, sticky="s")

    label1 = ttk.Label(labelframe2, text="Label")
    label1.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    select = StringVar()
    items = get_espences()
    
    if not items:
        items = ["No expences found"]

    select.set("Select from database")
    option_menu= OptionMenu(labelframe2, select, *items)
    option_menu.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    label2 = ttk.Label(labelframe2, text="Amount")
    label2.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    
    ex_value = DoubleVar()
    spinbox = Spinbox(labelframe2, from_=0.0, to=100000.0, increment=0.1, textvariable=ex_value)
    spinbox.grid(row=3, column=0, padx=5, pady=10, sticky="w")

    Button(labelframe2, text="Submit", command=addExpences, bg="red", fg="white").grid(row=4, column=0, pady=10)
        
    addwin.config(menu=menu_bar, bg="black")
    addwin.mainloop()

def addIncome(): # dont forget to reset the fields at the end
    income_label = in_name.get()
    income = in_value.get()

    if  not income_label:
        messagebox.showerror("Error", "Please assign a label to the income")
    else:
        cursor.execute("INSERT INTO Income (label, month, ammount, year) VALUES (?,?,?,?)", (income_label, month, income, year))
        db.commit()
        #print(f"{income_label} -> {income}")

    # clean the fields
    in_name.delete(0, END)
    #in_name.insert(0,"Salary")
    in_value.set(0.0)



def addExpences():
    expence_label = select.get()
    expence = ex_value.get()
    income_ID = get_income_ID("Salary",month)

    if expence_label == "Select from database" or expence_label == "No expences found":
        messagebox.showerror("Error", "Please choose a label, it is needed for the graphs")
    else:
        # add tp database
        if income_ID is None:
            income_ID = None
            messagebox.showerror("Error",f"No Salary was set for this ({month}) month")
            #print(f"{expence_label} -> {expence} -> {income_ID}")
        else:
            cursor.execute("INSERT INTO Expences (label, month, ammount, link_to_income) VALUES (?,?,?,?)", (expence_label, month, expence, income_ID))
            db.commit()
            #print(f"{expence_label} -> {expence} -> {income_ID}") # add this to the database
    
    # cleaning the data
    select.set("Select from database")
    ex_value.set(0.0)
    



def top_menu(link):
    menu_bar = Menu(link)

    # Create the "File" menu
    file_menu = Menu(menu_bar, tearoff=0)
    #file_menu.add_command(label="Add Income label", command=None)
    file_menu.add_command(label="Add Expences label", command=addLabel)
    file_menu.add_command(label="Add Savings", command=addsavings)
    file_menu.add_separator()
    file_menu.add_command(label="Refresh page", command=refreshnow)
    file_menu.add_command(label="Exit", command=link.destroy)
    menu_bar.add_cascade(label="Menu", menu=file_menu)

    #refresh = Menu(menu_bar, tearoff=0)
    #refresh.add_command(label="Refresh page", command=refreshnow)
    #menu_bar.add_cascade(label="Refresh page", menu=refresh)
    return menu_bar

def refreshnow():
    addwin.destroy()
    add_data()

def addLabel():
    global addlab, ex_label_entry
    
    addlab = Toplevel()
    addlab.title("Add Label")
    
    label1 = Frame(addlab)
    label1.pack(padx=20, pady=20)
    
    label_prompt = Label(label1, text="Enter Label:")
    label_prompt.grid(row=0, column=0, padx=5, pady=5)
    
    ex_label_entry = Entry(label1)
    ex_label_entry.focus()
    ex_label_entry.grid(row=0, column=1, padx=5, pady=5)
    
    submit_button = Button(label1, text="Submit", command=add_to_database, bg="green", fg="white")
    submit_button.grid(row=1, column=0, columnspan=2, pady=10)
    
    addlab.mainloop()

def add_to_database():
    global ex_label_entry
    name = ex_label_entry.get()

    cursor.execute("INSERT INTO Labels (label) VALUES (?)", (name,))
    db.commit()
    
    addlab.destroy()


def addsavings():
    global addsav, sav_value
    addsav = Toplevel()
    addsav.title("Add Savings")
    
    label1 = Frame(addsav)
    label1.pack(padx=20, pady=20)
    
    label_prompt = Label(label1, text="Add Savings up to 1500:")
    label_prompt.grid(row=0, column=0, padx=5, pady=5)
    
    sav_value = DoubleVar()
    spinbox = Spinbox(label1, from_=0.0, to=1500.0, increment=0.1, textvariable=sav_value)
    spinbox.grid(row=1, column=0, padx=5, pady=10, sticky="w")
    
    submit_button = Button(label1, text="Submit", command=addsavtodb, bg="green", fg="white")
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    addsav.mainloop()

def addsavtodb():
    savings = sav_value.get()

    cursor.execute("INSERT INTO Savings(month, ammount, year) VALUES(?,?,?)",(month, savings, year))
    db.commit()
    addsav.destroy()

def get_espences():
    labels = []
    cursor.execute("SELECT label FROM Labels")

    for item in cursor.fetchall():
        labels.append(item)
    
    return labels


def get_income_ID(label, month):
    cursor.execute("SELECT id FROM Income WHERE label=? AND month = ? ",(label,month))

    # fetch the row from the result set
    row = cursor.fetchone()

    # check if the row was found
    if row:
        return row[0] # returns the ID (which is the first column in the result row)
    else:
        return None

with sqlite3.connect("data.db") as db:
    cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Income(
               id integer PRIMARY KEY AUTOINCREMENT,
               label text NOT NULL,
               month integer NOT NULL,
               year integer NOT NULL,
               ammount float NOT NULL);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Savings(
               id integer PRIMARY KEY AUTOINCREMENT,
               label text DEFAULT 'Saved',
               month integer NOT NULL,
               year integer NOT NULL,
               ammount float NOT NULL);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Expences(
               id integer PRIMARY KEY AUTOINCREMENT,
               label text NOT NULL,
               month integer NOT NULL,
               ammount float NOT NULL,
               link_to_income integer NOT NULL);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Labels(
               id integer PRIMARY KEY AUTOINCREMENT,
               label text NOT NULL);""")

