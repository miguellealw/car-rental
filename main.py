"""
  Tkinter
"""

from tkinter import * 
from tkinter import messagebox
import sqlite3
from sql_startup import startup
from os.path import exists


try:

  # Connect to DB
  conn = sqlite3.connect('car_rental.db')
  print("Connected to DB successfully")

  cursor = conn.cursor()

  # only run startup script if the DB does not exist
  if not exists('./car_rental.db'):
    cursor.executescript(startup)
    print("Ran startup DB script successfully")
  else:
    print("DB already exists so the startup script did not run")

  conn.close()

except Exception as ep:
  print("Error connecting to DB", ep)
  conn.close()
finally:
  conn.close()



# create tkinter window

root = Tk()
root.title('Car Rental Dashboard')
# size of window
root.geometry("400x400")




# Functions that will submit queries
def submit():
  print("Submit button clicked")

def add_vehicle():
  pass

def open_add_vehicle_window():
  window = Toplevel()
  window.title("New Vehicle")
  window.geometry("400x400")

  """
  
  * Add car info
    *	VEHICLE ID
    * Descriptoin
    * Year
    * Type
    * Category
  
  """

  # Title
  title_label = Label(window, text='New Vehicle', font=('bold'))
  title_label.grid(row=0, column=1)

  # Input Entries
  id_label = Label(window, text='Vehicle ID:')
  id_label.grid(row=1, column=0)
  id_entry = Entry(window, width=30)
  id_entry.grid(row = 1, column=1)

  desc_label = Label(window, text='Description:')
  desc_label.grid(row=3, column=0)
  desc_entry = Entry(window, width=30)
  desc_entry.grid(row = 3, column=1)

  year_label = Label(window, text='Year:')
  year_label.grid(row=4, column=0)
  year_entry = Entry(window, width=30)
  year_entry.grid(row = 4, column=1)


  type_label = Label(window, text='Type:')
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

  type_v = StringVar()
  type_v.set(type_options[0])
    
  # Create Dropdown menu
  type_dropdown = OptionMenu(window , type_v, *type_options )
  type_dropdown.grid(row = 5, column = 1)


  category_label = Label(window, text='Category:')
  category_label.grid(row=6, column=0)

  # Dropdown menu options
  category_options = [
    "Basic", 
    "Luxury"
  ]

  category_v = StringVar()
  category_v.set(category_options[0])
    
  # Create Dropdown menu
  category_dropdown = OptionMenu(window , category_v, *category_options )
  category_dropdown.grid(row = 6, column = 1)

  # Button
  add_vehicle_btn = Button(window, text='Add Vehicle', command = add_vehicle)
  add_vehicle_btn.grid(row = 7, pady=5, column = 0, columnspan = 2)


def add_customer(window, name, phone):
  # create cursor (help create tables, perform queries, etc.)
  conn = sqlite3.connect('car_rental.db')
  cursor = conn.cursor()

  try:

    cursor.execute("""
      INSERT INTO CUSTOMER (Name, Phone) VALUES (:name, :phone);
    """, {
      "name": name,
      "phone": phone,
    })

    conn.commit()

    messagebox.showinfo("New Customer Created", "Customer Added Successfully")
    window.destroy()
    window.update()
    conn.close()

  except Exception as ex:
    print("Error creating customer", ex)
    conn.close()
  finally:
    conn.close()

def open_new_customer_window():
  window = Toplevel()
  window.title("New Customer")
  window.geometry("400x400")

  # Title
  title_label = Label(window, text='New Customer', font=('bold'))
  title_label.grid(row=0, column=1)

  # Input Entries
  name_label = Label(window, text='Customer Name:')
  name_label.grid(row=1, column=0)
  name_entry = Entry(window, width=30)
  name_entry.grid(row = 1, column=1)

  phone_label = Label(window, text='Customer Phone:')
  phone_label.grid(row=3, column=0)
  phone_entry = Entry(window, width=30)
  phone_entry.grid(row = 3, column=1)

  # Button
  add_customer_btn = Button(window, text='Add Customer', command = lambda: add_customer(window, name_entry.get(), phone_entry.get()))
  add_customer_btn.grid(row = 5, pady=5, column = 0, columnspan = 2)

# GUI components that will be accessed through root window

# TEXT BOXES, BUTTONS, LISTS
# organizing how you put those objects / widgets on your GUI
  # pack - horintal and vertical boxes, 
  # grid(recommended) - into columns and rows, 
  # place - x,y of your choosing

"""
  * Add customer info
    * Name
    * Phone

  * Add car info
    *	VEHICLE ID
    * Descriptoin
    * Year
    * Type
    * Category

  * Add rental reservation 
    * Find free vehicle (of type and category for a specific rental period)

  * Handle return of rented car
    * Print total customer payment due for that rental
      * Enter in DB and update returned attribute
    * Retrivive rental by return date, customer name, and vehicle info


  * Return view's resutls
    * List 
"""


########## MAIN WINDOW 
title_label = Label(root, text='Car Rental Dashboard', font=('bold'), pady=10)
# title_label.pack()
title_label.grid(row=0, column=0)


# Add info like customer and vehicle
add_info_label = Label(root, text='Add Information')
add_info_label.grid(row=2, column=0)

add_customer_btn = Button(root, text='Add Customer', command = open_new_customer_window)
add_customer_btn.grid(row = 3, pady=5, column = 0, columnspan = 2)

add_vehicle_btn = Button(root, text='Add Vehicle', command = open_add_vehicle_window)
add_vehicle_btn.grid(row = 3, pady=5, column = 2, columnspan = 2)


# Reservations
reservations_label = Label(root, text='Reservations')
reservations_label.grid(row = 4, column = 0)

add_reservation_btn = Button(root, text='New Reservation', command = submit)
add_reservation_btn.grid(row = 5, pady=5, column = 0, columnspan = 2)

return_car_btn = Button(root, text='Return Car', command = submit)
return_car_btn.grid(row = 5, pady=5, column = 2, columnspan = 2)



# main window lop
root.mainloop()