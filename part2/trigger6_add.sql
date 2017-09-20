
-- description: if the bid for the item already shown in the auction is added, 
-- 				the amount should be greater

PRAGMA foreign_keys = ON;
DROP TRIGGER IF EXISTS bid_amount_not_increasing;

CREATE TRIGGER bid_amount_not_increasing
AFTER INSERT ON Bids
FOR EACH ROW
WHEN EXISTS (
	SELECT *
	FROM Bids
	WHERE Amount >= new.Amount
	AND ItemID = new.ItemID
)
BEGIN
	SELECT RAISE(rollback, "amount should be higher");
END;