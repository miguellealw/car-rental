import tkinter as tk
from tkinter import messagebox, LEFT
from tkcalendar import DateEntry
from datetime import datetime

class ReturnRentalWindow:
  def __init__(self, window, conn):
    self.window = window
    self.conn = conn
    self.window.title("Return Vehicle")
    self.window.geometry("400x400")

    # Title
    title_label = tk.Label(self.window, text='Return Rental', font=('bold'))
    title_label.grid(row=0, column=1)

    # Return Date
    tk.Label(self.window, text='Rental Return Date:').grid(row=1, column=0)
    date_container = tk.Frame(self.window)
    date_container.grid(row=1, column=1)

    return_date = DateEntry(date_container, selectmode='day', mindate=datetime.now())
    return_date.pack(side=LEFT)

    # Vehicle ID
    customer_label = tk.Label(self.window, text='Customer ID:')
    customer_label.grid(row=2, column=0)
    customer_entry = tk.Entry(self.window, width=30)
    customer_entry.grid(row=2, column=1)

    # Vehicle ID
    id_label = tk.Label(self.window, text='Vehicle ID:')
    id_label.grid(row=3, column=0)
    id_entry = tk.Entry(self.window, width=30)
    id_entry.grid(row=3, column=1)

    return_rental_btn = tk.Button(
      self.window,
      text='Return Rental',
      command=lambda: self.return_rental(return_date.get(), id_entry.get(), customer_entry.get())
    )
    return_rental_btn.grid(row=7, pady=5, column=0, columnspan=2)

  def return_rental(self, return_date, vehicle_id, customer_id):
    # TODO: validate input

    try:
      # create cursor (help create tables, perform queries, etc.)
      cursor = self.conn.cursor()

      '''
      cursor.execute("""
        INSERT INTO VEHICLE (
          VehicleID, 
          Description, 
          Year, 
          Type, 
          Category
        ) VALUES (:vehicle_id, :description, :year, :type, :category);
      """, {
        "vehicle_id": vehicle_id,
        "description": description,
        "year": year,
        "type": type_number,
        "category": category_number,
      })
      '''

      # Set remaining_balance to the cost after the payment is made
      remaining_balance = 52
      self.conn.commit()
      messagebox.showinfo("Rental Returned", "Rental Returned Successfully! \nRemaining balance: "+str(remaining_balance))
      self.close_window()

    except Exception as ex:
      print("Error returning rental", ex)

  def get_index(list, value):
    pass

  def close_window(self):
    self.window.destroy()
    self.window.update()