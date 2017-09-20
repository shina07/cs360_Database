
-- description: if user bid on an item he or she is also selling, raise the trigger.
PRAGMA foreign_keys = ON;
DROP TRIGGER IF EXISTS bid_own_item;

CREATE TRIGGER bid_own_item
AFTER INSERT ON Bids
FOR EACH ROW
WHEN EXISTS (
	SELECT *
	FROM Items
	WHERE SellerID = new.UserID
	AND ItemID = new.ItemID
)
BEGIN
	SELECT RAISE(rollback, "User cannot bid own item");
END;