
import tkinter as tk
from tkinter import ttk, messagebox


class VehicleSearchWindow:
    def __init__(self, window, conn):
        self.window = window
        self.conn = conn
        self.window.title("Vehicle Search")
        self.window.geometry("400x400")

        # Container for entry fields
        entry_container = tk.Frame(self.window, pady=5, height=10)
        entry_container.pack(side='top')

        # VIN Entry
        tk.Label(entry_container, text='Vehicle ID Number:').grid(row=0, column=0, padx=5)
        vin_entry = tk.Entry(entry_container, width=15)
        vin_entry.grid(row=0, column=1, padx=5)

        # Vehcile Description Entry
        tk.Label(entry_container, text='Vehicle Description:').grid(row=1, column=0, padx=5)
        vdescription_entry = tk.Entry(entry_container, width=15)
        vdescription_entry.grid(row=1, column=1, padx=5)

        # Users Display List
        vehicles_tv = ttk.Treeview(self.window, columns=('User ID', 'User Name', 'Remaining Balance'),
                                show='headings', selectmode='browse')
        vehicles_tv.heading(0, text='Vehicle ID Number')
        vehicles_tv.heading(1, text='Vehicle Description')
        vehicles_tv.heading(2, text='Average Daily Price')
        vehicles_tv.column(0, width=130)
        vehicles_tv.column(1, width=130)
        vehicles_tv.column(2, width=60)

        # Function for updating view
        def update_vehicles_tv(vehicles):
            if vehicles is None:
                pass

            vehicles_tv.delete(*vehicles_tv.get_children())
            for i in enumerate(vehicles):
                input_tuple = i[1]
                input_tuple = list(input_tuple)  # Convert tuple into a mutable list

                # Make total look like a dollar amount
                if input_tuple[2] is None:
                    input_tuple[2] = '$0'
                else:
                    x = str(input_tuple[2]).index(".")
                    whole_number = str(input_tuple[2])
                    whole_number = whole_number[1:x+3]
                    input_tuple[2] = '$' + whole_number
                    # decimal = str(input_tuple[2])[x, x+2]
                    # input_tuple[2] = '$' + str(input_tuple[2])
                    # input_tuple[2] = '$' + whole_number

                vehicles_tv.insert(parent='', index=i[0], values=input_tuple)

        # Prevent tv headers from having their width changed manually
        def handle_click(event):
            if vehicles_tv.identify_region(x=event.x, y=event.y) == "separator":
                return "break"

        vehicles_tv.bind('<Button-1>', handle_click)

        # Scroll Bar
        tv_scroll = ttk.Scrollbar(self.window)
        tv_scroll.configure(command=vehicles_tv.yview)
        vehicles_tv.configure(yscrollcommand=tv_scroll.set)
        tv_scroll.pack(side='right', fill='y')

        vehicles_tv.pack(side='left', expand=True, fill='both')

        # Search Button
        search_btn = tk.Button(entry_container,
                               text='Search',
                               command=lambda: update_vehicles_tv(self.get_vehicles(
                                   vin=vin_entry.get(), description=vdescription_entry.get()
                               )))
        search_btn.grid(row=0, column=3, rowspan=2)

    def get_vehicles(self, vin, description):
        try:
            cursor = self.conn.cursor()

            if len(vin) > 0:  # Find vehicles with vin matching
                cursor.execute('''
                SELECT VIN, Vehicle, OrderAmount/TotalDays AS DailyAvg
                FROM vRentalInfo
                WHERE VIN = :vin
                GROUP BY VIN
                ORDER BY DailyAvg DESC
                ''', {"vin": vin})
            elif len(description) > 0:  # Find vehicles with description like
                cursor.execute('''
                SELECT VIN, Vehicle, OrderAmount/TotalDays AS DailyAvg
                FROM vRentalInfo
                WHERE Vehicle LIKE :description
                GROUP BY VIN
                ORDER BY DailyAvg DESC
                ''', {"description": '%' + description + '%'})
            else:  # Find all vehicles
                cursor.execute('''
                SELECT VIN, Vehicle, OrderAmount/TotalDays AS DailyAvg
                FROM vRentalInfo
                GROUP BY VIN
                ORDER BY DailyAvg DESC
                ''')

            return cursor.fetchall()

        except Exception as ex:
            print("Error getting vehicles: ", ex)
            messagebox.showinfo("Error", str(ex))
