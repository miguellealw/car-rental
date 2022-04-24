
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
	re.OrderDate,
	re.StartDate,
	re.ReturnDate,
	-- TODO: figure out hwo to return TotalDays per rental

	v.VehicleID as "VIN",
	v.Description as "Vehicle",
	v.Type as "Type" -- TODO: use description of type (use switch case)
	v.Category as "Category" -- TODO: use description of category (use switch case)

	c.CustID as "CustomerID",
	c.Name as "CustomerName",

	re.TotalAmount as "OrderAmount",
	-- TODO: figure out remaining amount as RemainingBalance
