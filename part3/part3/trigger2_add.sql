
-- description: The Current Price of an item does not match the Amount of the most recent bid for that item,
--				update Item currently to latest bid amount

PRAGMA foreign_keys = ON;
DROP TRIGGER IF EXISTS currently_not_latest_bid;

CREATE TRIGGER currently_not_latest_bid
AFTER INSERT ON Bids
FOR EACH ROW
WHEN EXISTS (
	SELECT *
	FROM Items
	WHERE ItemID = new.ItemID AND
	Currently != new.Amount
)
BEGIN
	UPDATE Items SET Currently = new.Amount WHERE ItemID = new.ItemID;
END;