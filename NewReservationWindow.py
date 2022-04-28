
import tkinter as tk
import sqlite3
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime


class NewReservationWindow:
    def __init__(self, window, conn):
        self.window = window
        self.conn = conn
        self.window.title("New Reservation")
        self.window.geometry("400x400")

        # Title
        title_label = tk.Label(window, text='New Reservation', font='bold')
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
            if len(date) > 3:  # Date selected
                date = datetime.strptime(date, '%m/%d/%y')
                calendar_end.config(mindate=date)
                calendar_end.set_date(date)

        calendar_start = DateEntry(date_container, selectmode='day', mindate=datetime.now(), textvariable=sel)
        calendar_start.pack(side=LEFT)

        tk.Label(date_container, text=' - ').pack(side=LEFT)

        # End Date
        calendar_end = DateEntry(date_container, selectmode='day', mindate=datetime.now())
        calendar_end.pack(side=LEFT)

        sel.trace('w', min_end_date_upd)

        # Cars available for reservation
        unreserved_cars = ttk.Treeview(window, height=10, columns=("VIN", "Vehicle Description"), show='headings')
        unreserved_cars.grid(row=5, column=0, columnspan=2)
        unreserved_cars.heading(0, text="VIN")
        unreserved_cars.heading(1, text="Vehicle Description")

        def update_cars(available_cars):
            # TODO: Check input
            unreserved_cars.delete(*unreserved_cars.get_children())
            for i in enumerate(available_cars):
                unreserved_cars.insert(parent='', index=i[0], text='', values=i[1])

        # Find vehicles button
        find_vehicles_button = tk.Button(
            window,
            text='Find Vehicle',
            command=lambda: update_cars(self.get_unreserved_vehicles(type_v.get(), category_v.get(), calendar_start.get_date(), calendar_end.get_date()))
        )
        find_vehicles_button.grid(row=4, pady=5, column=0, columnspan=2)

    def get_unreserved_vehicles(self, vehicle_type, vehicle_category, start_date, end_date):
        # TODO: validate input
        type_number = 1 + int(self.type_options.index(vehicle_type))
        category_number = int(self.category_options.index(vehicle_category))
        try:
            # create cursor (help create tables, perform queries, etc.)
            cursor = self.conn.cursor()

            # Find cars that do not have a reservation8 within the time period
            # For every rental needs to check if:
            #   1) Rental start date not within given dates
            #   2) Rental end date not within given dates
            #   3) Rental start date not before given start date and rental end date not after given end date

            cursor.execute("""
            SELECT v.VehicleID, v.Description
            FROM VEHICLE v
            WHERE v.Type = ? AND V.Category = ? AND
            v.VehicleID NOT IN (
            WITH dates AS (SELECT ? AS start_date, ? AS end_date)
            SELECT r.VehicleID
            FROM RENTAL r, dates
            WHERE 
            (r.StartDate BETWEEN dates.start_date AND dates.end_date) OR
            (r.ReturnDate BETWEEN dates.start_date AND dates.end_date) OR
            (r.StartDate <= dates.Start_date AND r.ReturnDate >= dates.end_date)
            )""", (type_number, category_number, start_date, end_date))

            return cursor.fetchall()

        except Exception as ex:
            print("Error creating reservation: ", ex)

    def close_window(self):
        self.window.destroy()
        self.window.update()


