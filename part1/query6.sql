Select Count(*) From (Select Distinct UserID From Items, Bids Where Items.SellerID = Bids.UserID);