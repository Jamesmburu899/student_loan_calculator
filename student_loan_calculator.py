import math
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def calculate_monthly_payment(loan_amount, interest_rate, loan_term):
    """
    Calculates the monthly payment for a loan using the amortization formula.

    Parameters:
        loan_amount (float): The total loan amount.
        interest_rate (float): The annual interest rate (in percentage).
        loan_term (int): The loan term in years.

    Returns:
        float: The calculated monthly payment.
    """
    monthly_interest_rate = interest_rate / 100 / 12
    loan_term_months = loan_term * 12
    
    if monthly_interest_rate == 0:
        return loan_amount / loan_term_months
    else:
        monthly_payment = (loan_amount * monthly_interest_rate) / (1 - math.pow(1 + monthly_interest_rate, -loan_term_months))
        return monthly_payment

def validate_inputs(loan_amount, interest_rate, loan_term):
    """
    Validates the user input to ensure they are positive numbers.

    Parameters:
        loan_amount (float): The total loan amount.
        interest_rate (float): The annual interest rate (in percentage).
        loan_term (int): The loan term in years.

    Returns:
        bool: True if inputs are valid, False otherwise.
    """
    if loan_amount <= 0 or interest_rate < 0 or loan_term <= 0:
        return False
    return True

def format_payment_result(payment):
    """
    Formats the calculated monthly payment to two decimal places.

    Parameters:
        payment (float): The monthly payment to be formatted.

    Returns:
        str: The formatted monthly payment.
    """
    return f"${payment:.2f}"

def calculate_amortization_schedule(loan_amount, interest_rate, loan_term, extra_payment=0):
    """
    Calculates the amortization schedule with extra payments included.

    Parameters:
        loan_amount (float): The total loan amount.
        interest_rate (float): The annual interest rate (in percentage).
        loan_term (int): The loan term in years.
        extra_payment (float): The extra payment added to the monthly payment.

    Returns:
        list of dict: The amortization schedule with month-wise details.
    """
    monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
    monthly_interest_rate = interest_rate / 100 / 12
    loan_balance = loan_amount
    schedule = []
    total_interest_paid = 0

    while loan_balance > 0:
        interest_payment = loan_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment + extra_payment
        if loan_balance < principal_payment:
            principal_payment = loan_balance
        loan_balance -= principal_payment
        total_interest_paid += interest_payment

        schedule.append({
            "month": len(schedule) + 1,
            "payment": monthly_payment + extra_payment,
            "interest_payment": interest_payment,
            "principal_payment": principal_payment,
            "balance": loan_balance,
        })

    return schedule, total_interest_paid

def plot_amortization_schedule(schedule):
    """
    Plots the loan amortization schedule.

    Parameters:
        schedule (list): The amortization schedule containing monthly details.
    """
    months = [entry['month'] for entry in schedule]
    balances = [entry['balance'] for entry in schedule]

    plt.figure(figsize=(10, 6))
    plt.plot(months, balances, label="Remaining Loan Balance")
    plt.xlabel("Month")
    plt.ylabel("Loan Balance ($)")
    plt.title("Loan Amortization Schedule")
    plt.grid(True)
    plt.legend()
    plt.show()

def display_amortization_schedule(schedule):
    """
    Displays the amortization schedule in a readable format.

    Parameters:
        schedule (list): The amortization schedule containing monthly details.
    """
    print(f"{'Month':<10}{'Payment':<15}{'Interest Payment':<20}{'Principal Payment':<20}{'Balance':<15}")
    for entry in schedule:
        print(f"{entry['month']:<10}{entry['payment']:<15.2f}{entry['interest_payment']:<20.2f}{entry['principal_payment']:<20.2f}{entry['balance']:<15.2f}")

def get_user_input():
    """
    Prompts the user to input the loan amount, interest rate, and loan term.

    Returns:
        tuple: A tuple containing loan amount, interest rate, and loan term.
    """
    try:
        loan_amount = float(entry_loan_amount.get())
        interest_rate = float(entry_interest_rate.get())
        loan_term = int(entry_loan_term.get())
        extra_payment = float(entry_extra_payment.get())
        
        if validate_inputs(loan_amount, interest_rate, loan_term):
            return loan_amount, interest_rate, loan_term, extra_payment
        else:
            messagebox.showerror("Input Error", "All values must be greater than zero.")
            return None
    except ValueError:
        messagebox.showerror("Input Error", "Please enter numeric values.")
        return None

def calculate_and_display():
    """
    Calculates the monthly payment and displays the amortization schedule.
    """
    user_input = get_user_input()
    if user_input:
        loan_amount, interest_rate, loan_term, extra_payment = user_input
        monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
        formatted_payment = format_payment_result(monthly_payment)
        
        # Determine the selected option
        if selected_option.get() == "Option 1":  # Standard amortization
            schedule, total_interest_paid = calculate_amortization_schedule(loan_amount, interest_rate, loan_term)
        else:  # Option 2: Extra payments
            schedule, total_interest_paid = calculate_amortization_schedule(loan_amount, interest_rate, loan_term, extra_payment)
        
        display_amortization_schedule(schedule)

        # Display final results in the GUI
        result_label.config(text=f"Monthly Payment: {formatted_payment}\nTotal Interest Paid: ${total_interest_paid:.2f}")
        
        # Plot the amortization graph
        plot_amortization_schedule(schedule)

# GUI setup
root = tk.Tk()
root.title("Student Loan Payment Calculator")

# Labels and entry fields
tk.Label(root, text="Loan Amount ($):").grid(row=0, column=0, padx=10, pady=5)
entry_loan_amount = tk.Entry(root)
entry_loan_amount.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Annual Interest Rate (%):").grid(row=1, column=0, padx=10, pady=5)
entry_interest_rate = tk.Entry(root)
entry_interest_rate.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Loan Term (Years):").grid(row=2, column=0, padx=10, pady=5)
entry_loan_term = tk.Entry(root)
entry_loan_term.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Extra Monthly Payment ($):").grid(row=3, column=0, padx=10, pady=5)
entry_extra_payment = tk.Entry(root)
entry_extra_payment.grid(row=3, column=1, padx=10, pady=5)

# Option selection
selected_option = tk.StringVar(value="Option 1")  # Default option is Option 1
tk.Radiobutton(root, text="Standard Amortization (Option 1)", variable=selected_option, value="Option 1").grid(row=4, columnspan=2)
tk.Radiobutton(root, text="Extra Payments (Option 2)", variable=selected_option, value="Option 2").grid(row=5, columnspan=2)

# Calculate button
tk.Button(root, text="Calculate Payment and Amortization", command=calculate_and_display).grid(row=6, columnspan=2, pady=10)

# Label for result display
result_label = tk.Label(root, text="Monthly Payment will appear here.", font=("Arial", 12))
result_label.grid(row=7, columnspan=2)

root.mainloop()


