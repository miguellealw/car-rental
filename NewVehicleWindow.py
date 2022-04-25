import tkinter as tk

class NewVehicleWindow:
  def __init__(self, window):
    self.window = window
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
    type_options = [
        "Compact",
        "Medium",
        "Large",
        "SUV",
        "Truck",
        "Van",
    ]

    type_v = tk.StringVar()
    type_v.set(type_options[0])
      
    # Create Dropdown menu
    type_dropdown = tk.OptionMenu(self.window , type_v, *type_options )
    type_dropdown.grid(row = 5, column = 1)


    category_label = tk.Label(self.window, text='Category:')
    category_label.grid(row=6, column=0)

    # Dropdown menu options
    category_options = [
      "Basic", 
      "Luxury"
    ]

    category_v = tk.StringVar()
    category_v.set(category_options[0])
      
    # Create Dropdown menu
    category_dropdown = tk.OptionMenu(self.window , category_v, *category_options )
    category_dropdown.grid(row = 6, column = 1)

    # Button
    add_vehicle_btn = tk.Button(self.window, text='Add Vehicle', command = self.add_vehicle)
    add_vehicle_btn.grid(row = 7, pady=5, column = 0, columnspan = 2)

  def add_vehicle(self):
    pass

  def close_window(window):
    window.destroy()
    window.update()