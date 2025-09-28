CREATE TABLE if not EXISTS  users (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    proficiency ENUM('Beginner', 'Intermediate', 'Advanced')
);

CREATE TABLE if not EXISTS  courts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sport_type VARCHAR(50),
    location VARCHAR(255)
)AUTO_INCREMENT = 1;

CREATE TABLE if not EXISTS  bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    court_id INT,
    user_id VARCHAR(255),
    email_id VARCHAR(255),
    start_time DATETIME,
    status VARCHAR(50) DEFAULT 'confirmed',
    sport_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (court_id) REFERENCES courts(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (email_id) REFERENCES users(email)
)AUTO_INCREMENT = 1;

CREATE TABLE if not EXISTS player_groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT,
    user_id VARCHAR(255),
    FOREIGN KEY (booking_id) REFERENCES bookings(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
)AUTO_INCREMENT = 1;
