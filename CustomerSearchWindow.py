
import tkinter as tk
from tkinter import ttk, messagebox


class CustomerSearchWindow:
    def __init__(self, window, conn):
        self.window = window
        self.conn = conn
        self.window.title("User Search")
        self.window.geometry("400x400")

        # Container for entry fields
        entry_container = tk.Frame(self.window, pady=5, height=10)
        entry_container.pack(side='top')

        # UID Entry
        tk.Label(entry_container, text='User ID:').grid(row=0, column=0, padx=5)
        uid_entry = tk.Entry(entry_container, width=15)
        uid_entry.grid(row=0, column=1, padx=5)

        # User Name Entry
        tk.Label(entry_container, text='User Name:').grid(row=1, column=0, padx=5)
        uname_entry = tk.Entry(entry_container, width=15)
        uname_entry.grid(row=1, column=1, padx=5)

        # Users Display List
        users_tv = ttk.Treeview(self.window, columns=('User ID', 'User Name', 'Remaining Balance'),
                                show='headings', selectmode='browse')
        users_tv.heading(0, text='User ID')
        users_tv.heading(1, text='User Name')
        users_tv.heading(2, text='Remaining Balance')
        users_tv.column(0, width=60)
        users_tv.column(1, width=170)
        users_tv.column(2, width=170)

        # Function for updating view
        def update_users_tv(users):
            if users is None:
                pass

            users_tv.delete(*users_tv.get_children())
            for i in enumerate(users):
                input_tuple = i[1]
                input_tuple = list(input_tuple)  # Convert tuple into a mutable list

                # Make total look like a dollar amount
                if input_tuple[2] is None:
                    input_tuple[2] = '$0'
                else:
                    input_tuple[2] = '$' + str(input_tuple[2])

                users_tv.insert(parent='', index=i[0], values=input_tuple)

        # Prevent tv headers from having their width changed manually
        def handle_click(event):
            if users_tv.identify_region(x=event.x, y=event.y) == "separator":
                return "break"

        users_tv.bind('<Button-1>', handle_click)

        # Scroll Bar
        tv_scroll = ttk.Scrollbar(self.window)
        tv_scroll.configure(command=users_tv.yview)
        users_tv.configure(yscrollcommand=tv_scroll.set)
        tv_scroll.pack(side='right', fill='y')

        users_tv.pack(side='left', expand=True, fill='both')

        # Search Button
        search_btn = tk.Button(entry_container,
                               text='Search',
                               command=lambda: update_users_tv(self.get_users(
                                   uid=uid_entry.get(), name=uname_entry.get()
                               )))
        search_btn.grid(row=0, column=3, rowspan=2)

    def get_users(self, uid, name):
        try:
            cursor = self.conn.cursor()

            if len(uid) > 0:  # Find users with uid matching
                cursor.execute('''
                SELECT CustomerID, CustomerName, SUM(RentalBalance)
                FROM vRentalInfo
                WHERE CustomerID = :uid
                GROUP BY CustomerID
                ORDER BY SUM(RentalBalance) DESC
                ''', {"uid": uid})
            elif len(name) > 0:  # Find users with name like
                cursor.execute('''
                SELECT CustomerID, CustomerName, SUM(RentalBalance)
                FROM vRentalInfo
                WHERE CustomerName LIKE :name
                GROUP BY CustomerID
                ORDER BY SUM(RentalBalance) DESC
                ''', {"name": '%' + name + '%'})
            else:  # Find all users
                cursor.execute('''
                SELECT CustomerID, CustomerName, SUM(RentalBalance)
                FROM vRentalInfo
                GROUP BY CustomerID
                ORDER BY SUM(RentalBalance) DESC
                ''')

            return cursor.fetchall()

        except Exception as ex:
            print("Error getting users: ", ex)
            messagebox.showinfo("Error", str(ex))
