-- Create a trigger to call a function before inserting into the "Displayed_Artifacts" table
CREATE OR REPLACE TRIGGER trigger_check_room_insertion
BEFORE INSERT ON "Displayed_Artifacts"
FOR EACH ROW EXECUTE FUNCTION check_room_insertion();

-- This trigger will run before inserting a record into the Exhibitions table.
-- It checks the number of active exhibitions for the specified room.
-- If there is already an active exhibition in this room, an exception will be thrown
-- and the insertion of the record will be canceled.
-- If an exhibition has been held or has not yet started, this check will succeed.