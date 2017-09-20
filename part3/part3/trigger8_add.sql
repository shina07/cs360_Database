
-- description: If new system time is added as the current time, the time should be increasing

PRAGMA foreign_keys = ON;
DROP TRIGGER IF EXISTS current_time_not_increasing;

CREATE TRIGGER current_time_not_increasing
AFTER INSERT ON CurrentTime
FOR EACH ROW
WHEN EXISTS (
	SELECT *
	FROM CurrentTime
	WHERE Time >= new.Time
)

BEGIN
	SELECT RAISE(rollback, "Time should go forward");
END;