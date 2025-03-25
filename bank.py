# loans
from tabulate import tabulate

'''Allow the user to:
o Select the type of loan.
o Enter the loan amount.
o Specify the term (within the allowable limits for the selected loan).
o Enter their monthly income to check debt ratio complian
'''

# dict for loan types
'''Housing Loan: 5.2% interest rate, term up to 25 years.
 Auto Loan: 7.5% interest rate, term up to 6 years.
 Personal Loan: 9.6% interest rate, term up to 10 years'''

loan_types = [
    {"select": 0,"type": "housing", "interest_rate": 5.2, "max_term": 25},
    {"select": 1,"type": "auto", "interest_rate": 7.5, "max_term": 6},
    {"select": 2,"type": "personal", "interest_rate": 9.6, "max_term": 10}
]

# save loan data here for printing and file
loan_data = {}
def valid_amount(instruction):
    # make sure amount is a positive real number
    while True:
        try:
            amount = float(input(instruction))
            
            if amount > 0:
                break
            else:
                print("Enter a positive")
        except ValueError:
            print("Enter a positive real number")
    return amount

def valid_term(loan_type):
    max_term = loan_type["max_term"]
    while True:
        try:
            term = int(input("Enter The term in years: ").strip())
            if term in range(max_term + 1):
                return term
            else:
                print(f"The maximum term for {loan_type["loan_type"]} loan is {max_term}")
        except ValueError:
            print("Enter a vaid integer")

def main():
    # select loan type
    options = tabulate(loan_types, headers = "keys")
    print(options)
    while True:
        try:
            choice = int(input("select a loan type based on the corresponding number: ").strip().upper())
            if choice in range(3):
                loan_type = loan_types[choice]
                break
            else:
                print("select numbers 0 to 2 to choose a loan type: ")
        except ValueError:
            print("please enter a valid integer")

    # Enter income
    income = valid_amount("Please enter your monthly income: ")
    # select loan amount
    
    loan_amount = valid_amount("Please enter your loan amount: ")


    # select term, whithin loan type limit (in years or months?)
    term = valid_term(loan_types[choice])

    interest_rate = loan_types[choice]["interest_rate"]

    installment = calculate_installment(loan_amount, interest_rate, term)
    
    if debt_ratio(installment, income) > 0.5:
        print("Your income is too low for this loan amount and term")
    else:
        print_loan(loan_data)
        # into a file Loan Type, Loan Amount, Interest Rate, Term, Monthly Payment, Total Interest,Status
        save_loan(loan_data)


def calculate_installment(loan_amount, interest_rate, term):
    p = loan_amount
    r = interest_rate/(100*12)
    n = term*12

    m = (p * r * ((1+r)**n))/((1+r)**n -1)
    print(m)
    return m

def debt_ratio(income, installment):
    return installment/income

def print_loan(loan_data):
    pass

def save_loan(loan_data):
    pass

main()
