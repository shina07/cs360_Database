Select Count(*) From (Select Distinct UserID From Users, Items Where Rating > 1000 and Users.UserID = Items.SellerID);