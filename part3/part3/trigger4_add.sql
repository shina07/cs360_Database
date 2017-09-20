
-- description: If auction is held in appropriate time (before its start time or after its end time), 
--				raise the trigger.
PRAGMA foreign_keys = ON;
DROP TRIGGER IF EXISTS bid_not_on_time;

CREATE TRIGGER bid_not_on_time
AFTER INSERT ON Bids
FOR EACH ROW
WHEN EXISTS (
	SELECT *
	FROM Items
	WHERE ItemID = new.ItemID
	AND ( Started > new.Time
		  OR Ends < new.Time)
)
BEGIN
	SELECT RAISE(rollback, "cannot bid if not on time");
END;