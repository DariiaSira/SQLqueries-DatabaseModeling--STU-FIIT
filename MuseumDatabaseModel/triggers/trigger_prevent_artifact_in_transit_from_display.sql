-- Create a trigger to call a function before inserting into the "Displayed_Artifacts" table
CREATE OR REPLACE TRIGGER trigger_prevent_artifact_in_transit_from_display
BEFORE INSERT ON "Displayed_Artifacts"
FOR EACH ROW EXECUTE FUNCTION prevent_artifact_in_transit_from_display();

-- This triggers will run before a record is inserted into the "Displayed_Artifacts" table.
-- Еру function checks the status the status of the artifact is not in transit:
    -- If the artifact to be included in the exhibition is in the "in_transit" state;
-- an exception will be thrown and the insertion of the entry will be canceled.