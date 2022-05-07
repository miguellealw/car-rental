import tkinter as tk
import sqlite3
from tkinter import messagebox


"""
a. List for every customer the ID, name, and if there is any remaining balance. The user has the
right to search either by a customer’s ID, name, part of the name, or to run the query with no
filters/criteria. The amount needs to be in US dollars. For customers with zero (0) or NULL
balance, you need to return zero dollars ($0.00). Make sure that your query returns
meaningful attribute names. In the case that the user decides not to provide any filters, order
the results based on the balance amount. Make sure that you return all records. Submit your
editable SQL query that your code executes

b. List for every vehicle the VIN, the description, and the average DAILY price. The user has
the right either to search by the VIN, vehicle’s description, part of the description, or to run
the query with no filters/criteria. An example criterion would be all ‘BMW’ vehicles. The
amount needs to be in US dollars. The average DAILY price derives from the rental table,
and the amount needs to have two decimals as well as the dollar ‘$’ sign. For vehicles that
they do not have any rentals, you need to substitute the NULL value with a ‘Non-Applicable’
text. Make sure that your query returns meaningful attribute names. In the case that the user
decides not to provide any filters, order the results based on the average daily price. Submit
your editable SQL query that your code executes. 
"""

class SearchRentalsWindow:
  def __init__(self, window, conn):
      self.window = window
      self.conn = conn
      self.window.title("Rentals")
      self.window.geometry("600x400")

      # Title
      title_label = tk.Label(window, text='Search Rentals', font=('bold'))
      title_label.grid(row=0, column=1)

      # Input Entries
      name_label = tk.Label(window, text='Customer ID:')
      name_label.grid(row=1, column=0)
      name_entry = tk.Entry(window, width=30)
      name_entry.grid(row = 1, column=1)

      phone_label = tk.Label(window, text='Vehicle VIN:')
      phone_label.grid(row=1, column=3)
      phone_entry = tk.Entry(window, width=30)
      phone_entry.grid(row = 1, column=4)

      # Button
      search_btn = tk.Button(
        window, 
        text='Search', 
        command = lambda: self.search()
      )
      search_btn.grid(row = 5, pady=5, column = 0, columnspan = 2)

  def search():
    pass

  def close_window(self):
    self.window.destroy()
    self.window.update()