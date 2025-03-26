import tkinter as tk
from tkinter import messagebox
import os
from csv import DictWriter

loan_types = [
    {"select": 0, "loan_type": "housing",  "interest_rate": 5.2, "max_term": 25},
    {"select": 1, "loan_type": "auto",     "interest_rate": 7.5, "max_term": 6},
    {"select": 2, "loan_type": "personal", "interest_rate": 9.6, "max_term": 10}
]

def calculate_installment(loan_amount, interest_rate, term):
    """Calculate monthly installment using the standard loan formula."""
    p = loan_amount
    r = interest_rate / (100 * 12)
    n = term * 12
    m = round((p * r * ((1 + r) ** n)) / (((1 + r) ** n) - 1), 2)
    return m

def debt_ratio(income, installment):
    """Ratio of monthly installment to monthly income."""
    return installment / income

def save_loan(loan_data):
    """Save loan details to a CSV file."""
    file_path = 'loan_records.csv'
    field_names = loan_data.keys()
    with open(file_path, 'a+', newline='') as file:
        writer = DictWriter(file, fieldnames=field_names)
        if file.tell() == 0:  
            writer.writeheader()
        writer.writerow(loan_data)

def process_loan_application(loan_type_name, monthly_income, loan_amount, term):
    """Validate loan inputs, calculate payment, and save data regardless of approval."""
    # Find the matching loan type data.
    loan_type = None
    for lt in loan_types:
        if lt["loan_type"] == loan_type_name.lower().split()[0]:
            loan_type = lt
            break

    # If loan type is invalid, record the attempt and return.
    if not loan_type:
        loan_data = {
            'loan_type':       loan_type_name,
            'loan_amount':     loan_amount,
            'interest_rate':   None,
            'term':            term,
            'monthly_payment': None,
            'total_interest':  None,
            'status':          'denied'
        }
        save_loan(loan_data)
        return False, "Invalid loan type."
    
    # Check term validity.
    if term <= 0 or term > loan_type["max_term"]:
        loan_data = {
            'loan_type':       loan_type["loan_type"],
            'loan_amount':     loan_amount,
            'interest_rate':   loan_type["interest_rate"],
            'term':            term,
            'monthly_payment': None,
            'total_interest':  None,
            'status':          'denied'
        }
        save_loan(loan_data)
        return False, f"Term must be between 1 and {loan_type['max_term']} years for {loan_type_name}."
    
    # Calculate monthly installment.
    interest_rate = loan_type["interest_rate"]
    installment = calculate_installment(loan_amount, interest_rate, term)
    
    # Check debt ratio.
    if debt_ratio(monthly_income, installment) > 0.5:
        loan_data = {
            'loan_type':       loan_type["loan_type"],
            'loan_amount':     loan_amount,
            'interest_rate':   interest_rate,
            'term':            term,
            'monthly_payment': installment,
            'total_interest':  None,
            'status':          'denied'
        }
        save_loan(loan_data)
        return False, "Your income is too low for this loan amount and term."
    
    # Loan approved; calculate total interest.
    total_interest = round(installment * term * 12 - loan_amount, 2)
    loan_data = {
        'loan_type':       loan_type["loan_type"],
        'loan_amount':     loan_amount,
        'interest_rate':   interest_rate,
        'term':            term,
        'monthly_payment': installment,
        'total_interest':  total_interest,
        'status':          'approved'
    }
    save_loan(loan_data)
    return True, loan_data

# Tkinter UI Functions

def show_results(success, result):
    """Clear the window and display loan results or error messages."""
    for widget in root.winfo_children():
        widget.destroy()
    
    if success:
        tk.Label(root, text="Loan Approved!", bg="#e6f0ff", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(root, text=f"Loan Type: {result['loan_type'].capitalize()}", bg="#e6f0ff").pack()
        tk.Label(root, text=f"Loan Amount: ${result['loan_amount']:.2f}", bg="#e6f0ff").pack()
        tk.Label(root, text=f"Interest Rate: {result['interest_rate']}%", bg="#e6f0ff").pack()
        tk.Label(root, text=f"Term: {result['term']} years", bg="#e6f0ff").pack()
        tk.Label(root, text=f"Monthly Payment: ${result['monthly_payment']:.2f}", bg="#e6f0ff").pack()
        tk.Label(root, text=f"Total Interest: ${result['total_interest']:.2f}", bg="#e6f0ff").pack()
        tk.Label(root, text=f"Status: {result['status'].capitalize()}", bg="#e6f0ff").pack(pady=10)
    else:
        tk.Label(root, text="Loan Application Failed", bg="#e6f0ff", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(root, text=result, fg="red", bg="#e6f0ff").pack()
    
    tk.Button(root, text="Start Over", command=show_loan_options, bg="#4d94ff", fg="white").pack(pady=10)

def submit_loan_application(loan_type, mi_entry, amount_entry, term_entry):
    """Collect user inputs, process the loan, and display results."""
    try:
        monthly_income = float(mi_entry.get())
        loan_amount = float(amount_entry.get())
        term = int(term_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")
        return
    
    success, result = process_loan_application(loan_type, monthly_income, loan_amount, term)
    show_results(success, result)

def show_loan_details(loan_type):
    """Display fields to input income, amount, and term for the selected loan type."""
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text=f"{loan_type} Selected", bg="#e6f0ff", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(root, text="Monthly Income ($):", bg="#e6f0ff").pack()
    mi_entry = tk.Entry(root)
    mi_entry.pack()
    tk.Label(root, text="Loan Amount ($):", bg="#e6f0ff").pack()
    amount_entry = tk.Entry(root)
    amount_entry.pack()
    
    max_term = 0
    for lt in loan_types:
        if lt["loan_type"] == loan_type.lower().split()[0]:
            max_term = lt["max_term"]
            break
    tk.Label(root, text=f"Term (years, max {max_term}):", bg="#e6f0ff").pack()
    term_entry = tk.Entry(root)
    term_entry.pack()
    
    tk.Button(root, text="Submit", bg="#4d94ff", fg="white",
              command=lambda: submit_loan_application(loan_type, mi_entry, amount_entry, term_entry)).pack(pady=5)
    tk.Button(root, text="Back to Loan Options", bg="#4d94ff", fg="white", command=show_loan_options).pack(pady=5)

def show_loan_options():
    """Display available loan types and a brief description."""
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Choose the type of loan", bg="#e6f0ff", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(root, text="Housing Loan: 5.2% interest rate, up to 25 years", bg="#e6f0ff").pack()
    tk.Label(root, text="Auto Loan: 7.5% interest rate, up to 6 years", bg="#e6f0ff").pack()
    tk.Label(root, text="Personal Loan: 9.6% interest rate, up to 10 years", bg="#e6f0ff").pack(pady=10)
    
    tk.Button(root, text="Housing Loan", bg="#4d94ff", fg="white",  
              command=lambda: show_loan_details("Housing Loan")).pack(pady=5)
    tk.Button(root, text="Auto Loan", bg="#4d94ff", fg="white",     
              command=lambda: show_loan_details("Auto Loan")).pack(pady=5)
    tk.Button(root, text="Personal Loan", bg="#4d94ff", fg="white", 
              command=lambda: show_loan_details("Personal Loan")).pack(pady=5)

def on_start_button_click():
    """Check if privacy is agreed; if yes, show loan options."""
    if privacy_var.get() == 1:
        show_loan_options()
    else:
        messagebox.showwarning("Privacy Policy", "Please agree to the Privacy Policy before proceeding.")

root = tk.Tk()
root.title("CS120 Loan Calculator")
root.configure(bg="#e6f0ff")

tk.Label(root, text="Welcome to CS120 Loans", bg="#e6f0ff", font=("Arial", 14, "bold")).pack(pady=10)
start_button = tk.Button(root, text="Start Loan Process", command=on_start_button_click, 
                         bg="#4d94ff", fg="white", relief=tk.RAISED)
start_button.pack(pady=5)
privacy_var = tk.IntVar(value=0)
privacy_check = tk.Checkbutton(root, text="Agree to Privacy Policy", variable=privacy_var, 
                               bg="#e6f0ff", selectcolor="#4d94ff")
privacy_check.pack(pady=5)
root.mainloop()
