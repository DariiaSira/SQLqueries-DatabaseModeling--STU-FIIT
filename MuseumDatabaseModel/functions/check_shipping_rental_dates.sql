-- Create a function to verify shipping date is before borrow date and
-- delivering date is after return one to avoid wrong set values.
CREATE OR REPLACE FUNCTION check_shipping_rental_dates()
RETURNS TRIGGER AS $$
BEGIN
    -- Checking shipping_date and delivery_date against rental period
    IF EXISTS (
        SELECT 1
        FROM "Rental" R
        JOIN "Artifacts" A ON R.artifact_id = A.artifact_id
        JOIN "Control" C ON A.control_id = C.control_id
        WHERE R.artifact_id = (SELECT artifact_id FROM "Artifacts" WHERE control_id = NEW.control_id)
        AND NEW.shipping_date <= R.rental_date OR NEW.delivery_date <= R.return_date
    ) THEN
        RAISE EXCEPTION 'Shipping and delivery dates must be within rental period.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- shipping_date (Shipping is under museum's, which sends the item obligation. It takes some time, so shipping date is before actual rental date, when museum owns the artifact)
-- -> rental_date (the actual date museum owns the artifact)
--  -> delivery_date (Delivering is under museum's, which owns the item obligation. It takes some time, so delivery date is before actual return date, when museum sends the artifact)
--   -> return_date (the actual date museum gets back the artifact)

-- For example: We have museum A(we) and B.
-- A(We) borrows the item from B:
--      B sends on 1th (shipping_date=1), A have it on 3rd (rental_date=3).
--      A sends back on 10th (delivery_date=10), B have it back on 12th (return_date=12)
-- A(We) lends the item to B (the same situation):
--      A sends on 1th (shipping_date=1), B have it on 3rd (rental_date=3).
--      B sends back on 10th (delivery_date=10), A have it back on 12th (return_date=12)
