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

### **InsecureWeb: Demo Healthcare Patient Management System Vulnerability Analysis**

---

#### **Overview**

This project demonstrates three common web vulnerabilities — **Cross-Site Scripting (XSS)**, **Insecure Direct Object Reference (IDOR)**, and **CSV Injection** — using a simple **Healthcare Patient Management System**. These vulnerabilities are frequently encountered in real-life systems, particularly in applications dealing with sensitive information, such as patient portals in healthcare systems.

The primary goal is to understand how these vulnerabilities occur, how they can be exploited by attackers, and the potential risks to the system and its users. Additionally, this project highlights the importance of secure coding practices to mitigate these issues.

---

### **Why These Vulnerabilities Were Chosen**

1. **Cross-Site Scripting (XSS)**:
   - **Reason**: XSS occurs when user input is not properly sanitized and allows the injection of malicious scripts. In healthcare systems, patient comments or chat sections can be entry points for attackers.
   - **Risk**: Attackers can steal session cookies, deface the website, or redirect users to malicious sites. In the context of healthcare, they could tamper with sensitive patient-doctor communication or manipulate medical records.

2. **Insecure Direct Object Reference (IDOR)**:
   - **Reason**: IDOR vulnerabilities arise when access to sensitive information relies solely on predictable IDs or URLs without sufficient access control. In healthcare systems, patient IDs or record IDs are often passed through the URL, which attackers can manipulate.
   - **Risk**: Attackers could access or modify other patients' private medical records, violating patient confidentiality and regulatory standards (such as HIPAA in healthcare).

3. **CSV Injection**:
   - **Reason**: CSV Injection occurs when unsanitized data is exported to a CSV file that is later opened in a spreadsheet tool (e.g., Excel), allowing attackers to execute malicious commands.
   - **Risk**: Attackers could insert harmful formulas or commands in patient records, compromising the system of whoever opens the exported file, leading to data exfiltration or system exploitation.

---

### **How These Vulnerabilities Work and Can Be Exploited**

#### **1. Cross-Site Scripting (XSS)**

- **How it works**: XSS occurs when an application accepts unsanitized input from a user, which is then reflected back to other users or administrators. In this demo app, the patient can input comments (e.g., in the appointment chat with a doctor), and malicious scripts entered here are not sanitized.
  
- **Exploitation**:
  - A patient enters a comment containing a malicious script: `<script>alert('XSS Attack!')</script>`.
  - When the doctor or another user views the comment, the script is executed in their browser, resulting in an alert or potentially more harmful actions like cookie theft.

- **Risk Example**: In a real healthcare system, an attacker could exploit XSS to tamper with medical data or perform phishing attacks on staff or other patients.

- **Mitigation**: Always sanitize user input using proper encoding techniques like escaping special characters (e.g., `&`, `<`, `>`). Utilize libraries such as **DOMPurify** in JavaScript or sanitize HTML server-side using tools such as **Bleach** (Python).

---

#### **2. Insecure Direct Object Reference (IDOR)**

- **How it works**: IDOR allows attackers to manipulate URLs or request parameters to access data they are not authorized to view. In this app, each patient has a unique `patient_id` (e.g., `/record/1`), but there is no authorization check to ensure the user viewing the record is the correct patient.

- **Exploitation**:
  - A patient is logged in and accessing their record via `/record/1`.
  - The attacker changes the URL to `/record/2` to view or modify another patient's record, exploiting the lack of access controls.

- **Risk Example**: In a healthcare system, this flaw could expose sensitive medical data, violating privacy laws like HIPAA and resulting in legal and financial penalties for the healthcare provider.

- **Mitigation**: Always enforce **authorization** checks at the server level. Ensure that the current user has the appropriate rights to access the requested resource. Implement role-based access control (RBAC) and check whether the `user_id` matches the `patient_id` in each request.

---

#### **3. CSV Injection**

- **How it works**: CSV Injection occurs when user-supplied data (e.g., patient names or notes) is exported to a CSV file without being sanitized. When the file is opened in a spreadsheet application like Excel, malicious data could be interpreted as commands and executed.

- **Exploitation**:
  - An attacker submits a comment or patient note containing a malicious formula: `=cmd|' /C calc'!A0`.
  - When the exported CSV file is opened in Excel, the formula is executed, launching the calculator or a more harmful command.

- **Risk Example**: CSV Injection can compromise the machines of administrators who open the files. In a healthcare system, it could lead to data breaches or the attacker gaining control of critical systems.

- **Mitigation**: Ensure that user inputs destined for CSV exports are properly sanitized. Escape characters such as `=`, `+`, `-`, and `@` before saving user data into a CSV file. Use a CSV sanitization library or create your own sanitization logic to prevent malicious formulas from being executed.

---

### **Code Highlights**

Here are some points in the code where these vulnerabilities occur and how they can be mitigated:

#### **Cross-Site Scripting (XSS) in `appointment.html`:**
```python
# Vulnerability: Comment input is not sanitized, allowing XSS.
patient['doctor_chat'] = comment  # No input sanitization here.
```
- **Mitigation**: Use libraries such as **html.escape** (Python) or **DOMPurify** (JavaScript) to sanitize user input before displaying it in the HTML template.

#### **IDOR in `/record/<patient_id>`:**
```python
@app.route('/record/<patient_id>')
def record(patient_id):
    # No authorization check, patient ID can be modified in the URL to access another patient's records.
    ...
```
- **Mitigation**: Check that the `patient_id` in the URL matches the logged-in user's `user_id` to prevent unauthorized access to other patients' records.

#### **CSV Injection in `/export`:**
```python
writer.writerow([patient['patient_id'], patient['name'], patient['notes'], patient['doctor_chat']])
# No input sanitization before exporting to CSV, allowing CSV Injection.
```
- **Mitigation**: Sanitize CSV data by escaping dangerous characters like `=`, `+`, `-`, and `@` to prevent them from being interpreted as formulas.

---

### **Conclusion**

This project demonstrates how seemingly simple web applications can be vulnerable to major security issues like XSS, IDOR, and CSV Injection if proper input sanitization and access controls are not implemented. In real-world systems, especially in sensitive sectors like healthcare, these vulnerabilities can have severe consequences, including data breaches, legal liabilities, and reputational damage.

**Next Steps**:
1. Implement proper input sanitization to prevent XSS and CSV Injection.
2. Enforce strict access controls to mitigate IDOR.
3. Conduct regular security audits and testing to detect and address vulnerabilities early.

This project serves as a practical example of why secure coding practices are critical in web application development, especially for applications that handle sensitive data like healthcare records.
