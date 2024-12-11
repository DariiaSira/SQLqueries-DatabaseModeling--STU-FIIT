-- Create a function to check that a room has only one active exhibition.
-- Since the museum has several rooms, an exhibition can take place within one or more rooms.
-- However, it is impossible to have two exhibitions within the same room at the same time.
-- So, the function checks that one room don't have two active exhibitions.
-- For prepared and passed ones it's doesn't work.

CREATE OR REPLACE FUNCTION check_room_insertion()
RETURNS TRIGGER AS $$
DECLARE
    count_active_exhibitions INT;
BEGIN
    SELECT COUNT(*)
    INTO count_active_exhibitions
    FROM "Displayed_Artifacts" da
    JOIN "Exhibitions" e ON da.exhibition_id = e.exhibition_id
    WHERE da.room_id = NEW.room_id
    AND e.exhibition_status = 'active';
    IF count_active_exhibitions > 0 THEN
        RAISE EXCEPTION 'The room already has an active exhibition.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

