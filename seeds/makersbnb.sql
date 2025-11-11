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
  password TEXT NOT NULL
);

CREATE TABLE spaces (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  price NUMERIC(7,2) NOT NULL,
  user_id INT NOT NULL,
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
INSERT INTO users (name, email, password) VALUES ('Isaac Madgewick', 'isaacm@example.com', 'password123');
INSERT INTO users (name, email, password) VALUES ('Sabia Jeyaratnam', 'sabiaj@example.com', 'password123');
INSERT INTO users (name, email, password) VALUES ('Sam Llewellyn', 'saml@example.com', 'password123');
INSERT INTO users (name, email, password) VALUES ('Anna Veselova', 'annav@example.com', 'password123');
INSERT INTO users (name, email, password) VALUES ('Nazarii', 'nazarii@example.com', 'password123');
INSERT INTO users (name, email, password) VALUES ('Margot Bourne', 'margotb@example.com', 'password123');

-- Seed spaces (Airbnb-style listings)
INSERT INTO spaces (name, description, price, user_id) VALUES 
('Cozy City Apartment', 'Modern 1-bed apartment in central London, near cafes and transport.', 120.00, 1),
('Seaside Cottage', 'Charming cottage overlooking the sea. Perfect for a weekend getaway.', 180.00, 2),
('Mountain Cabin', 'Rustic cabin with a fireplace and forest views in the Lake District.', 150.00, 3),
('Modern Loft', 'Bright open-plan loft in downtown Manchester with skyline views.', 200.00, 4),
('Countryside Retreat', 'Peaceful farmhouse surrounded by fields and trails.', 130.00, 5),
('Studio Flat', 'Compact studio ideal for solo travellers, near Oxford city centre.', 95.00, 6);

-- Seed availabilities (each space has different available ranges)
INSERT INTO availabilities (start_date, end_date, space_id) VALUES
('2025-11-01', '2025-11-15', 1),
('2025-12-01', '2025-12-20', 1),
('2025-11-05', '2025-11-25', 2),
('2025-12-10', '2025-12-31', 3),
('2025-11-15', '2025-11-30', 4),
('2025-12-01', '2025-12-15', 5),
('2025-11-10', '2025-11-20', 6);

-- Seed bookings (each by different users)
INSERT INTO bookings (date, confirmed, space_id, user_id) VALUES
('2025-11-05', false, 1, 2), -- Sabia books Isaac's apartment
('2025-11-10', false, 2, 3), -- Sam books Sabia's cottage
('2025-12-12', true, 3, 4), -- Anna books Sam's cabin
('2025-11-18', true, 4, 5), -- Nazarii books Anna's loft
('2025-12-05', false, 5, 6), -- Margot books Nazarii's retreat
('2025-11-12', true, 6, 1); -- Isaac books Margot's studio
