import mysql.connector
from mysql.connector import errorcode


print("--- Loading db_manager.py ---") # Debug print to confirm file is being read

class Database:
    """Handles all database operations."""
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establishes a connection to the database."""
        try:
            self.connection = mysql.connector.connect(
                user=self.config['db_user'],
                password=self.config['db_password'],
                host=self.config['db_host'],
                database=self.config['db_name']
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("Database connection successful.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            exit(1)

    def disconnect(self):
        """Closes the database connection."""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")

    def setup_database(self):
        """Sets up the database schema and initial data."""
        print("Setting up database schema...")
        with open('schema.sql', 'r') as f:
            sql_script = f.read()
        
        for statement in sql_script.split(';'):
            if statement.strip():
                try:
                    self.cursor.execute(statement)
                except mysql.connector.Error as err:
                    print(f"Failed executing statement: {statement}")
                    print(f"Error: {err}")
        self.connection.commit()
        print("Database setup complete.")
        self._seed_data()

    def _seed_data(self):
        """Seeds the database with initial court data."""
        print("Seeding initial data...")
        courts = [
            (1, 'football', 'North Complex Court 1'),
            (2, 'football', 'North Complex Court 2'),
            (3, 'badminton', 'East Gym Court A'),
            (4, 'badminton', 'East Gym Court B'),
        ]
        query = "INSERT IGNORE INTO courts (id, sport_type, location) VALUES (%s, %s, %s)"
        for court in courts:
            self.cursor.execute(query, court)
        self.connection.commit()
        print("Data seeding complete.")


    def save_user_proficiency(self, user_id, proficiency):
        """Saves or updates a user's proficiency."""
        query = """
        INSERT INTO users (id, name, email, proficiency) 
        VALUES (%s, 'Default Name', 'default@email.com', %s) 
        ON DUPLICATE KEY UPDATE proficiency = %s
        """
        self.cursor.execute(query, (user_id, proficiency, proficiency))
        self.connection.commit()

    def check_availability(self, sport, date, time):
        """Checks for available courts."""
        query = """
        SELECT c.id, c.location FROM courts c
        WHERE c.sport_type = %s AND c.id NOT IN (
            SELECT b.court_id FROM bookings b WHERE b.start_time = %s
        )
        """
        start_time = f"{date} {time}"
        self.cursor.execute(query, (sport, start_time))
        return self.cursor.fetchall()

    def find_match(self, sport, date, time, proficiency):
        """Finds pending matches for individual players."""
        query = """
        SELECT b.id as booking_id, b.court_id, pg.user_id, u.proficiency
        FROM bookings b 
        JOIN player_groups pg ON b.id = pg.booking_id
        JOIN users u ON pg.user_id = u.id
        WHERE b.sport_type = %s AND b.start_time = %s AND u.proficiency = %s
        AND b.status = 'pending_match'
        """
        start_time = f"{date} {time}"
        # Match with players of similar proficiency
        self.cursor.execute(query, (sport, start_time, proficiency))
        return self.cursor.fetchall()


    def create_booking(self, court_id, user_id, date, time, status='confirmed'):
        """Creates a new booking."""
        query = """
        INSERT INTO bookings (court_id, user_id, start_time, status, sport_type)
        VALUES (%s, %s, %s, %s, (SELECT sport_type FROM courts WHERE id = %s))
        """
        start_time = f"{date} {time}"
        self.cursor.execute(query, (court_id, user_id, start_time, status, court_id))
        self.connection.commit()
        return self.cursor.lastrowid

    def add_player_to_group(self, booking_id, user_id):
        """Adds a player to a booking group."""
        query = "INSERT INTO player_groups (booking_id, user_id) VALUES (%s, %s)"
        self.cursor.execute(query, (booking_id, user_id))
        self.connection.commit()