import tkinter as tk
from NewCustomerWindow import NewCustomerWindow
from NewVehicleWindow import NewVehicleWindow
from ReturnRentalWindow import ReturnRentalWindow
from NewReservationWindow import NewReservationWindow

class DashboardWindow:
  def __init__(self, root, conn):
    self.root = root
    self.conn = conn
    self.title_label = tk.Label(self.root, text='Car Rental Dashboard', font=('bold'), pady=10)
    self.title_label.grid(row=0, column=0)

    # Add info like customer and vehicle
    self.add_info_label = tk.Label(self.root, text='Add Information')
    self.add_info_label.grid(row=2, column=0)

    self.add_customer_btn = tk.Button(self.root, text='Add Customer', command = self.open_new_customer_window)
    self.add_customer_btn.grid(row = 3, pady=5, column = 0, columnspan = 2)

    self.add_vehicle_btn = tk.Button(self.root, text='Add Vehicle', command = self.open_add_vehicle_window)
    self.add_vehicle_btn.grid(row = 3, pady=5, column = 2, columnspan = 2)


    # Reservations
    self.reservations_label = tk.Label(self.root, text='Reservations')
    self.reservations_label.grid(row = 4, column = 0)

    self.add_reservation_btn = tk.Button(self.root, text='New Reservation', command = self.open_new_reservation_window)
    self.add_reservation_btn.grid(row = 5, pady=5, column = 0, columnspan = 2)

    self.return_car_btn = tk.Button(root, text='Return Car', command = self.open_return_car_window)
    self.return_car_btn.grid(row = 5, pady=5, column = 2, columnspan = 2)

  def open_new_customer_window(self):
    self.newWindow = tk.Toplevel(self.root)
    self.app = NewCustomerWindow(self.newWindow, self.conn)

  def open_add_vehicle_window(self):
    self.newWindow = tk.Toplevel(self.root)
    self.app = NewVehicleWindow(self.newWindow, self.conn)

  def open_new_reservation_window(self):
    self.newWindow = tk.Toplevel(self.root)
    self.app = NewReservationWindow(self.newWindow, self.conn)



  def open_return_car_window(self):
    self.newWindow = tk.Toplevel(self.root)
    self.app = ReturnRentalWindow(self.newWindow, self.conn)