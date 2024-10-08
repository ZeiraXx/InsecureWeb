import sqlite3

def drop_tables():
    # Connect to the SQLite database
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()

    # List of tables to drop
    tables = ['users', 'patients', 'appointments']

    # Loop through the list of tables and drop them
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
        print(f"Table {table} has been dropped.")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def create_tables():
    # Connect to the SQLite database
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # Create patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            health_history TEXT,
            picture TEXT
        )
    ''')

    # Create appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY,
            patient_id INTEGER,
            date TEXT,
            time TEXT,
            details TEXT,
            doctor_username TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
            FOREIGN KEY (doctor_username) REFERENCES users(username)
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def populate_db():
    # Connect to the SQLite database
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()

    # Data to be inserted
    users_data = [
        (1, 'Kaylee', 'qwerty', 'Doctor'),
        (2, 'Kim', 'kim123', 'Doctor'),
        (3, 'Miya', 'password1', 'Patient'),
        (4, 'Weiss', 'password2', 'Patient'),
        (5, 'Michael', 'michael123', 'Patient'),
        (6, 'Henry', 'henry1', 'Patient')
    ]

    patients_data = [
        (3, 'Miya', 'Hospitalized for flu; Medication: Ibuprofen; Allergies: None', 'miya.jpeg'),
        (4, 'Kamal', 'Medication: Paracetamol; Operation: Appendix removal; Allergies: Penicillin', 'kamal.jpeg'),
        (5, 'Michael', 'Medication: Amoxicillin; Surgery: Tonsillectomy; Allergies: Pollen', 'michael.jpeg'),
        (6, 'Henry', 'Hospitalized for asthma; Medication: Albuterol; Allergies: Dust mites', 'henry.jpeg')
    ]

    appointments_data = [
        (1, 3, '2024-10-15', '10:00', 'Routine check-up', 'Kaylee'),
        (2, 6, '2024-10-17', '14:00', 'Mental Health Evaluation', 'Kim'),
        (3, 4, '2024-10-20', '15:00', 'Specialist Consultation', 'Kaylee'),
        (4, 5, '2024-10-20', '09:00', 'Routine check-up', 'Kim'),
        (5, 6, '2024-10-21', '09:00', 'Follow-up Visit', 'Kim')
    ]

    # Insert data into users table
    cursor.executemany('''
        INSERT INTO users (id, username, password, role) VALUES (?, ?, ?, ?)
    ''', users_data)

    # Insert data into patients table
    cursor.executemany('''
        INSERT INTO patients (patient_id, name, health_history, picture) VALUES (?, ?, ?, ?)
    ''', patients_data)

    # Insert data into appointments table
    cursor.executemany('''
        INSERT INTO appointments (appointment_id, patient_id, date, time, details, doctor_username) VALUES (?, ?, ?, ?, ?, ?)
    ''', appointments_data)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    drop_tables()    # Drop all existing tables
    create_tables()  # Recreate tables
    print("All table has been create.")
    populate_db()    # Populate with new data
    print("All table has been populate.")
