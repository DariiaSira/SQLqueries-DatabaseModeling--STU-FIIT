-- Create a trigger to call a function when inserting and updating records
CREATE OR REPLACE TRIGGER trigger_update_exhibition_status
BEFORE INSERT OR UPDATE ON "Exhibitions"
FOR EACH ROW EXECUTE FUNCTION update_exhibition_status();

-- This trigger will run when inserting new records or updating existing records in the "Exhibitions" table,
-- exhibition_status will be automatically updated according to the current date and the exhibition start and end dates.