from graphs import Graph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as GraphLink
import mplcursors
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime



current_time = datetime.date.today()
defyear = current_time.year

with sqlite3.connect("data.db") as db:
    cursor = db.cursor()


def view_data(): #the main window for seeing the data
    global viewin, monthOption, yearOption, monthOptionEX, yearOptionEX, menuGraphIn, menuGraphEX

    viewin = Toplevel()
    window_height = 346
    window_width = 220
    viewin.title("Displaying the data in a visual way")
    viewin.geometry(f"{window_height}x{window_width}")

    income_label = ttk.LabelFrame(viewin, text="Income")
    income_label.grid(row=0, column=0,  padx= 5, pady=5)
 
 # the combobox meniu for choosing the month
    monthOption = StringVar()
    months = get_months()

    if not months:
        months = ["No months found"]

    combobox = ttk.Combobox(income_label, values=months, textvariable= monthOption)
    combobox.grid(row=0, column=0, pady=10, sticky="n")    

    # the combobox meniu for choosing the year
    yearOption = StringVar()
    years = get_year()

    if not years:
        years = ["No year found"]

    combobox2 = ttk.Combobox(income_label, values=years, textvariable= yearOption)
    combobox2.grid(row=2, column=0, pady=10, padx=10, sticky="n")
    combobox2.insert(0,defyear)
    
    menuGraphIn = StringVar()
    options = ['line plot', 'scatter plot', 'bar plot']
    menuGraphIn.set("Choose a graph type")
    menu = ttk.Combobox(income_label,values=options,textvariable=menuGraphIn)
    menu.grid(row=3, column=0, pady=10, padx=10, sticky="n")

    Button(income_label,text="Generate", command=income_graph).grid(row=4, column=0, pady=10, padx=10, sticky="w") # put a function here based on the menuGraphIn option
    Button(income_label,text="Reset", command=lambda:clear_canvas(fig, canvas,list1, graph_label,income_shit)).grid(row=4, column=0, pady=10, padx=10, sticky="e") # put a function here based on the menuGraphIn option

# the expence part
    expence_label = ttk.LabelFrame(viewin, text="Expenses")
    expence_label.grid(row=0, column=1,  padx= 5, pady=5)

    monthOptionEX = StringVar()
    months = get_months()

    if not months:
        months = ["No months found"]

    combobox3 = ttk.Combobox(expence_label, values=months, textvariable= monthOptionEX)
    combobox3.grid(row=0, column=0, columnspan=4, pady=10, sticky="n")    

    # the combobox meniu for choosing the year
    yearOptionEX = StringVar()
    years = get_year()

    if not years:
        years = ["No year found"]

    combobox4 = ttk.Combobox(expence_label, values=years, textvariable= yearOptionEX)
    combobox4.grid(row=1, column=0, pady=10, padx=10, sticky="s")
    combobox4.insert(0,"Not in use yet!!")

    menuGraphEX = StringVar()
    options = ['line plot', 'scatter plot', 'bar plot', 'pie chart']
    menuGraphEX.set("Choose a graph type")
    menu = ttk.Combobox(expence_label,values=options,textvariable=menuGraphEX)
    menu.grid(row=3, column=0, pady=10, padx=10, sticky="n")

    Button(expence_label,text="Generate", command=expense_graph).grid(row=4, column=0, pady=10, padx=10, sticky="w") 

    Button(expence_label,text="Reset", command=lambda:clear_canvas(fig2, canvas2 ,list2, expense_label,expense_shit)).grid(row=4, column=0, pady=10, padx=10, sticky="e")

    viewin.mainloop()


def income_graph():
    global fig, canvas,list1, graph_label, income_shit
    graph = Graph()
    income_shit = Toplevel()

    month = monthOption.get()
    year = yearOption.get()
    graph_type = menuGraphIn.get()
    labels,ammount, total_income_of_the_month = get_total_income(month, year)

    graph_label = ttk.LabelFrame(income_shit, text="Graph view")
    graph_label.grid(row=1, column=0)
    
    if graph_type == 'line plot':

        fig = graph.line_plot(labels,ammount)
        fig.set_size_inches(4,4)

        canvas = GraphLink(fig, master=graph_label)
        canvas.get_tk_widget().grid(row=0, column=0, pady=10)

        list1= Listbox(graph_label, width=32)
        list1.grid(row=0, column=1, pady=10, sticky="n")

        list1.delete(0, END)
        list1.insert(0, "Income list:")
        list1.insert(1,f"Total income for the month: {total_income_of_the_month}")
        list1.insert(2, "-" * 32)
        for i, (ammount, label) in enumerate(zip(ammount, labels), start=3):
            list1.insert(i, f"{label} -> {ammount}")

        canvas.draw()

    if graph_type == 'scatter plot':

        fig = graph.scatter_plot(labels,ammount)
        fig.set_size_inches(4,4)

        canvas = GraphLink(fig, master=graph_label)
        canvas.get_tk_widget().grid(row=0, column=0, pady=10)

        list1= Listbox(graph_label, width=32)
        list1.grid(row=0, column=1, pady=10, sticky="n")

        list1.delete(0, END)
        list1.insert(0, "Income list:")
        list1.insert(1,f"Total income for the month: {total_income_of_the_month}")
        list1.insert(2, "-" * 32)
        for i, (ammount, label) in enumerate(zip(ammount, labels), start=3):
            list1.insert(i, f"{label} -> {ammount}")

        canvas.draw()

    if graph_type == 'bar plot':
        fig = graph.bar_plot(labels,ammount)
        fig.set_size_inches(4,4)

        canvas = GraphLink(fig, master=graph_label)
        canvas.get_tk_widget().grid(row=0, column=0, pady=10)

        list1= Listbox(graph_label, width=32)
        list1.grid(row=0, column=1, pady=10, sticky="n")

        list1.delete(0, END)
        list1.insert(0, "Income list:")
        list1.insert(1,f"Total income for the month: {total_income_of_the_month}")
        list1.insert(2, "-" * 32)
        for i, (ammount, label) in enumerate(zip(ammount, labels), start=3):
            list1.insert(i, f"{label} -> {ammount}")

        canvas.draw()


def expense_graph():
    global fig2, canvas2 ,list2, expense_label, expense_shit
    graph1 = Graph()
    expense_shit = Toplevel()

    month = monthOptionEX.get() 
    year = yearOptionEX.get()
    graph_type = menuGraphEX.get()

    labels, ammount, expences_for_the_month = get_expences_data(month)

    expense_label = ttk.LabelFrame(expense_shit, text="Expense view")
    expense_label.grid(row=1, column=0)

    if graph_type == 'line plot':
        fig2 = graph1.line_plot(labels,ammount)
        fig2.set_size_inches(4,4)

        canvas2 = GraphLink(fig2, master=expense_label)
        canvas2.get_tk_widget().grid(row=0, column=0, pady=10)

        list2= Listbox(expense_label, width=32)
        list2.grid(row=0, column=1, pady=10, sticky="n")
        
        list2.delete(0, END)
        list2.insert(0, "Income list:")
        list2.insert(1,f"Total income for the month: {expences_for_the_month}")
        list2.insert(2, "-" * 32)
        for i, (ammount, label) in enumerate(zip(ammount, labels), start=3):
            list2.insert(i, f"{label} -> {ammount}")

        canvas2.draw()

    if graph_type == 'scatter plot':
        fig2 = graph1.scatter_plot(labels,ammount)
        fig2.set_size_inches(4,4)

        canvas2 = GraphLink(fig2, master=expense_label)
        canvas2.get_tk_widget().grid(row=0, column=0, pady=10)

        list2= Listbox(expense_label, width=32)
        list2.grid(row=0, column=1, pady=10, sticky="n")
        
        list2.delete(0, END)
        list2.insert(0, "Income list:")
        list2.insert(1,f"Total income for the month: {expences_for_the_month}")
        list2.insert(2, "-" * 32)
        for i, (ammount, label) in enumerate(zip(ammount, labels), start=3):
            list2.insert(i, f"{label} -> {ammount}")

        canvas2.draw()

    if graph_type == 'bar plot':
        fig2 = graph1.bar_plot(labels,ammount)
        fig2.set_size_inches(4,4)

        canvas2 = GraphLink(fig2, master=expense_label)
        canvas2.get_tk_widget().grid(row=0, column=0, pady=10)

        list2= Listbox(expense_label, width=32)
        list2.grid(row=0, column=1, pady=10, sticky="n")
        
        list2.delete(0, END)
        list2.insert(0, "Income list:")
        list2.insert(1,f"Total income for the month: {expences_for_the_month}")
        list2.insert(2, "-" * 32)
        for i, (ammount, label) in enumerate(zip(ammount, labels), start=3):
            list2.insert(i, f"{label} -> {ammount}")

        canvas2.draw()

    if graph_type == 'pie chart':
        fig2 = graph1.pie_chart(labels,ammount)
        fig2.set_size_inches(4,4)

        canvas2 = GraphLink(fig2, master=expense_label)
        canvas2.get_tk_widget().grid(row=0, column=0, pady=10)

        list2= Listbox(expense_label, width=32)
        list2.grid(row=0, column=1, pady=10, sticky="n")
        
        list2.delete(0, END)
        list2.insert(0, "Income list:")
        list2.insert(1,f"Total income for the month: {expences_for_the_month}")
        list2.insert(2, "-" * 32)
        for i, (ammount, label) in enumerate(zip(ammount, labels), start=3):
            list2.insert(i, f"{label} -> {ammount}")

        canvas2.draw()

     
def clear_canvas(fig,canvas,listb, label, master):

    for ax in fig.axes:
        ax.clear()
    
    canvas.get_tk_widget().destroy()  # Destroy the canvas widget
    listb.delete(0,END)
    listb.destroy()
    label.destroy()
    master.destroy()


def get_total_income(month, year):
    ammount = []
    labels = []
    cursor.execute("SELECT label, ammount FROM Income WHERE month =? AND year=?",(month, year))

    # fetch the row from the result set
    row = cursor.fetchall()

    for item in row:
        labels.append(item[0])
        ammount.append(item[1])
    
    total_income_of_the_month = sum(ammount)
    return labels,ammount, total_income_of_the_month


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

