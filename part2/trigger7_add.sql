
-- description: All new bids should have the same time as the current System Time

PRAGMA foreign_keys = ON;
DROP TRIGGER IF EXISTS bid_not_matches_system_time;

CREATE TRIGGER bid_not_matches_system_time
AFTER INSERT ON Bids
FOR EACH ROW
WHEN EXISTS (
	SELECT *
	FROM Bids
	WHERE UserID = new.UserID
	AND ItemID = new.ItemID
	AND Amount = new.Amount
	AND Time NOT IN (SELECT Time
					 FROM CurrentTime
					 ORDER BY Time DESC
					 LIMIT 1)
)
BEGIN
	SELECT RAISE(rollback, "new bids must have system time");
END;