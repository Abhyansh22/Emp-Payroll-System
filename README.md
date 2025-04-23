💼 Employee Payroll Generation System
A simple GUI-based Payroll Management System built with Python, Tkinter, and MySQL. This system allows users to register employees, calculate their net salary, and generate payslips based on bonuses and deductions.

🚀 Features
Add new employee records

Calculate net salary using:
Net Salary = Base Salary + Bonuses - Deductions
Update employee details

Generate employee payslips

View a list of all registered employees

User-friendly GUI built with Tkinter

Persistent data storage using MySQL

🛠️ Technologies Used
Python 3.12+

Tkinter – for the graphical user interface

MySQL – for storing employee data

mysql-connector-python – for Python-MySQL integration

🏗️ Database Setup
The database and tables are created automatically when the program is first run:

Database: payroll_sys

Table: employees

sql
Copy
Edit
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(255),
    position VARCHAR(255),
    base_salary DECIMAL(10, 2),
    bonuses DECIMAL(10, 2) DEFAULT 0,
    deductions DECIMAL(10, 2) DEFAULT 0
);
▶️ Running the Application
Simply run the Python script:
This will launch the GUI application.

🧾 Sample Payslip Output

PaySlip for John Doe (Software Engineer)
-----------------------------------------------------
Base Salary: 50000.0
Bonuses: 5000.0
Deductions: 2000.0
-----------------------------------------------------
Net Salary: 53000.0

📂 Project Structure
<br>
├── payroll_app.py          # Main GUI and logic
<br>
├── README.md               # Project documentation
