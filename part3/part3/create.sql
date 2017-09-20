DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Items;
DROP TABLE IF EXISTS Bids;
DROP TABLE IF EXISTS Categories;

CREATE TABLE Users(
	UserID TEXT PRIMARY KEY, 
	Location TEXT, 
	Country TEXT, 
	Rating INTEGER);

CREATE TABLE Items(
	ItemID INTEGER PRIMARY KEY, 
	Name TEXT, 
	Currently REAL, 
	BuyPrice REAL, 
	FirstBid REAL, 
	NumberOfBids INTEGER, 
	Started TEXT, 
	Ends TEXT, 
	Description TEXT, 
	SellerID TEXT,

	FOREIGN KEY(SellerID) REFERENCES Users(UserID));

CREATE TABLE Bids(
	UserID TEXT, 
	Amount REAL, 
	Time TEXT, 
	ItemID INTEGER,
	
	UNIQUE(ItemID, Time)
	UNIQUE(UserID, ItemID, Amount),

	FOREIGN KEY(UserID) REFERENCES Users(UserID)
	FOREIGN KEY(ItemID) REFERENCES Items(ItemID));

CREATE TABLE Categories(
	ItemID INTEGER, 
	Category TEXT,
	UNIQUE(ItemID, Category),

	FOREIGN KEY(ItemID) REFERENCES Items(ItemID));

DROP TABLE IF EXISTS CurrentTime;
CREATE TABLE CurrentTime(
	Time DATETIME
	);
INSERT INTO CurrentTime VALUES ("2001-12-20 00:00:01");
SELECT Time FROM CurrentTime;