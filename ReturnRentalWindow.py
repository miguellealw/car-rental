import tkinter as tk
from tkinter import ttk, messagebox, LEFT

from tkcalendar import DateEntry
from datetime import datetime


class ReturnRentalWindow:
    def __init__(self, window, conn):
        self.window = window
        self.conn = conn
        self.window.title("Return Vehicle")
        self.window.geometry("600x600")

        # Title
        title_label = tk.Label(self.window, text='Return Rental', font=('bold'))
        title_label.grid(row=0, column=1)

        '''
        # Return Date
        tk.Label(self.window, text='Rental Return Date:').grid(row=1, column=0)
        date_container = tk.Frame(self.window)
        date_container.grid(row=1, column=1)

        return_date = DateEntry(date_container, selectmode='day')
        return_date.pack(side=LEFT)
        '''

        # Customer Name
        customer_label = tk.Label(self.window, text='Customer Name:')
        customer_label.grid(row=2, column=0)
        customer_entry = tk.Entry(self.window, width=30)
        customer_entry.grid(row=2, column=1)

        # Vehicle Make and Model
        id_label = tk.Label(self.window, text='Vehicle Make and Model:')
        id_label.grid(row=3, column=0)
        v_description = tk.Entry(self.window, width=30)
        v_description.grid(row=3, column=1)

        '''
        # She does not want a drop down like this
        # Get our list of Makes/Models
        select_descriptions = "SELECT Description FROM VEHICLE GROUP BY Description"
        conn = self.conn.cursor()
        conn.execute(select_descriptions)
        options = conn.fetchall()
        print(options)
    
        # Create Dropdown menu using our options
        category_v = tk.StringVar()
        category_v.set(options[0])
        category_dropdown = tk.OptionMenu(self.window, category_v, *options)
        category_dropdown.grid(row=5, column=1)
        '''

        select_descriptions = "SELECT c.Name, v.Description, c.CustID, v.VehicleID FROM VEHICLE v, CUSTOMER c, RENTAL r WHERE r.CustID = c.CustID AND r.VehicleID = v.VehicleID AND r.Returned = 0"
        # select_descriptions = "SELECT Returned FROM RENTAL"
        conn = self.conn.cursor()
        conn.execute(select_descriptions)
        options = conn.fetchall()
        print(options)

        # Cars available for reservation
        rented_cars = ttk.Treeview(window, height=10,
                                   columns=("VIN", "Vehicle Description", "Daily Rate", "Weekly Rate"),
                                   show='headings')
        rented_cars.grid(row=5, column=0, columnspan=3)
        rented_cars.heading(0, text="VIN")
        rented_cars.heading(1, text="Vehicle Description")
        rented_cars.heading(2, text="Daily Rate")
        rented_cars.heading(3, text="Weekly Rate")
        rented_cars.column(0, width=150)
        rented_cars.column(1, width=150)
        rented_cars.column(2, width=150)
        rented_cars.column(3, width=150)

        def display_rentals(available_cars):
            # TODO: Check input
            if available_cars != -1:
                rented_cars.delete(*rented_cars.get_children())
                for i in enumerate(available_cars):
                    rented_cars.insert(parent='', index=i[0], text='', values=i[1])

        find_rental_btn = tk.Button(
            self.window,
            text='Find Rentals',
            command=lambda: display_rentals(self.get_rentals(v_description.get(), customer_entry.get()))
        )
        find_rental_btn.grid(row=7, pady=5, column=0, columnspan=2)

        return_rental_button = tk.Button(
            self.window,
            text='Return Selected Rental',
            # command=lambda: display_rentals(self.return_rental(customer_entry.get(),
            #                                                   rented_cars.item(rented_cars.focus(), 'values')))
            command=lambda: self.return_rental(customer_entry.get(), rented_cars.item(rented_cars.focus(), 'values'))
        )
        return_rental_button.grid(row=7, pady=5, column=1, columnspan=2)

    def get_rentals(self, v_description, customer_entry):
        # TODO: validate input
        try:
            # create cursor (help create tables, perform queries, etc.)
            cursor = self.conn.cursor()

            # Find cars that match the vehicle description and are rented by our current customer
            # For every rental needs to check if:
            #   1) Customer Name matches our input
            #   2) Vehicle Description matches our input

            '''
            cursor.execute("""
            SELECT v.VehicleID, v.Description, ra.Daily, ra.Weekly
            FROM RENTAL r, CUSTOMER c, VEHICLE v, RATE ra
            WHERE c.Name = :cust_name AND r.CustID = c.CustID AND v.VehicleID = r.VehicleID AND r.Returned = 0
            AND v.Type = ra.Type AND v.Category = ra.Category
            AND v.Description = :v_description
            """, {
                "v_description": v_description,
                "cust_name": customer_entry,
            })
            '''

            cursor.execute("""
                        SELECT v.VehicleID, v.Description, ra.Daily, ra.Weekly
                        FROM VEHICLE v, CUSTOMER c, RENTAL r, RATE ra
                        WHERE r.CustID = c.CustID AND r.VehicleID = v.VehicleID
                        AND ra.Type = v.Type AND ra.Category = v.Category
                        AND v.Description = ? AND c.Name = ?
                        """, (v_description, customer_entry))

            return cursor.fetchall()
        except Exception as ex:
            print("Error finding vehicles: ", ex)

    def return_rental(self, customer_entry, selected_vehicle):
        # TODO: validate input

        if selected_vehicle:
            try:
                # create cursor (help create tables, perform queries, etc.)
                cursor = self.conn.cursor()
                vin = str(selected_vehicle[0])
                print(vin)
                date = datetime.now()
                
                cursor.execute("""
                            UPDATE RENTAL
                            SET ReturnDate = ?, PaymentDate = ?, RETURNED = 1, TotalAmount = 0
                            WHERE CustID = ? AND VehicleID = ?
                            """, (date, date, customer_entry, vin))
                
                cursor.execute("""
                            SELECT TotalAmount
                            FROM VEHICLE v, CUSTOMER c, RENTAL r, RATE ra
                            WHERE r.CustID = c.CustID AND r.VehicleID = v.VehicleID
                            AND ra.Type = v.Type AND ra.Category = v.Category
                            AND v.VehicleID = ? AND c.Name = ?
                            """, (vin, customer_entry))

                remaining_balance = cursor.fetchone()
                remaining_balance = str(remaining_balance)[1:len(str(remaining_balance)) - 2]

                cursor.execute("""
                            UPDATE RENTAL
                            SET Returned = 1, TotalAmount = 0
                            WHERE VehicleID = :vin
                            """, {"vin": vin})

                # Set remaining_balance to the cost after the payment is made
                self.conn.commit()
                messagebox.showinfo("Rental Returned",
                                    "Rental Returned Successfully! \nRemaining balance: " + str(remaining_balance))
                self.close_window()
                # return remaining_balance

            except Exception as ex:
                print("Error returning rental", ex)
        else:
            messagebox.showinfo("No Vehicle Selected",
                                "Please select a vehicle and try again")
            return -1

    def get_index(list, value):
        pass

    def close_window(self):
        self.window.destroy()
        self.window.update()
