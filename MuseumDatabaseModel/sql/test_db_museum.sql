INSERT INTO "Owners" ("name", "contact_phone", "contact_email", "address")
VALUES
  ('Jane Smith', '+9876543210', 'jane.smith@example.com', '456 Elm Street, Othertown'),
  ('Michael Johnson', '+1122334455', 'michael.johnson@example.com', '789 Oak Avenue, Anycity'),
  ('Emily Davis', '+9988776655', 'emily.davis@example.com', '101 Pine Road, Anothercity');

INSERT INTO "Categories" ("name", "description")
VALUES
  ('Painting', 'Artworks created by applying pigment to a surface.'),
  ('Pottery', 'Artworks made of clay and other materials, typically shaped while wet and then hardened by firing.'),
  ('Photography', 'Art of creating durable images by recording light.');

INSERT INTO "Rooms" ("name", "description")
VALUES
  ('Gallery Room 2', 'Another spacious room for art exhibitions.'),
  ('Lobby', 'The entrance area of the gallery.'),
  ('Small Gallery', 'A cozy space for intimate art displays.');

INSERT INTO "Control" ("control_date", "checked", "description", "shipping_date", "delivery_date")
VALUES
  ('2024-04-20T09:00:00Z', false, 'Pending check before shipping.', '2024-04-10T09:00:00Z', '2024-04-20T12:00:00Z'),
  ('2024-04-16T11:00:00Z', true, 'Checked before shipping.', '2024-04-10T08:00:00Z', '2024-04-20T12:00:00Z'),
  ('2024-04-19T10:00:00Z', true, 'Checked before shipping.', '2024-04-12T08:00:00Z', '2024-04-30T12:00:00Z');

INSERT INTO "Control" ("control_date", "checked", "description", "shipping_date", "delivery_date")
VALUES
 ('2024-04-19T10:00:00Z', true, 'Checked before shipping.', '2024-04-12T08:00:00Z', '2024-04-30T12:00:00Z');

UPDATE "Control"
    SET shipping_date = '2024-04-12T08:00:00Z',
        delivery_date = '2024-04-23T08:00:00Z'
WHERE control_id = 7;

UPDATE "Artifacts"
    SET control_id = 27
WHERE artifact_id = 22;

INSERT INTO "Artifacts" ("name", "description", "control_id", "artifact_status")
VALUES
  ('Golden Mask', 'An ancient golden mask.', 6, 'unknown'),
  ('Still Life', 'A classic still life painting.', 7, 'in_transit'),
  ('Ceramic Vase', 'A modern ceramic vase.', 8, 'in_storage');

INSERT INTO "Exhibitions" ("name", "description", "exhibition_status", "start_date", "end_date")
VALUES
  ('Modern Art Showcase', 'Displaying contemporary artworks.', NULL, '2024-05-01T10:00:00Z', '2024-06-01T18:00:00Z'),
  ('Photography Exhibition', 'Showcasing captivating photographs.', NULL, '2024-05-10T10:00:00Z', '2024-06-10T18:00:00Z'),
  ('Pottery Collection', 'Featuring a variety of pottery pieces.', NULL, '2024-05-15T10:00:00Z', '2024-06-15T18:00:00Z'),
  ('Modern Art Showcase2', 'Displaying contemporary artworks.', NULL, '2024-04-01T10:00:00Z', '2024-05-01T18:00:00Z');

UPDATE "Exhibitions"
SET "start_date" = '2024-03-20T10:00:00Z',
    "end_date" = '2024-04-20T18:00:00Z'
WHERE "name" = 'Pottery Collection';


INSERT INTO "ArtifactCategories" ("artifact_id", "category_id")
VALUES
  (16, 4),
  (17, 5),
  (18, 6);

INSERT INTO "Displayed_Artifacts" ("exhibition_id", "artifact_id", "room_id")
VALUES
  (4, 16, 4),
  (6, 18, 5);

INSERT INTO "Rental" ("artifact_id", "owner_id", "rental_status", "rental_date", "return_date")
VALUES
  (16, 5, 'borrowed', '2024-04-11T09:00:00Z', '2024-04-22T12:00:00Z'),
  (17, 6, 'lent', '2024-04-10T08:00:00Z', '2024-05-20T12:00:00Z'),
  (18, 4, 'owned', NULL, NULL);

INSERT INTO "Categories" ("name", "description")
VALUES
('Painting', 'Artworks created by applying pigment to a surface.'),
('Pottery', 'Artworks made of clay and other materials, typically shaped while wet and then hardened by firing.'),
('Photography', 'Art of creating durable images by recording light.');
