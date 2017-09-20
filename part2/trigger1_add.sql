
-- description: The end time for an auction must always be after its start time
PRAGMA foreign_keys = ON;
DROP TRIGGER IF EXISTS item_ends_before_starts;

CREATE TRIGGER item_ends_before_starts
AFTER INSERT ON Items
FOR EACH ROW
WHEN EXISTS (
	SELECT *
	FROM Items
	WHERE ItemID = new.ItemID
	AND new.Started >= new.Ends
)
BEGIN
	SELECT RAISE(rollback, "Item end time is before start time");
END;