from tkinter import *
from add_data import *
from view_data import *

 
window = Tk()   

screen_width = 300
screen_height = 400
window.geometry(f"{screen_width}x{screen_height}")
window.title("Monthly finance tracker")
window.configure(background="black")

Button(window, text="Add income/expences", command=add_data, bg="blue", fg="white").pack(pady=(150, 0))
Button(window, text="View statistics", command=view_data, bg="green", fg="white").pack()
Button(window, text="Exit", command=window.destroy, bg="red", fg="white").pack()

window.mainloop()