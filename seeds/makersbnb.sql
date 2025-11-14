-- Drop existing tables
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS availabilities;
DROP TABLE IF EXISTS spaces;
DROP TABLE IF EXISTS users;

-- Create tables
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email text NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE spaces (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  price NUMERIC(7,2) NOT NULL,
  user_id INT NOT NULL,
  image_url TEXT,
  CONSTRAINT fk_spaces_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE bookings (
  id SERIAL PRIMARY KEY,
  date DATE NOT NULL,
  confirmed BOOLEAN NOT NULL,
  space_id INT NOT NULL,
  CONSTRAINT fk_bookings_space FOREIGN KEY(space_id) REFERENCES spaces(id) ON DELETE CASCADE,
  user_id INT NOT NULL,
  CONSTRAINT fk_bookings_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE availabilities (
  id SERIAL PRIMARY KEY,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  space_id INT NOT NULL,
  CONSTRAINT fk_availabilities_space FOREIGN KEY(space_id) REFERENCES spaces(id) ON DELETE CASCADE
);

-- Seed users
INSERT INTO users (name, email, password_hash) VALUES ('Isaac Madgewick', 'isaacm@example.com', 'hash_for_isaac');
INSERT INTO users (name, email, password_hash) VALUES ('Sabia Jeyaratnam', 'sabiaj@example.com', 'phash_for_sabia');
INSERT INTO users (name, email, password_hash) VALUES ('Sam Llewellyn', 'saml@example.com', 'hash_for_sam');
INSERT INTO users (name, email, password_hash) VALUES ('Anna Veselova', 'annav@example.com', 'hash_for_anna');
INSERT INTO users (name, email, password_hash) VALUES ('Nazarii', 'nazarii@example.com', 'hash_for_nazarii');
INSERT INTO users (name, email, password_hash) VALUES ('Margot Bourne', 'margotb@example.com', 'hash_for_margot');
INSERT INTO users (name, email, password_hash) VALUES ('Testing Account', 'pytest@pytest.com', '$2b$12$QKinH9vWDAA4WVL6nSaMuO.1OQ5cCyZo5mu1KzCYVyeGBzZJYzt2y');

-- Seed spaces (Airbnb-style listings)
INSERT INTO spaces (name, description, price, user_id, image_url) VALUES
('Cozy City Apartment', 'Modern 1-bed apartment in central London, near cafes and transport.', 120.00, 1, 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop'),
('Seaside Cottage', 'Charming cottage overlooking the sea. Perfect for a weekend getaway.', 180.00, 2, 'https://images.unsplash.com/photo-1499696010180-025ef6e1a8f9?w=800&h=600&fit=crop'),
('Mountain Cabin', 'Rustic cabin with a fireplace and forest views in the Lake District.', 150.00, 3, 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop'),
('Modern Loft', 'Bright open-plan loft in downtown Manchester with skyline views.', 200.00, 4, 'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800&h=600&fit=crop'),
('Countryside Retreat', 'Peaceful farmhouse surrounded by fields and trails.', 130.00, 5, 'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800&h=600&fit=crop'),
('Studio Flat', 'Compact studio ideal for solo travellers, near Oxford city centre.', 95.00, 6, 'https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800&h=600&fit=crop'),
('Riverside Loft', 'Bright open-plan loft with modern amenities and views of the River Thames.', 140.00, 7, 'https://images.unsplash.com/photo-1505691723518-36a5ac3be353?w=800&h=600&fit=crop'),
('Cosy Garden Cottage', 'Charming cottage with a private garden patio, perfect for a peaceful weekend stay.', 120.00, 7, 'https://images.unsplash.com/photo-1507089947368-19c1da9775ae?w=800&h=600&fit=crop');

-- Seed availabilities (each space has different available ranges)
INSERT INTO availabilities (start_date, end_date, space_id) VALUES
('2025-11-01', '2025-11-15', 1),
('2025-12-01', '2025-12-20', 1),
('2025-11-05', '2025-11-25', 2),
('2025-12-10', '2025-12-31', 3),
('2025-11-15', '2025-11-30', 4),
('2025-12-01', '2025-12-15', 5),
('2025-11-10', '2025-11-20', 6),
('2025-11-12', '2025-11-19', 7),
('2025-11-12', '2025-11-19', 8);

-- Seed bookings (each by different users)
INSERT INTO bookings (date, confirmed, space_id, user_id) VALUES
('2025-11-05', false, 1, 2), -- Sabia books Isaac's apartment
('2025-11-07', false, 1, 7), -- Test User books Isaac's apartment
('2025-11-10', false, 2, 3), -- Sam books Sabia's cottage
('2025-11-07', false, 2, 7), -- Test User books Sabia's cottage
('2025-12-12', true, 3, 4), -- Anna books Sam's cabin
('2025-11-18', true, 4, 5), -- Nazarii books Anna's loft
('2025-12-05', false, 5, 6), -- Margot books Nazarii's retreat
('2025-11-12', true, 6, 1), -- Isaac books Margot's studio
('2025-11-13', false, 7, 1), -- Isaac books Test User's loft
('2025-11-14', false, 8, 2); -- Sabia books Test User's cottage
