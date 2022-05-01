
import tkinter as tk
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
from math import floor


class NewReservationWindow:
    def __init__(self, window, conn):
        self.window = window
        self.conn = conn
        self.window.title("New Reservation")
        self.window.geometry("600x400")

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

        # Rental Type picker
        rental_type_container = tk.Frame(self.window)
        rental_type_container.grid(row=1, column=2)
        rental_type_v = tk.IntVar(value=1)
        rental_type_daily = tk.Radiobutton(rental_type_container, text='Daily', width=10,
                                           variable=rental_type_v, value=1)
        rental_type_weekly = tk.Radiobutton(rental_type_container, text='Weekly', width=10,
                                            variable=rental_type_v, value=7)
        rental_type_daily.grid(row=0, column=1)
        rental_type_weekly.grid(row=1, column=1)
        tk.Label(rental_type_container, text='Type:').grid(row=0, column=0, rowspan=2)

        # CID Enter
        cid_container = tk.Frame(self.window)
        cid_container.grid(row=2, column=2)
        tk.Label(cid_container, text='Customer ID:').grid(row=0, column=0)
        cid_entry = tk.Entry(cid_container, width=10)
        cid_entry.grid(row=0, column=1)

        # Date entry container
        tk.Label(self.window, text='Date:').grid(row=3, column=0)
        date_container = tk.Frame(self.window)
        date_container.grid(row=3, column=1, columnspan=2)

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
        unreserved_cars = ttk.Treeview(window, height=10,
                                       columns=("VIN", "Vehicle Description", "Daily Rate", "Weekly Rate"),
                                       show='headings')
        unreserved_cars.grid(row=5, column=0, columnspan=3)
        unreserved_cars.heading(0, text="VIN")
        unreserved_cars.heading(1, text="Vehicle Description")
        unreserved_cars.heading(2, text="Daily Rate")
        unreserved_cars.heading(3, text="Weekly Rate")
        unreserved_cars.column(0, width=150)
        unreserved_cars.column(1, width=150)
        unreserved_cars.column(2, width=150)
        unreserved_cars.column(3, width=150)

        def update_cars(available_cars):
            # TODO: Check input
            unreserved_cars.delete(*unreserved_cars.get_children())
            for i in enumerate(available_cars):
                unreserved_cars.insert(parent='', index=i[0], text='', values=i[1])

        # Find vehicles button
        find_vehicles_button = tk.Button(
            window,
            text='Find Vehicle',
            command=lambda: update_cars(self.get_unreserved_vehicles(type_v.get(),
                                                                     category_v.get(),
                                                                     calendar_start.get_date(),
                                                                     calendar_end.get_date()))
        )
        find_vehicles_button.grid(row=4, pady=5, column=0)

        # Reserve vehicle button
        reserve_vehicle_button = tk.Button(
            window,
            text='Reserve',
            command=lambda: (self.reserve_vehicle(cid_entry.get(),
                             unreserved_cars.item(unreserved_cars.focus(), 'values'),
                             calendar_start.get_date(),
                             calendar_end.get_date(),
                             rental_type_v.get()),
            update_cars(self.get_unreserved_vehicles(type_v.get(),
                        category_v.get(),
                        calendar_start.get_date(),
                        calendar_end.get_date())))
        )
        reserve_vehicle_button.grid(row=4, pady=5, column=2)

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
            SELECT v.VehicleID, v.Description, r.Daily, r.Weekly
            FROM VEHICLE v JOIN RATE r ON v.Type = r.Type AND v.Category = r.Category
            WHERE v.Type = ? AND V.Category = ? AND
            v.VehicleID NOT IN (
            WITH dates AS (SELECT ? AS start_date, ? AS end_date)
            SELECT r.VehicleID
            FROM RENTAL r, dates
            WHERE 
            ((r.StartDate BETWEEN dates.start_date AND dates.end_date) OR
            (r.ReturnDate BETWEEN dates.start_date AND dates.end_date) OR
            (r.StartDate <= dates.Start_date AND (r.ReturnDate) >= dates.end_date)) 
            AND r.Returned = 0
            )""", (type_number, category_number, start_date, end_date))

            return cursor.fetchall()
        except Exception as ex:
            print("Error finding vehicles: ", ex)

    def reserve_vehicle(self, custid, selected_vehicle, start_date, end_date, rental_type):
        # TODO: Check for valid input
        try:
            if not custid.isnumeric():  # Checks if custID is numeric, but NOT if it exists
                raise Exception("Invalid customer ID: Customer ID is not numeric or is empty.")

            vin = selected_vehicle[0]
            cursor = self.conn.cursor()

            qty = floor((end_date - start_date).days/rental_type) + 1
            # end_date is assumed to be the end of the day, and start_date the start
            # so end_date - start_date is 1 less than it should be, ergo 1 is added
            order_date = date.today()

            # Query Rate to ensure most up-to-date total
            if rental_type == 1:
                cursor.execute("""
                SELECT r.Daily 
                FROM RATE r JOIN VEHICLE v ON r.Type = v.Type AND r.Category = V.Category 
                WHERE v.VehicleID = :vin""", {"vin": vin})
            elif rental_type == 7:
                cursor.execute("""
                SELECT r.Weekly 
                FROM RATE r JOIN VEHICLE v ON r.Type = v.Type AND r.Category = V.Category 
                WHERE v.VehicleID = :vin""", {"vin": vin})
            else:  # Rental type is checked here
                raise Exception("Unrecognized rental type.")

            # Calculating the total amount this way is kind of idiotic
            total_amount = cursor.fetchall()
            total_amount = total_amount[0][0] * qty

            # Have to subtract 1 here for a similar reason as above

            print("Adding reservation: " + str((custid, vin, start_date, order_date,
                                                qty, end_date, total_amount)))
            cursor.execute("""
            INSERT INTO RENTAL (
                CustID,
                VehicleID,
                StartDate,
                OrderDate,
                RentalType,
                Qty,
                ReturnDate,
                TotalAmount,
                Returned
            ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, 0 )
            """, (custid, vin, start_date, order_date, rental_type, qty, end_date, total_amount))
            cursor.execute("""
            SELECT VehicleID, StartDate, OrderDate FROM RENTAL WHERE CustID = ? AND VehicleID = ?""",
                           (custid, vin))
            self.conn.commit()
            messagebox.showinfo("New Rental Added", "Vehicle Rented Successfully!")
        except Exception as ex:
            print("Error creating reservation: ", ex)
            messagebox.showinfo("Error", "Error creating reservation: " + str(ex))

    def close_window(self):
        self.window.destroy()
        self.window.update()


