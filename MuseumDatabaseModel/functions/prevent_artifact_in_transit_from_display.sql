CREATE OR REPLACE FUNCTION prevent_artifact_in_transit_from_display()
RETURNS TRIGGER AS $$
BEGIN
    -- Checking the status of an artifact before including it in an exhibition: it can't be in transit
    IF EXISTS (
        SELECT 1
        FROM "Artifacts"
        WHERE artifact_id = NEW.artifact_id
        AND artifact_status = 'in_transit'
    ) THEN
        RAISE EXCEPTION 'The artifact is in transit and cannot be displayed at this time.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


