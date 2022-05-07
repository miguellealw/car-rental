import tkinter as tk
from tkinter import messagebox

class NewVehicleWindow:
  def __init__(self, window, conn):
    self.window = window
    self.conn = conn
    self.window.title("New Vehicle")
    self.window.geometry("400x400")

    """
    
    * Add car info
      *	VEHICLE ID
      * Descriptoin
      * Year
      * Type
      * Category
    
    """

    # Title
    title_label = tk.Label(self.window, text='New Vehicle', font=('bold'))
    title_label.grid(row=0, column=1)

    # Input Entries
    id_label = tk.Label(self.window, text='Vehicle ID:')
    id_label.grid(row=1, column=0)
    id_entry = tk.Entry(self.window, width=30)
    id_entry.grid(row = 1, column=1)

    desc_label = tk.Label(self.window, text='Description:')
    desc_label.grid(row=3, column=0)
    desc_entry = tk.Entry(self.window, width=30)
    desc_entry.grid(row = 3, column=1)

    year_label = tk.Label(self.window, text='Year:')
    year_label.grid(row=4, column=0)
    year_entry = tk.Entry(self.window, width=30)
    year_entry.grid(row = 4, column=1)


    type_label = tk.Label(self.window, text='Type:')
    type_label.grid(row=5, column=0)

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
    type_dropdown = tk.OptionMenu(self.window , type_v, *self.type_options )
    type_dropdown.grid(row = 5, column = 1)


    category_label = tk.Label(self.window, text='Category:')
    category_label.grid(row=6, column=0)

    # Dropdown menu options
    self.category_options = [
      "Basic", 
      "Luxury"
    ]

    category_v = tk.StringVar()
    category_v.set(self.category_options[0])
      
    # Create Dropdown menu
    category_dropdown = tk.OptionMenu(self.window , category_v, *self.category_options )
    category_dropdown.grid(row = 6, column = 1)

    add_vehicle_btn = tk.Button(
      self.window, 
      text='Add Vehicle', 
      command = lambda: self.add_vehicle(id_entry.get(), desc_entry.get(), year_entry.get(), type_v.get(), category_v.get())
    )
    add_vehicle_btn.grid(row = 7, pady=5, column = 0, columnspan = 2)

  def add_vehicle(self, vehicle_id, description, year, type, category):
    type_number = 1 + int(self.type_options.index( type ))
    category_number = int(self.category_options.index( category ))


    # TODO: validate input

    try:
      # create cursor (help create tables, perform queries, etc.)
      cursor = self.conn.cursor()

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

      self.conn.commit()
      messagebox.showinfo("New Vehicle Added", "Vehicle Added Successfully!")
      self.close_window()

    except Exception as ex:
      print("Error adding vehicle", ex)

  def close_window(self):
    self.window.destroy()
    self.window.update()