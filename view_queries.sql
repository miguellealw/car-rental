
/*
	OrderDate
	StartDate – in an ascending order
	ReturnDate
	Total Days per Rental as 'TotalDays'– you need to change weeks to days

	Vehicle’s ID as 'VIN'
	Vehicle’s Description as 'Vehicle'
	Vehicle’s Type as 'Type'– you need to use the description of the type
	Vehicle’s Category as 'Category' – you need to use the description of the category
	Customer’s ID as 'CustomerID'
	Customer’s Name as 'CustomerName'

	Order Total Amount as 'OrderAmount',
	Order Remaining Amount as 'RentalBalance' – If there is no remaining balance return zero ‘0’
*/

CREATE VIEW vRentalInfo AS
SELECT 
re.OrderDate, re.StartDate, re.ReturnDate, re.TotalAmount as "OrderAmount",
-- TODO: figure out hwo to return TotalDays per rental
v.VehicleID as "VIN", v.Description as "Vehicle",
CASE 
    WHEN v.Type = 1 THEN "Compact"
    WHEN v.Type = 2 THEN "Medium"
    WHEN v.Type = 3 THEN "Large"
    WHEN v.Type = 4 THEN "SUV"
    WHEN v.Type = 5 THEN "Truck"
    WHEN v.Type = 6 THEN "Van"
    ELSE "Unsupported vehicle type"
END AS "Type",
CASE
	WHEN v.Category = 0 THEN "Basic"
	WHEN v.Category = 1 THEN "Luxury"
	ELSE "Unsupported vehicle category"
END AS "Category", 
c.CustID as "CustomerID", c.Name as "CustomerName"
-- TODO: figure out remaining amount as RemainingBalance
FROM car_rental.RENTAL re
INNER JOIN car_rental.CUSTOMER c ON re.CustID = c.CustID
INNER JOIN car_rental.VEHICLE v ON re.VehicleID = v.VehicleID;

