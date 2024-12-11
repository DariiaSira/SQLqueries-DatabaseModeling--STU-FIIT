-- Create a trigger to call a function before inserting into the "Displayed_Artifacts" table
CREATE OR REPLACE TRIGGER trigger_ensure_unique_display
BEFORE INSERT ON "Displayed_Artifacts"
FOR EACH ROW EXECUTE FUNCTION ensure_unique_display();

-- This triggers will run before a record is inserted into the "Displayed_Artifacts" table.
-- The function verifies that the artifact is not already on display at another active exhibit:
    -- If the artifact is already on display in another exhibition (i.e., there is an entry in the
    -- "Displayed_Artifacts" table with the same artifact_id but a different exhibition_id);
-- an exception will be thrown and the insertion of the entry will be canceled.