from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import os
import base64
import secrets
import bleach

# Generate a random secret key if not set in environment variable
if 'SECRET_KEY' not in os.environ:
    secret_key = secrets.token_hex(16)  # Generates a random key
else:
    secret_key = os.environ['SECRET_KEY']  # Load from environment variable

app = Flask(__name__)
app.secret_key = secret_key  # Used for session management

# obfuscate id using based64 encoding and decoding
def obfuscate(id):
    # Convert id to a string, encode to bytes, then base64 encode
    encoded_bytes = base64.urlsafe_b64encode(str(id).encode('utf-8'))
    # Strip the padding "=" for a cleaner URL
    return encoded_bytes.decode('utf-8').rstrip('=')

def deobfuscate(obfuscated_id):
    padding = '=' * (4 - (len(obfuscated_id) % 4))
    obfuscated_id += padding
    # Base64 decode the obfuscated ID back to original id
    decoded_bytes = base64.urlsafe_b64decode(obfuscated_id.encode('utf-8'))
    return int(decoded_bytes.decode('utf-8'))

def load_users():
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    
    users = {}
    for row in cursor.execute('SELECT username, password, role FROM users'):
        users[row[0]] = {'password': row[1], 'role': row[2]}
    
    conn.close()
    return users

def load_patients():
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    
    patients = []
    for row in cursor.execute('SELECT patient_id, name, health_history, picture FROM patients'):
        obfuscated_id = obfuscate(row[0])
        patients.append({'patient_id': row[0], 'name': row[1], 'health_history': row[2], 'picture': row[3],'obfuscated_id': obfuscated_id})
    
    conn.close()
    return patients

def load_appointments():
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    
    appointments = []
    for row in cursor.execute('SELECT appointment_id, patient_id, date, time, details, doctor_username FROM appointments'):
        appointments.append({
            'appointment_id': row[0],
            'patient_id': row[1],
            'date': row[2],
            'time': row[3],
            'details': row[4],
            'doctor_username': row[5]
        })
    
    conn.close()
    return appointments

def save_user(username, password, role):
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
    
    conn.commit()
    conn.close()

def save_patient(name, health_history, picture):
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO patients (name, health_history, picture) VALUES (?, ?, ?)', (name, health_history, picture))
    
    conn.commit()
    conn.close()

def save_appointment(patient_id, date, time, details, bank_info, doctor_username):
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO appointments (patient_id, date, time, details, bank_info, doctor_username) VALUES (?, ?, ?, ?, ?, ?)',
                   (patient_id, date, time, details, bank_info, doctor_username))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = bleach.clean(request.form['username']) #sanitize input
        password = bleach.clean(request.form['password']) #sanitize input
        role = request.form['role']

        try:
            save_user(username.capitalize(), password, role)
        except sqlite3.IntegrityError:
            return "Username already exists.", 400
        
        return redirect(url_for('index'))

    return render_template('signup.html')

# ------------------------------------------------------------------------------------- vul code
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']
    
#     # Vulnerable SQL query using string concatenation
#     query = f"SELECT * FROM users WHERE username = '{username.capitalize()}' AND password = '{password}'"
    
#     conn = sqlite3.connect('healthcare.db')
#     cursor = conn.cursor()
    
#     cursor.execute(query)
#     user = cursor.fetchone()
    
#     conn.close()
    
#     if user:
#         session['username'] = username.capitalize()
#         session['role'] = user[3]  # Assuming role is in the 3th column
#         return redirect(url_for('home'))
    
#     return "Invalid credentials", 403
# ------------------------------------------------------------------------------------- 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = bleach.clean(request.form['username'].capitalize())  # sanitize
        password = bleach.clean(request.form['password']) # sanitize
        
        # Use parameterized query to prevent SQL injection
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        
        conn = sqlite3.connect('healthcare.db')
        cursor = conn.cursor()
        
       
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            session['username'] = username
            session['role'] = user[3]  # Assuming role is in the 3th column
            return redirect(url_for('home'))
        
        return "Invalid credentials", 403

    # If it's a GET request, render the login page
    return render_template('login.html')


@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    role = session.get('role')

    if role == 'Doctor':
        # Get doctor ID based on the logged-in username
        conn = sqlite3.connect('healthcare.db')
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM users WHERE username = ?', (session['username'].replace("_", " "),))
        doctor_id_result = cursor.fetchone()
        conn.close()

        if doctor_id_result:
            doctor_id = doctor_id_result[0]
            return redirect(url_for('doctor_home', obfuscated_id=obfuscate(doctor_id)))
        else:
            return "Doctor not found", 404

    elif role == 'Patient':
        # Get patient details
        patients = load_patients()
        # Find the patient record matching the logged-in user
        patient_record = None
        for patient in patients:
            if patient['name'].replace(" ", "_").lower() == session['username'].lower():
                patient_record = patient
                break
        
        if not patient_record:
            return "Patient record not found", 404
        
        patient_id = patient_record['patient_id']
        return redirect(url_for('patient_home', obfuscated_id=obfuscate(patient_id)))
    
    else:
        return "Invalid role", 403

# @app.route('/home/doctor/int:doctor_id>')
# def doctor_home(doctor_id):
#     if 'username' not in session:
#         return redirect(url_for('index'))
    
#     role = session.get('role')

#     # Ensure that only doctors can access this route
#     if role != 'Doctor':
#         return "Unauthorized role for this page", 403

#     # Connect to the SQLite database
#     conn = sqlite3.connect('healthcare.db')
#     cursor = conn.cursor()

#     # # Find the doctor's ID using the username (doctor_name)
#     # cursor.execute('SELECT id FROM users WHERE username = ?', (doctor_id.replace("_", " "),))
#     # result = cursor.fetchone()
    
#     # if not result:
#     #     return "Doctor not found", 404

#     # doctor_id = result[0]

#     # Get all appointments and patients for all doctors
#     cursor.execute('''
#         SELECT a.appointment_id, a.date, a.time, a.details, p.patient_id, p.name 
#         FROM appointments a
#         JOIN patients p ON a.patient_id = p.patient_id
#     ''')

#     appointments = cursor.fetchall()

#     conn.close()  # Close the database connection

#     return render_template('home_doctor.html', doctor_id=doctor_id, appointments=appointments, role=role)

@app.route('/home/doctor/<obfuscated_id>', methods=['GET'])
def doctor_home(obfuscated_id):
    if 'username' not in session:
        return redirect(url_for('index'))
    
    # Deobfuscate the ID
    doctor_id = deobfuscate(obfuscated_id)

    role = session.get('role')

    # Ensure that only doctors can access this route
    if role != 'Doctor':
        return "Unauthorized role for this page", 403
    
    # Connect to the SQLite database
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()

    # Doctors can only access their own appointments
    cursor.execute('SELECT id FROM users WHERE username = ?', (session['username'].replace("_", " "),))
    result = cursor.fetchone()

    if result:
        own_doctor_id = result[0]
    else:
        return "Unauthorized", 403
    # Ensure the doctor can only access their own data
    if own_doctor_id != int(doctor_id):
        return "Unauthorized access to another doctor's data", 403
    
    # Load appointments and patients
    appointments = load_appointments()  # List of appointments
    patients = load_patients()  # List of patients

    # Render the template with appointments and patients
    return render_template('home_doctor.html', patients=patients, appointments=appointments)

## ------------------------------------------------------------------------------------- vul code
# @app.route('/home/patient/<int:patient_id>')
# def patient_home(patient_id):
#     if 'username' not in session:
#         return redirect(url_for('index'))
    
#     role = session.get('role')
    
#     # Connect to the SQLite database
#     conn = sqlite3.connect('healthcare.db')
#     cursor = conn.cursor()
    

#     if role == 'Patient':
#         cursor.execute('SELECT patient_id FROM patients WHERE name = ?', (session['username'].replace("_", " "),))
        
#     # Find the patient by ID
#     cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
#     patient = cursor.fetchone()
    
#     if not patient:
#         return "Patient not found", 404
    
#     # Convert the fetched patient tuple to a dictionary for rendering
#     patient_dict = {
#         'patient_id': patient[0],
#         'name': patient[1],
#         'health_history': patient[2],
#         'picture': patient[3]
#     }
    
#     # Get appointments for this patient
#     cursor.execute('SELECT appointment_id, date, time, details, doctor_username FROM appointments WHERE patient_id = ?', (patient_id,))
#     patient_appointments = cursor.fetchall()
    
#     conn.close()  # Close the database connection
    
#     return render_template('home_patient.html', patient=patient_dict, appointments=patient_appointments, role=role)
## -------------------------------------------------------------------------------------

@app.route('/home/patient/<obfuscated_id>')
def patient_home(obfuscated_id):
    if 'username' not in session:
        return redirect(url_for('index'))
    
    # Deobfuscate the ID
    patient_id = deobfuscate(obfuscated_id)
    role = session.get('role')

    # Ensure that only patients can access this route
    if role != 'Patient':
        return "Unauthorized role for this page", 403

    # Connect to the SQLite database
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()

    # Patients can only access their own record
    cursor.execute('SELECT patient_id FROM patients WHERE name = ?', (session['username'].replace("_", " "),))
    result = cursor.fetchone()
    
    if result:
        own_patient_id = result[0]
    else:
        return "Unauthorized", 403

    # Ensure the patient can only access their own data
    if own_patient_id != patient_id:
        return "Unauthorized access to another patient's data", 403

    # Find the patient by ID
    cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
    patient = cursor.fetchone()
    
    if not patient:
        return "Error patient not found", 404
    
    # Convert the fetched patient tuple to a dictionary for rendering
    patient_dict = {
        'patient_id': patient[0],
        'name': patient[1],
        'health_history': patient[2],
        'picture': patient[3]
    }

    # Get appointments for this patient
    cursor.execute('SELECT appointment_id, date, time, details, doctor_username FROM appointments WHERE patient_id = ?', (patient_id,))
    patient_appointments = cursor.fetchall()

    conn.close()  # Close the database connection
    
    return render_template('home_patient.html', patient=patient_dict, appointments=patient_appointments, role=role)



@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    role = session.get('role')
    if role == 'Doctor':
        return "Doctors cannot make appointments.", 403
    
    # Connect to the SQLite database
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        if role == 'Patient':
            # Find patient_id based on username
            cursor.execute('SELECT patient_id FROM patients WHERE name = ?', (session['username'].replace("_", " "),))
            patient_id = cursor.fetchone()
            if patient_id:
                patient_id = patient_id[0]
            else:
                return "Patient record not found", 404
        else:
            patient_id = request.form['patient_id']
        
        date = request.form['date']
        time = request.form['time'] 
        details = bleach.clean(request.form['details']) ## sanitize data input 
        doctor_username = request.form['doctor']
        
        # Save appointment to the database
        cursor.execute('''
            INSERT INTO appointments (patient_id, date, time, details, doctor_username)
            VALUES (?, ?, ?, ?, ?)
        ''', (patient_id, date, time, details, doctor_username))
        
        conn.commit()  # Commit the changes
        return redirect(url_for('home'))
    
    # Fetch the list of doctors for the dropdown
    cursor.execute('SELECT username FROM users WHERE role = "Doctor"')
    doctors = cursor.fetchall()
    
    conn.close()  # Close the database connection
    
    return render_template('appointment.html', doctors=[doc[0] for doc in doctors])

@app.route('/patient/<obfuscated_id>', methods=['GET', 'POST'])
def patient_view(obfuscated_id):
    if 'username' not in session:
        return redirect(url_for('index'))

    # Deobfuscate the ID
    patient_id = deobfuscate(obfuscated_id)

    role = session.get('role')
    
    # Connect to the SQLite database
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    
    # If user is a patient, ensure they can only view their own record
    if role == 'Patient':
        cursor.execute('SELECT patient_id FROM patients WHERE name = ?', (session['username'].replace("_", " "),))
        patient_record = cursor.fetchone()
        
        if not patient_record or patient_record[0] != patient_id:
            return "Unauthorized access", 403
    
    # If user is Doctor, they can view any patient
    cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
    patient = cursor.fetchone()
    
    if not patient:
        return "Patient not found", 404
    
    if request.method == 'POST' and role == 'Doctor':
        # Allow doctor to edit health history
        new_health_history = request.form['health_history']
        cursor.execute('UPDATE patients SET health_history = ? WHERE patient_id = ?', (new_health_history, patient_id))
        conn.commit()
        return redirect(url_for('patient_view', patient_id=patient_id))
    
    # Get appointments for this patient
    cursor.execute('SELECT * FROM appointments WHERE patient_id = ?', (patient_id,))
    patient_appointments = cursor.fetchall()
    
    conn.close()  # Close the database connection
    
    # Convert the fetched patient tuple to a dictionary for rendering
    patient_dict = {
        'patient_id': patient[0],
        'name': patient[1],
        'health_history': patient[2],
        'picture': patient[3]
    }
    
    return render_template('patient_view.html', patient=patient_dict, appointments=patient_appointments, role=role)


@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = bleach.clean(request.form['name']) # sanitize data
        health_history = bleach.clean(request.form['health_history']) #sanitize
        picture = bleach.clean(request.form['picture'])  # sanitize filename
        
        save_patient(name, health_history, picture)
        
        return redirect(url_for('home'))
    
    return render_template('add_patient.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))

# Add Content Security Policy (CSP)
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self';"
    return response

if __name__ == '__main__':
    app.run(debug=True)


