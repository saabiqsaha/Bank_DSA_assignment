import tkinter as tk
from tkinter import messagebox
import os
from csv import DictWriter

# Loan types data
loan_types = [
    {"select": 0, "loan_type": "housing", "interest_rate": 5.2, "max_term": 25},
    {"select": 1, "loan_type": "auto", "interest_rate": 7.5, "max_term": 6},
    {"select": 2, "loan_type": "personal", "interest_rate": 9.6, "max_term": 10}
]

def calculate_installment(loan_amount, interest_rate, term):
    p = loan_amount
    r = interest_rate/(100*12)
    n = term*12
    m = round((p * r * ((1+r)**n))/((1+r)**n -1), 2)
    return m

def debt_ratio(income, installment):
    return installment/income

def save_loan(loan_data):
    file_path = 'loan_records.csv'
    field_names = loan_data.keys()

    with open(file_path, 'a+', newline='') as file:
        writer = DictWriter(file, fieldnames=field_names)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(loan_data)

def process_loan_application(loan_type_name, monthly_income, loan_amount, term):
    # Find the loan type in our data
    loan_type = None
    for lt in loan_types:
        if lt["loan_type"] == loan_type_name.lower().split()[0]:  # Extract first word and convert to lowercase
            loan_type = lt
            break
    
    if not loan_type:
        return False, "Invalid loan type"
    
    # Validate term
    if term <= 0 or term > loan_type["max_term"]:
        return False, f"Term must be between 1 and {loan_type['max_term']} years for {loan_type_name}"
    
    # Calculate installment
    interest_rate = loan_type["interest_rate"]
    installment = calculate_installment(loan_amount, interest_rate, term)
    
    # Check debt ratio
    ratio = debt_ratio(monthly_income, installment)
    if ratio > 0.5:
        return False, "Your income is too low for this loan amount and term"
    
    # Calculate total interest
    total_interest = round(installment * term * 12 - loan_amount, 2)
    
    # Create loan data dictionary
    loan_data = {
        'loan_type': loan_type["loan_type"],
        'loan_amount': loan_amount,
        'interest_rate': interest_rate,
        'term': term,
        'monthly_payment': installment,
        'total_interest': total_interest,
        'status': 'approved'
    }
    
    # Save loan data
    save_loan(loan_data)
    
    return True, loan_data

def show_results(success, result):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="#3498db")
    
    if success:
        title_label = tk.Label(root, text="Loan Approved!", font=("Helvetica", 16, "bold"), bg="#3498db")
        title_label.pack(pady=20)
        
        # Display loan details
        details_frame = tk.Frame(root, bg="#3498db")
        details_frame.pack(pady=10)
        
        details = [
            f"Loan Type: {result['loan_type'].capitalize()}",
            f"Loan Amount: ${result['loan_amount']:,.2f}",
            f"Interest Rate: {result['interest_rate']}%",
            f"Term: {result['term']} years",
            f"Monthly Payment: ${result['monthly_payment']:,.2f}",
            f"Total Interest: ${result['total_interest']:,.2f}",
            f"Status: {result['status'].capitalize()}"
        ]
        
        for detail in details:
            detail_label = tk.Label(details_frame, text=detail, font=("Helvetica", 12), bg="#3498db", anchor="w")
            detail_label.pack(pady=5, fill="x")
    else:
        title_label = tk.Label(root, text="Loan Application Failed", font=("Helvetica", 16, "bold"), bg="#3498db")
        title_label.pack(pady=20)
        
        error_label = tk.Label(root, text=result, font=("Helvetica", 12), bg="#3498db", fg="red")
        error_label.pack(pady=10)
    
    # Add a button to start over
    restart_button = tk.Button(root, text="Start Over", command=show_loan_options,
                            font=("Helvetica", 12, "bold"), bg="white", fg="#3498db",
                            activebackground="#2980b9", activeforeground="white", relief="flat", bd=0)
    restart_button.pack(padx=20, pady=20)

def submit_loan_application(loan_type, mi_entry, amount_entry, term_entry):
    try:
        monthly_income = float(mi_entry.get())
        loan_amount = float(amount_entry.get())
        term = int(term_entry.get())
        
        if monthly_income <= 0:
            messagebox.showerror("Input Error", "Monthly income must be a positive number")
            return
        
        if loan_amount <= 0:
            messagebox.showerror("Input Error", "Loan amount must be a positive number")
            return
        
        if term <= 0:
            messagebox.showerror("Input Error", "Term must be a positive integer")
            return
        
        success, result = process_loan_application(loan_type, monthly_income, loan_amount, term)
        show_results(success, result)
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for all fields")

def show_loan_details(loan_type):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="#3498db")
    
    # Find the loan type in our data to get max term
    max_term = 0
    for lt in loan_types:
        if lt["loan_type"] == loan_type.lower().split()[0]:  # Extract first word and convert to lowercase
            max_term = lt["max_term"]
            break
    
    title_label = tk.Label(root, text=f"{loan_type} Selected", font=("Helvetica", 16, "bold"), bg="#3498db")
    title_label.pack(pady=20)
    
    mi_label = tk.Label(root, text="Monthly Income ($)", font=("Helvetica", 12), bg="#3498db")
    mi_label.pack(pady=5)
    mi_entry = tk.Entry(root, font=("Helvetica", 12))
    mi_entry.pack(pady=5)
    
    amount_label = tk.Label(root, text="Loan Amount ($)", font=("Helvetica", 12), bg="#3498db")
    amount_label.pack(pady=5)
    amount_entry = tk.Entry(root, font=("Helvetica", 12))
    amount_entry.pack(pady=5)
    
    term_label = tk.Label(root, text=f"Term (years, max {max_term})", font=("Helvetica", 12), bg="#3498db")
    term_label.pack(pady=5)
    term_entry = tk.Entry(root, font=("Helvetica", 12))
    term_entry.pack(pady=5)
    
    loan_submit = tk.Button(root, text="Submit", 
                           command=lambda: submit_loan_application(loan_type, mi_entry, amount_entry, term_entry),
                           font=("Helvetica", 12, "bold"), bg="white", fg="#3498db",
                           activebackground="#2980b9", activeforeground="white", relief="flat", bd=0)
    loan_submit.pack(padx=20, pady=10)
    
    back_button = tk.Button(root, text="Back to Loan Options", command=show_loan_options,
                           font=("Helvetica", 12, "bold"), bg="white", fg="#3498db",
                           activebackground="#2980b9", activeforeground="white", relief="flat", bd=0)
    back_button.pack(padx=20, pady=10)

def show_loan_options():
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="#3498db")
    title_label = tk.Label(root, text="Choose the type of loan", font=("Helvetica", 16, "bold"), bg="#3498db")
    title_label.pack(pady=20)
    
    # Add description of loan types
    description_frame = tk.Frame(root, bg="#3498db")
    description_frame.pack(pady=10)
    
    descriptions = [
        "Housing Loan: 5.2% interest rate, term up to 25 years",
        "Auto Loan: 7.5% interest rate, term up to 6 years",
        "Personal Loan: 9.6% interest rate, term up to 10 years"
    ]
    
    for desc in descriptions:
        desc_label = tk.Label(description_frame, text=desc, font=("Helvetica", 10), bg="#3498db")
        desc_label.pack(pady=2)
    
    home_button = tk.Button(root, text="Housing Loan", command=lambda: show_loan_details("Housing Loan"),
                           font=("Helvetica", 12, "bold"), bg="white", fg="#3498db",
                           activebackground="#2980b9", activeforeground="white", relief="flat", bd=0)
    home_button.pack(padx=20, pady=10)
    
    car_button = tk.Button(root, text="Auto Loan", command=lambda: show_loan_details("Auto Loan"),
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

# Initialize the main window
root = tk.Tk()
root.title("CS120 Loan Calculator")
root.geometry("500x600")  # Set a reasonable window size
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
