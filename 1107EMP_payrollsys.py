import tkinter as tk
from tkinter import messagebox
import mysql.connector


class Employee:
    def __init__(self, employee_id, name, position, base_salary, bonuses=0, deductions=0):
        self.employee_id = employee_id
        self.name = name
        self.position = position
        self.base_salary = base_salary
        self.bonuses = bonuses
        self.deductions = deductions

    def calculate_net_salary(self):
        return self.base_salary + self.bonuses - self.deductions


class Payroll:
    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost',user='root',passwd='Admin@22')
        self.cursor = self.conn.cursor(buffered = True)
        self.conn.autocommit = True
        
        self.cursor.execute('create database if not exists payroll_sys')
        self.cursor.execute('use payroll_sys')
        #self.cursor.execute('drop table employees')
        self.cursor.execute('create table if not exists employees (employee_id INT PRIMARY KEY,name VARCHAR(255),position VARCHAR(255),base_salary DECIMAL(10, 2),bonuses DECIMAL(10, 2) DEFAULT 0,deductions DECIMAL(10, 2) DEFAULT 0)')
        self.conn = mysql.connector.connect(host='localhost',user='root',passwd='Admin@22',database='payroll_sys')
        self.cursor = self.conn.cursor(buffered = True)

    def add_employee(self, employee):
        query = ("INSERT INTO employees (employee_id, name, position, base_salary, bonuses, deductions) "
                 "VALUES (%s, %s, %s, %s, %s, %s)")
        data = (employee.employee_id, employee.name, employee.position, employee.base_salary, employee.bonuses, employee.deductions)
        self.cursor.execute(query, data)
        self.conn.commit()

    def update_employee(self, employee_id, **kwargs):
        for key, value in kwargs.items():
            query = f"UPDATE employees SET {key} = %s WHERE employee_id = %s"
            self.cursor.execute(query, (value, employee_id))
        self.conn.commit()

    def details(self):
        self.cursor.execute('select employee_id,name,position from employees')
        deta=self.cursor.fetchall()
        return deta

    def get_employee(self, employee_id):
        query = "SELECT * FROM employees WHERE employee_id = %s"
        self.cursor.execute(query, (employee_id,))
        row = self.cursor.fetchone()
        if row:
            return Employee(*row)
        return None

    def calculate_salary(self, employee_id):
        employee = self.get_employee(employee_id)
        if employee:
            return employee.calculate_net_salary()
        return None

    def generate_payslip(self, employee_id):
        employee = self.get_employee(employee_id)
        if employee:
            return PaySlip(employee)
        return None

    def close(self):
        self.cursor.close()
        self.conn.close()


class PaySlip:
    def __init__(self, employee):
        self.employee = employee

    def generate(self):
        details = f"""
        PaySlip for {self.employee.name} ({self.employee.position})
        -----------------------------------------------------
        Base Salary: {self.employee.base_salary}
        Bonuses: {self.employee.bonuses}
        Deductions: {self.employee.deductions}
        -----------------------------------------------------
        Net Salary: {self.employee.calculate_net_salary()}
        """
        return details.strip()


class PayrollApp:
    def __init__(self, root, payroll):
        self.root = root
        self.root.title("Payroll Management System")
        self.payroll = payroll

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        tk.Label(self.frame, text="Employee ID").grid(row=0, column=0)
        tk.Label(self.frame, text="Name").grid(row=1, column=0)
        tk.Label(self.frame, text="Position").grid(row=2, column=0)
        tk.Label(self.frame, text="Base Salary").grid(row=3, column=0)
        tk.Label(self.frame, text='Bonuses').grid(row=4,column=0)
        tk.Label(self.frame, text='Deductions').grid(row=5,column=0)

        # Entries
        self.employee_id_entry = tk.Entry(self.frame)
        self.employee_id_entry.grid(row=0, column=1)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=1, column=1)
        self.position_entry = tk.Entry(self.frame)
        self.position_entry.grid(row=2, column=1)
        self.base_salary_entry = tk.Entry(self.frame)
        self.base_salary_entry.grid(row=3, column=1)
        self.bonuses_entry = tk.Entry(self.frame)
        self.bonuses_entry.grid(row=4, column=1)
        self.deductions_entry = tk.Entry(self.frame)
        self.deductions_entry.grid(row=5, column=1)

        # Buttons
        self.add_employee_button = tk.Button(self.frame, text="Add Employee", command=self.add_employee)
        self.add_employee_button.grid(row=6, column=0, columnspan=1)

        self.generate_payslip_button = tk.Button(self.frame, text="Generate PaySlip", command=self.generate_payslip)
        self.generate_payslip_button.grid(row=6, column=1, columnspan=1)

        self.update_button = tk.Button(self.frame, text="Update Details", command=self.updatee)
        self.update_button.grid(row=7, column=0, columnspan=1)

        self.showw_button=tk.Button(self.frame, text='Show Employees', command=self.showw)
        self.showw_button.grid(row=7, column=1, columnspan=1)

        self.exitt_button=tk.Button(self.frame, text='Exit', command=self.exitt)
        self.exitt_button.grid(row=8, column=1, columnspan=1)

        
        self.payslip_text = tk.Text(root, height=10, width=65)
        self.payslip_text.pack(pady=10)
        
        
        self.edata=tk.Text(root, height = 10, width=50)
        self.edata.pack(pady=10)
        

    def add_employee(self):
        employee_id = int(self.employee_id_entry.get())
        name = self.name_entry.get()
        position = self.position_entry.get()
        base_salary = float(self.base_salary_entry.get())
        bonuses=float(self.bonuses_entry.get())
        deductions=float(self.deductions_entry.get())
        
        employee = Employee(employee_id, name, position, base_salary,bonuses,deductions)
        self.payroll.add_employee(employee)
        messagebox.showinfo("Success", "Employee added successfully")

    def generate_payslip(self):
        employee_id = int(self.employee_id_entry.get())
        payslip = self.payroll.generate_payslip(employee_id)
        if payslip:
            self.payslip_text.delete(1.0, tk.END)
            self.payslip_text.insert(tk.END, payslip.generate())
        else:
            messagebox.showerror("Error", "Employee not found")

    def showw(self):
        data = self.payroll.details()
        self.edata.delete(1.0, tk.END)
        self.edata.insert(tk.END, data)

    def updatee(self):
        self.payroll.update_employee(employee_id = int(self.employee_id_entry.get()), name = self.name_entry.get(), position = self.position_entry.get(), base_salary = float(self.base_salary_entry.get()), bonuses=float(self.bonuses_entry.get()), deductions=float(self.deductions_entry.get()))
        messagebox.showinfo("Success", "Employee details updated successfully")

    def exitt(self):
        self.payroll.close()
        root.destroy()


payroll = Payroll()

root = tk.Tk()
app = PayrollApp(root, payroll)
root.mainloop()

payroll.close()
