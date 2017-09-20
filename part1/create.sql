Create Table Users(UserID TEXT, Location TEXT, Country TEXT, Rating Int);
Create Table Items(ItemID Int, Name TEXT, Currently REAL, BuyPrice REAL, FirstBid REAL, NumberOfBids Int, Started TEXT, Ends TEXT, Description TEXT, SellerID TEXT);
Create Table Bids(UserID TEXT, Amount REAL, Time TEXT, ItemID Int);
Create Table Categories(ItemID Int, Category TEXT);
