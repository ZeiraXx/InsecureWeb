```
 ___  ________   ________  _______   ________  ___  ___  ________  _______      
|\  \|\   ___  \|\   ____\|\  ___ \ |\   ____\|\  \|\  \|\   __  \|\  ___ \     
\ \  \ \  \\ \  \ \  \___|\ \   __/|\ \  \___|\ \  \\\  \ \  \|\  \ \   __/|    
 \ \  \ \  \\ \  \ \_____  \ \  \_|/_\ \  \    \ \  \\\  \ \   _  _\ \  \_|/__  
  \ \  \ \  \\ \  \|____|\  \ \  \_|\ \ \  \____\ \  \\\  \ \  \\  \\ \  \_|\ \ 
   \ \__\ \__\\ \__\____\_\  \ \_______\ \_______\ \_______\ \__\\ _\\ \_______\
    \|__|\|__| \|__|\_________\|_______|\|_______|\|_______|\|__|\|__|\|_______|
                   \|_________|                                                 
                                                                                
                                                                                
 ___       __   _______   ________                                              
|\  \     |\  \|\  ___ \ |\   __  \                                             
\ \  \    \ \  \ \   __/|\ \  \|\ /_                                            
 \ \  \  __\ \  \ \  \_|/_\ \   __  \                                           
  \ \  \|\__\_\  \ \  \_|\ \ \  \|\  \                                          
   \ \____________\ \_______\ \_______\                                         
    \|____________|\|_______|\|_______|                                         

```
### **InsecureWeb: Healthcare Portal Application**

---

This is a web-based healthcare portal built with Flask that allows doctors and patients to manage healthcare records and appointments.

## Features
- **User Roles**: Doctor and Patient
- **Doctor Features**:
  - View all patients and their health records.
  - View and manage appointments.
  - Edit patients' health history.
- **Patient Features**:
  - View personal health records.
  - Make appointments with doctors.
- **Authentication**: Secure login for both patients and doctors.
- **Security**: Sanitized input to prevent SQL injection and XSS attacks.

## Technologies Used
- **Backend**: Flask, SQLite3
- **Frontend**: HTML, CSS, Jinja2
- **Security**: User authentication, Input sanitization (Bleach), Content Security Policy (CSP)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/healthcare-portal.git
    ```

2. Navigate into the project directory:
    ```bash
    cd healthcare-portal
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the SQLite database:
    ```bash
    python innit_db.py
    ```

5. Run the application:
    ```bash
    python app.py
    ```

## Usage

1. Open your browser and navigate to `link shown in terminal`.
2. Sign up as a doctor or patient or login as:
   | username | password   | role    |
   |----------|------------|---------|
   | kaylee   | qwerty     | doctor  |
   | kim      | kim123     | doctor  |
   | miya     | password1  | patient |
   | weiss    | password2  | patient |
   | michael  | michael123 | patient |
   | henry    | henry1     | patient |   
3. Doctors can view all patients, manage appointments, and edit health histories.
5. Patients can view their own records and book appointments with doctors.

## Security
- All inputs are sanitized using `bleach` to prevent SQL injection and XSS.
- Authentication uses Flask sessions with a random secret key.
- Content Security Policy (CSP) is applied to limit resource loading.

