
import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

class NewReservationWindow:
    def __init__(self, window, conn):
        self.window = window
        self.conn = conn
        self.window.title("New Reservation")
        self.window.geometry("400x400")

        # Title
        title_label = tk.Label(window, text='New Reservation', font=('bold'))
        title_label.grid(row=0, column=1)

        type_label = tk.Label(self.window, text='Type:')
        type_label.grid(row=1, column=0)

        # Dropdown menu options
        self.type_options = [
            "Compact",
            "Medium",
            "Large",
            "SUV",
            "Truck",
            "Van",
        ]

        type_v = tk.StringVar()
        type_v.set(self.type_options[0])

        # Create Dropdown menu
        type_dropdown = tk.OptionMenu(self.window, type_v, *self.type_options)
        type_dropdown.grid(row=1, column=1)

        category_label = tk.Label(self.window, text='Category:')
        category_label.grid(row=2, column=0)

        # Dropdown menu options
        self.category_options = [
            "Basic",
            "Luxury"
        ]

        category_v = tk.StringVar()
        category_v.set(self.category_options[0])

        # Create Dropdown menu
        category_dropdown = tk.OptionMenu(self.window, category_v, *self.category_options)
        category_dropdown.grid(row=2, column=1)

        # Create Date Entry Fields
        # Date entry field
        tk.Label(self.window, text='Date:').grid(row=3, column=0)

        # Start Date
        # Update function for startdate
        # Changes mindate on end date calendar
        sel = tk.StringVar()
        def min_end_date_upd(*args):
            date = sel.get()
            if (len(date) > 3):  # Date selected
                calendar_end.config(mindate=datetime.strptime(date,'%m/%d/%y'))

        calendar_start = DateEntry(self.window, selectmode='day',textvariable=sel)
        calendar_start.grid(row=3, column=1)

        tk.Label(self.window, text=' - ').grid(row=3, column=2)

        # End Date
        calendar_end = DateEntry(self.window, selectmode='day')
        calendar_end.grid(row=3, column=4)

        sel.trace('w', min_end_date_upd)

    def close_window(self):
        self.window.destroy()
        self.window.update()


