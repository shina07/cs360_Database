
-- description: NumofBids attribute for each Item should matches to the actual number of bids for the item.

PRAGMA foreign_keys = ON;
DROP TRIGGER IF EXISTS number_of_bids_not_correct;

CREATE TRIGGER number_of_bids_not_correct
AFTER INSERT ON Bids
FOR EACH ROW
WHEN EXISTS (
	SELECT *
	FROM Items
	WHERE ItemID = new.ItemID
	AND NumberOfBids != (SELECT COUNT(*)
						 FROM Bids
						 WHERE ItemID = new.ItemID)
)
BEGIN
	UPDATE Items
	SET NumberOfBids = (SELECT COUNT(*)
			 			FROM Bids
			 			WHERE ItemID = new.ItemID)
	WHERE ItemID = new.ItemID;
END;