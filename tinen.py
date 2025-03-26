import tkinter as tk
from tkinter import messagebox
from csv import DictWriter
import os
from tabulate import tabulate

loan_mapping = {
    "Home Loan": {"loan_type": "housing", "interest_rate": 5.2, "max_term": 25},
    "Car Loan": {"loan_type": "auto", "interest_rate": 7.5, "max_term": 6},
    "Personal Loan": {"loan_type": "personal", "interest_rate": 9.6, "max_term": 10}
}

def calculate_installment(loan_amount, interest_rate, term):
    p = loan_amount
    r = interest_rate / (100 * 12)
    n = term * 12
    m = round((p * r * ((1 + r)**n)) / (((1 + r)**n) - 1), 2)
    return m

def debt_ratio(income, installment):
    return installment / income

def print_loan(loan_data):
    data_str = tabulate(loan_data.items(), tablefmt="plain")
    print(data_str)

def save_loan(loan_data):
    file_path = 'loan_records.csv'
    field_names = loan_data.keys()
    with open(file_path, 'a+', newline='') as file:
        writer = DictWriter(file, fieldnames=field_names)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(loan_data)
    print("Loan data saved to file.")

def show_loan_details(loan_type):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="#3498db")
    loan_info = loan_mapping[loan_type]
    title_label = tk.Label(root, text=f"{loan_type} Selected", font=("Helvetica", 16, "bold"), bg="#3498db")
    title_label.pack(pady=20)
    mi_label = tk.Label(root, text="Monthly Income", font=("Helvetica", 12), bg="#3498db")
    mi_label.pack(pady=5)
    mi_entry = tk.Entry(root, font=("Helvetica", 12))
    mi_entry.pack(pady=5)
    amount_label = tk.Label(root, text="Loan Amount", font=("Helvetica", 12), bg="#3498db")
    amount_label.pack(pady=5)
    amount_entry = tk.Entry(root, font=("Helvetica", 12))
    amount_entry.pack(pady=5)
    term_label = tk.Label(root, text="Term (years)", font=("Helvetica", 12), bg="#3498db")
    term_label.pack(pady=5)
    term_entry = tk.Entry(root, font=("Helvetica", 12))
    term_entry.pack(pady=5)
    
    def process_loan():
        try:
            income = float(mi_entry.get())
            if income <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Enter a valid positive monthly income")
            return
        try:
            loan_amount = float(amount_entry.get())
            if loan_amount <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Enter a valid positive loan amount")
            return
        try:
            term = int(term_entry.get())
            if term <= 0 or term > loan_info["max_term"]:
                messagebox.showerror("Error", f"The maximum term for {loan_type} is {loan_info['max_term']} years")
                return
        except:
            messagebox.showerror("Error", "Enter a valid integer term")
            return
        installment = calculate_installment(loan_amount, loan_info["interest_rate"], term)
        if debt_ratio(income, installment) > 0.5:
            messagebox.showwarning("Loan Denied", "Your income is too low for this loan amount and term")
        else:
            total_interest = round(installment * term * 12 - loan_amount, 2)
            loan_data = {'loan_type': loan_info["loan_type"],
                         'loan_amount': loan_amount,
                         'interest_rate': loan_info["interest_rate"],
                         'term': term,
                         'monthly_payment': installment,
                         'total_interest': total_interest,
                         'status': 'approved'}
            print_loan(loan_data)
            save_loan(loan_data)
            messagebox.showinfo("Loan Approved", f"Loan approved. Monthly payment: {installment}")
    
    loan_submit = tk.Button(root, text="Submit", command=process_loan,
                            font=("Helvetica", 12, "bold"), bg="white", fg="#3498db",
                            activebackground="#2980b9", activeforeground="white", relief="flat", bd=0)
    loan_submit.pack(padx=20, pady=10)

def show_loan_options():
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="#3498db")
    title_label = tk.Label(root, text="Choose the type of loan", font=("Helvetica", 16, "bold"), bg="#3498db")
    title_label.pack(pady=20)
    home_button = tk.Button(root, text="Housing Loan", command=lambda: show_loan_details("Home Loan"),
                             font=("Helvetica", 12, "bold"), bg="white", fg="#3498db",
                             activebackground="#2980b9", activeforeground="white", relief="flat", bd=0)
    home_button.pack(padx=20, pady=10)
    car_button = tk.Button(root, text="Auto Loan", command=lambda: show_loan_details("Car Loan"),
                            font=("Helvetica", 12, "bold"), bg="white", fg="#3498db",
                            activebackground="#2980b9", activeforeground="white", relief="flat", bd=0)
    car_button.pack(padx=20, pady=10)
    personal_button = tk.Button(root, text="Personal Loan", command=lambda: show_loan_details("Personal Loan"),
                                font=("Helvetica", 12, "bold"), bg="white", fg="#3498db",
                                activebackground="#2980b9", activeforeground="white", relief="flat", bd=0)
    personal_button.pack(padx=20, pady=10)

def on_button_click():
    if privacy_var.get() == 1:
        show_loan_options()
    else:
        messagebox.showwarning("Privacy Policy", "Please agree to the Privacy Policy before proceeding.")

root = tk.Tk()
root.configure(bg="#3498db")
title_label = tk.Label(root, text="Welcome to CS120 Loans", font=("Helvetica", 16, "bold"), bg="#3498db")
title_label.pack(pady=20)
button = tk.Button(root, text="Start Loan Process", command=on_button_click,
                   font=("Helvetica", 12, "bold"), bg="white", fg="#3498db",
                   activebackground="#2980b9", activeforeground="white", relief="flat", bd=0)
button.pack(padx=20, pady=10)
privacy_var = tk.IntVar(value=0)
privacy_check = tk.Checkbutton(root, text="Agree to Privacy Policy", variable=privacy_var,
                               bg="#3498db", fg="white", font=("Helvetica", 12))
privacy_check.pack(pady=10)

root.mainloop()
