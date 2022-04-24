"""
	Tkinter
"""

from tkinter import * 
from tkinter import messagebox
import sqlite3


try:

	# Connect to DB
	conn = sqlite3.connect('car_rental.db')
	print("Connected to DB successfully")

	cursor = conn.cursor()

	cursor.executescript("""

CREATE TABLE CUSTOMER (
	CustID INTEGER UNIQUE NOT NULL,
	Name TEXT NOT NULL,
	Phone TEXT NOT NULL,
	
	PRIMARY KEY(CustID)
);

CREATE TABLE RATE (
	-- *Type: 1:Compact, 2:Medium, 3:Large, 4:SUV, 5:Truck, 6:VAN	
	Type INTEGER NOT NULL,
	-- *Category: 0:Basic, 1:Luxury
	Category INTEGER NOT NULL,
	Weekly INTEGER NOT NULL,
	Daily INTEGER NOT NULL,
    
	PRIMARY KEY (Type, Category)
);


CREATE TABLE RENTAL (
	CustID INTEGER AUTO_INCREMENT NOT NULL,
	VehicleID TEXT NOT NULL,
	-- Format: day-month-year
	StartDate DATE NOT NULL,
	OrderDate DATE NOT NULL,
	-- *RentalType: ‘1’ for Daily, and ‘7’ for Weekly
	RentalType INTEGER NOT NULL,
	Qty INTEGER NOT NULL,
	ReturnDate DATE NOT NULL,
	TotalAmount INTEGER,
	-- Nullable
	PaymentDate DATE,
	
	PRIMARY KEY (CustID, VehicleID, StartDate),
	
	-- Foreign Keys
	FOREIGN KEY(CustID) REFERENCES CUSTOMER(CustID),
	FOREIGN KEY(VehicleID) REFERENCES VEHICLE(VehicleID)
);

CREATE TABLE VEHICLE (
	VehicleID TEXT UNIQUE NOT NULL,
	Description TEXT,
	Year INTEGER NOT NULL,
	-- *Type: 1:Compact, 2:Medium, 3:Large, 4:SUV, 5:Truck, 6:VAN
	Type INTEGER NOT NULL,
	-- *Category: 0:Basic, 1:Luxury
	Category INTEGER NOT NULL,
	
	PRIMARY KEY(VehicleID)
);

INSERT INTO CUSTOMER ("CustID", "Name", "Phone") VALUES
('201', 'A. Parks', '(214) 555-0127'),
('202', 'S. Patel', '(849) 811-6298'),
('203', 'A. Hernandez', '(355) 572-5385'),
('204', 'G. Carver', '(753) 763-8656'),
('205', 'Sh. Byers', '(912) 925-5332'),
('206', 'L. Lutz', '(931) 966-1775'),
('207', 'L. Bernal', '(884) 727-0591'),
('208', 'I. Whyte', '(811) 979-7345'),
('209', 'L. Lott', '(954) 706-2219'),
('210', 'G. Clarkson', '(309) 625-1838'),
('211', 'Sh. Dunlap', '(604) 581-6642'),
('212', 'H. Gallegos', '(961) 265-8638'),
('213', 'L. Perkins', '(317) 996-3104'),
('214', 'M. Beach', '(481) 422-0282'),
('215', 'C. Pearce', '(599) 881-5189'),
('216', 'A. Hess', '(516) 570-6411'),
('217', 'M. Lee', '(369) 898-6162'),
('218', 'R. Booker', '(730) 784-6303'),
('219', 'A. Crowther', '(325) 783-4081'),
('220', 'H. Mahoney', '(212) 262-8829'),
('221', 'J. Brown', '(644) 756-0110'),
('222', 'H. Stokes', '(931) 969-7317'),
('223', 'J. Reeves', '(940) 981-5113'),
('224', 'A. Mcghee', '(838) 610-5802'),
('225', 'L. Mullen', '(798) 331-7777'),
('226', 'R. Armstrong', '(325) 783-4081'),
('227', 'J. Greenaway', '(212) 262-8829'),
('228', 'K. Kaiser Acosta', '(228) 576-1557'),
('229', 'D. Kirkpatrick', '(773) 696-8009'),
('230', 'A. Odonnell', '(439) 536-8929'),
('231', 'K. Kay', '(368) 336-5403');

INSERT INTO RATE ("Type", "Category", "Weekly", "Daily") VALUES
('1', '0', '480', '80'),
('1', '1', '600', '100'),
('2', '0', '530', '90'),
('2', '1', '660', '110'),
('3', '0', '600', '100'),
('3', '1', '710', '120'),
('4', '0', '685', '115'),
('4', '1', '800', '135'),
('5', '0', '780', '130'),
('6', '0', '685', '115');

INSERT INTO RENTAL ("CustID", "VehicleID", "StartDate", "OrderDate", "RentalType", "Qty", "ReturnDate", "TotalAmount", "PaymentDate") VALUES
('203', 'JM3KE4DY4F0441471', '2019-09-09', '2019-05-22', '1', '4', '2019-09-13', '460', '2019-09-09'),
('210', '19VDE1F3XEE414842', '2019-11-01', '2019-10-28', '7', '2', '2019-11-15', '1200', ''),
('210', 'JTHFF2C26F135BX45', '2019-05-01', '2019-04-15', '7', '1', '2019-05-08', '600', '2019-05-08'),
('210', 'JTHFF2C26F135BX45', '2019-11-01', '2019-10-28', '7', '2', '2019-11-15', '1200', ''),
('210', 'WAUTFAFH0E0010613', '2019-11-01', '2019-10-28', '7', '2', '2019-11-15', '1200', ''),
('210', 'WBA3A9G51ENN73366', '2019-11-01', '2019-10-28', '7', '2', '2019-11-15', '1200', ''),
('210', 'WBA3B9C59EP458859', '2019-11-01', '2019-10-28', '7', '2', '2019-11-15', '1200', ''),
('210', 'WDCGG0EB0EG188709', '2019-11-01', '2019-10-28', '7', '2', '2019-11-15', '1200', ''),
('212', '19VDE1F3XEE414842', '2019-06-10', '2019-04-15', '7', '3', '2019-07-01', '1800', '2019-06-10'),
('216', '1N6BF0KM0EN101134', '2019-08-02', '2019-03-15', '7', '4', '2019-08-30', '2740', '2019-08-02'),
('216', '1N6BF0KM0EN101134', '2019-08-30', '2019-03-15', '1', '2', '2019-09-01', '230', '2019-08-02'),
('221', '19VDE1F3XEE414842', '2019-07-01', '2019-06-12', '7', '1', '2019-07-08', '600', '2019-07-01'),
('221', '19VDE1F3XEE414842', '2019-07-09', '2019-06-12', '1', '2', '2019-07-11', '200', '2019-07-01'),
('221', '19VDE1F3XEE414842', '2020-01-01', '2019-12-15', '7', '4', '2020-01-29', '2400', ''),
('221', 'JTHFF2C26F135BX45', '2020-01-01', '2019-12-15', '7', '4', '2020-01-29', '2400', ''),
('221', 'WAUTFAFH0E0010613', '2019-07-01', '2019-06-12', '7', '1', '2019-07-08', '600', '2019-07-01'),
('221', 'WAUTFAFH0E0010613', '2019-07-09', '2019-06-12', '1', '2', '2019-07-11', '200', '2019-07-01'),
('221', 'WAUTFAFH0E0010613', '2020-01-01', '2019-12-15', '7', '4', '2020-01-29', '2400', ''),
('221', 'WBA3A9G51ENN73366', '2020-01-01', '2019-12-15', '7', '4', '2020-01-29', '2400', ''),
('221', 'WBA3B9C59EP458859', '2020-01-01', '2019-12-15', '7', '4', '2020-01-29', '2400', ''),
('221', 'WDCGG0EB0EG188709', '2020-01-01', '2019-12-15', '7', '4', '2020-01-29', '2400', ''),
('229', '19VDE1F3XEE414842', '2019-05-06', '2019-04-12', '1', '4', '2019-05-10', '400', '2019-05-06'),
('229', 'WAUTFAFH0E0010613', '2019-05-06', '2019-04-12', '1', '4', '2019-05-10', '400', '2019-05-06');

INSERT INTO VEHICLE ("VehicleID", "Description", "Year", "Type", "Category") VALUES
('19VDE1F3XEE414842', 'Acura ILX', '2014', '1', '1'),
('1FDEE3FL6EDA29122', 'Ford E 350', '2014', '6', '0'),
('1FDRF3B61FEA87469', 'Ford Super Duty Pickup', '2015', '5', '0'),
('1FTNF1CF2EKE54305', 'Ford F Series Pickup', '2014', '5', '0'),
('1G1JD5SB3E4240835', 'Chevrolet Optra', '2014', '1', '0'),
('1GB3KZCG1EF117132', 'Chevrolet Silverado', '2014', '5', '0'),
('1HGCR2E3XEA305302', 'Honda Accord', '2014', '2', '0'),
('1N4AB7AP2EN855026', 'Nissan Sentra', '2014', '1', '0'),
('1N6BA0EJ9EN516565', 'Nissan Titan', '2014', '5', '0'),
('1N6BF0KM0EN101134', 'Nissan NV', '2014', '6', '0'),
('1VWCH7A3XEC037969', 'Volkswagen Passat', '2014', '2', '1'),
('2HGFB2F94FH501940', 'Honda Civic', '2015', '1', '0'),
('2T3DFREV0FW317743', 'Toyota RAV4', '2015', '4', '0'),
('3MZBM1L74EM109736', 'Mazda 3', '2014', '1', '0'),
('3N1CE2CP0FL409472', 'Nissan Versa Note', '2015', '1', '0'),
('3N1CN7APXEK444458', 'Nissan Versa', '2014', '1', '0'),
('3VW2A7AU1FM012211', 'Volkswagen Golf', '2015', '1', '0'),
('4S4BRCFC1E3203823', 'Subaru Outback', '2014', '4', '0'),
('4S4BSBF39F3261064', 'Subaru Outback', '2015', '4', '0'),
('4S4BSELC0F3325370', 'Subaru Outback', '2015', '4', '0'),
('5J6RM4H90FL028629', 'Honda CR-V', '2015', '4', '0'),
('5N1AL0MM8EL549388', 'Infiniti JX35', '2014', '4', '1'),
('5NPDH4AE2FH565275', 'Hyundai Elantra', '2015', '1', '0'),
('5TDBKRFH4ES26D590', 'Toyota Highlander', '2014', '4', '0'),
('5XYKT4A75FG610224', 'Kia Sorento', '2015', '4', '0'),
('5XYKU4A7XFG622415', 'Kia Sorento', '2015', '4', '0'),
('5XYKUDA77EG449709', 'Kia Sorento', '2014', '4', '0'),
('JF1GPAA61F8314971', 'Subaru Impreza', '2015', '1', '0'),
('JH4KC1F50EC800004', 'Acura RLX', '2014', '3', '1'),
('JH4KC1F56EC000095', 'Acura RLX', '2014', '3', '1'),
('JM1BM1V35E1210570', 'Mazda 3', '2014', '1', '0'),
('JM3KE4DY4F0441471', 'Mazda CX5', '2015', '4', '0'),
('JM3TB3DV0E0015742', 'Mazda CX9', '2014', '4', '0'),
('JN8AS5MV0FW760408', 'Nissan Rogue Select', '2015', '4', '0'),
('JTEZUEJR7E5081641', 'Toyota 4Runner', '2014', '4', '0'),
('JTHBW1GG1F120DU53', 'Lexus ES 300h', '2015', '2', '1'),
('JTHCE1BL3F151DE04', 'Lexus GS 350', '2015', '2', '1'),
('JTHDL5EF9F5007221', 'Lexus LS 460', '2015', '3', '1'),
('JTHFF2C26F135BX45', 'Lexus IS 250C', '2015', '1', '1'),
('JTJHY7AX2F120EA11', 'Lexus LX 570', '2015', '4', '1'),
('JTJJM7FX2E152CD75', 'Lexus GX460', '2014', '4', '1'),
('JTMBFREV1FJ019885', 'Toyota RAV4', '2015', '4', '0'),
('KM8SN4HF0FU107203', 'Hyundai Santa Fe', '2015', '4', '0'),
('KMHJT3AF1FU028211', 'Hyundai Tucson', '2015', '4', '0'),
('KMHTC6AD8EU998631', 'Hyundai Veloster', '2014', '1', '0'),
('KNAFZ4A86E5195865', 'KIA Sportage', '2014', '4', '0'),
('KNAFZ4A86E5195895', 'KIA Forte', '2014', '1', '0'),
('KNAGN4AD2F5084324', 'Kia Optima Hybrid', '2015', '2', '0'),
('KNALN4D75E5A57351', 'Kia Cadenza', '2014', '3', '0'),
('KNALU4D42F6025717', 'Kia K900', '2015', '3', '0'),
('KNDPCCA65F7791085', 'KIA Sportage', '2015', '4', '0'),
('WA1LGAFE8ED001506', 'Audi Q7', '2014', '4', '1'),
('WAU32AFD8FN005740', 'Audi A8', '2015', '3', '1'),
('WAUTFAFH0E0010613', 'Audi A5', '2014', '1', '1'),
('WBA3A9G51ENN73366', 'BMW 3 Series', '2014', '1', '1'),
('WBA3B9C59EP458859', 'BMW 3 Series', '2014', '1', '1'),
('WBAVL1C57EVR93286', 'BMW X1', '2014', '4', '1'),
('WDCGG0EB0EG188709', 'Mercedes_Benz GLK', '2014', '1', '1'),
('YV440MDD6F2617077', 'Volvo XC60', '2015', '4', '1'),
('YV4940NB5F1191453', 'Volvo XC70', '2015', '4', '1');
	""")


	print("Created table successfully")

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