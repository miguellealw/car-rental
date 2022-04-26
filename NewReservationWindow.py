
import tkinter as tk
import sqlite3
from tkinter import *
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
        # Date entry container
        tk.Label(self.window, text='Date:').grid(row=3, column=0)
        date_container = tk.Frame(self.window)
        date_container.grid(row=3, column=1)

        # Start Date
        # Update function for startdate
        # Changes mindate on end date calendar
        sel = tk.StringVar()
        def min_end_date_upd(*args):
            date = sel.get()
            if (len(date) > 3):  # Date selected
                date = datetime.strptime(date,'%m/%d/%y')
                calendar_end.config(mindate=date)
                calendar_end.set_date(date)

        calendar_start = DateEntry(date_container, selectmode='day', textvariable=sel)
        calendar_start.pack(side=LEFT)

        tk.Label(date_container, text=' - ').pack(side=LEFT)

        # End Date
        calendar_end = DateEntry(date_container, selectmode='day', mindate=datetime.now())
        calendar_end.pack(side=LEFT)

        sel.trace('w', min_end_date_upd)

        # Confirm reservation button
        reservation_button =tk.Button(
            window,
            text='Reserve Vehicle',
            command=lambda: self.add_reservation(type_v.get(), category_v.get(), calendar_start.get_date(), calendar_end.get_date())
        )
        reservation_button.grid(row=4, pady=5, column=0, columnspan=2)


    def add_reservation(self, vehicle_type, vehicle_category, start_date, end_date):
        # TODO: validate input, do anything really

        try:
            # create cursor (help create tables, perform queries, etc.)
            cursor = self.conn.cursor()
            cursor.close()

        except Exception as ex:
            print("Error creating reservation: ", ex)

    def close_window(self):
        self.window.destroy()
        self.window.update()


