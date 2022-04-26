import tkinter as tk
from tkinter import * 
from DashboardWindow import DashboardWindow
from connect_to_db import connect_to_db

DB_NAME = "car_rental.db"

# GUI components that will be accessed through root window

# TEXT BOXES, BUTTONS, LISTS
# organizing how you put those objects / widgets on your GUI
  # pack - horintal and vertical boxes, 
  # grid(recommended) - into columns and rows, 
  # place - x,y of your choosing

"""
TODO:
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



# ########## MAIN WINDOW 
def main():
  root = tk.Tk()
  root.title('Car Rental Dashboard')
  root.geometry("400x400")

  conn = connect_to_db(DB_NAME)
  # 'with' will handle closing db
  with conn:
    app = DashboardWindow(root, conn)

  # main window lop
  root.mainloop()

if __name__ == '__main__':
  main()
