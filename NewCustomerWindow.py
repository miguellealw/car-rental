
import tkinter as tk
import sqlite3
from tkinter import messagebox

class NewCustomerWindow:
  def __init__(self, window, conn):
      self.window = window
      self.conn = conn
      self.window.title("New Customer")
      self.window.geometry("400x400")

      # Title
      title_label = tk.Label(window, text='New Customer', font=('bold'))
      title_label.grid(row=0, column=1)

      # Input Entries
      name_label = tk.Label(window, text='Customer Name:')
      name_label.grid(row=1, column=0)
      name_entry = tk.Entry(window, width=30)
      name_entry.grid(row = 1, column=1)

      phone_label = tk.Label(window, text='Customer Phone:')
      phone_label.grid(row=3, column=0)
      phone_entry = tk.Entry(window, width=30)
      phone_entry.grid(row = 3, column=1)

      # Button
      add_customer_btn = tk.Button(
        window, 
        text='Add Customer', 
        command = lambda: self.add_customer( name_entry.get(), phone_entry.get() )
      )
      add_customer_btn.grid(row = 5, pady=5, column = 0, columnspan = 2)

  def add_customer(self, name, phone):
    # TODO: validate input

    try:
      # create cursor (help create tables, perform queries, etc.)
      cursor = self.conn.cursor()

      cursor.execute("""
        INSERT INTO CUSTOMER (Name, Phone) VALUES (:name, :phone);
      """, {
        "name": name,
        "phone": phone,
      })

      self.conn.commit()
      messagebox.showinfo("New Customer Created", "Customer Added Successfully!")
      self.close_window()

    except Exception as ex:
      print("Error creating customer", ex)

  def close_window(self):
    self.window.destroy()
    self.window.update()