
from bank import Bank
from utils import read_amount, pause, line, title


ADMIN_PASSWORD = "bankadmin123"


def create_account_menu(bank):
    title("OPEN A NEW BANK ACCOUNT")

    name = input("Full name: ").strip()
    phone = input("Phone number: ").strip()
    email = input("Email address: ").strip()
    pin = input("Create a 4-digit PIN: ").strip()

    print("\n1. Savings Account")
    print("2. Current Account")
    account_type = input("Select account type: ").strip()

    if account_type not in ("1", "2"):
        print("Invalid account type.")
        return

    amount = read_amount("Opening deposit (Rs.): ", allow_zero=True)

    if amount is None:
        return

    try:
        account = bank.create_account(
            name, phone, email, pin, account_type, amount
        )

        print("\nAccount created successfully.")
        print("Account Number:", account.account_number)
        print("Account Holder:", account.name)
        print("Account Type:", account.account_type)
        print(f"Opening Balance: Rs. {account.balance:.2f}")

    except (ValueError, RuntimeError) as error:
        print("Could not create account:", error)


def customer_login(bank):
    title("CUSTOMER LOGIN")

    account_number = input("Account number: ").strip()
    pin = input("Enter your 4-digit PIN: ").strip()

    account = bank.authenticate(account_number, pin)

    if account is None:
        print("Invalid account number, PIN, or inactive account.")
        return None

    print("Login successful. Welcome,", account.name)
    return account


def customer_menu(bank):
    account = customer_login(bank)

    if account is None:
        return

    while True:
        title("CUSTOMER DASHBOARD")
        print("1. Account Overview")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Transaction History")
        print("6. Download Account Statement")
        print("7. Change PIN")
        print("8. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            bank.show_account(account)

        elif choice == "2":
            amount = read_amount("Deposit amount (Rs.): ")
            if amount is not None:
                bank.deposit(account, amount)

        elif choice == "3":
            amount = read_amount("Withdrawal amount (Rs.): ")
            if amount is not None:
                bank.withdraw(account, amount)

        elif choice == "4":
            recipient = input("Recipient account number: ").strip()
            amount = read_amount("Transfer amount (Rs.): ")

            if amount is not None:
                bank.transfer(account, recipient, amount)

        elif choice == "5":
            bank.show_history(account)

        elif choice == "6":
            path = bank.export_statement(account)
            if path:
                print("Statement saved to:", path)
            else:
                print("Unable to export statement.")

        elif choice == "7":
            old_pin = input("Current PIN: ").strip()
            new_pin = input("New 4-digit PIN: ").strip()

            try:
                bank.change_pin(account, old_pin, new_pin)
                print("PIN changed successfully.")
            except (ValueError, RuntimeError) as error:
                print("Unable to change PIN:", error)

        elif choice == "8":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice.")

        pause()


def staff_login():
    title("STAFF AUTHENTICATION")
    password = input("Enter staff password: ")

    if password == ADMIN_PASSWORD:
        print("Staff authentication successful.")
        return True

    print("Access denied. Incorrect password.")
    return False


def staff_menu(bank):
    if not staff_login():
        return

    while True:
        title("STAFF / ADMIN DASHBOARD")
        print("1. View All Bank Accounts")
        print("2. Search an Account")
        print("3. Sort Accounts by Balance")
        print("4. View Recent Transactions")
        print("5. Bank Summary and Statistics")
        print("6. Freeze or Unfreeze Account")
        print("7. Export Accounts to CSV")
        print("8. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            bank.list_accounts()

        elif choice == "2":
            number = input("Enter account number: ").strip()
            account = bank.find_account(number)

            if account:
                bank.show_account(account)
            else:
                print("Account not found.")

        elif choice == "3":
            bank.sort_accounts()

        elif choice == "4":
            bank.show_recent_transactions()

        elif choice == "5":
            bank.show_summary()

        elif choice == "6":
            number = input("Enter account number: ").strip()

            try:
                bank.toggle_account_status(number)
                print("Account status updated successfully.")
            except ValueError as error:
                print(error)

        elif choice == "7":
            path = bank.export_accounts()

            if path:
                print("Account report saved to:", path)
            else:
                print("Unable to export account report.")

        elif choice == "8":
            break

        else:
            print("Invalid choice.")

        pause()


def authenticated_account(bank):
    print("\nPlease authenticate to continue.")
    return customer_login(bank)


def direct_deposit(bank):
    account = authenticated_account(bank)

    if account is None:
        return

    amount = read_amount("Deposit amount (Rs.): ")

    if amount is not None:
        bank.deposit(account, amount)


def direct_withdrawal(bank):
    account = authenticated_account(bank)

    if account is None:
        return

    amount = read_amount("Withdrawal amount (Rs.): ")

    if amount is not None:
        bank.withdraw(account, amount)


def direct_transfer(bank):
    account = authenticated_account(bank)

    if account is None:
        return

    recipient = input("Recipient account number: ").strip()
    amount = read_amount("Transfer amount (Rs.): ")

    if amount is not None:
        bank.transfer(account, recipient, amount)


def direct_balance_check(bank):
    account = authenticated_account(bank)

    if account is not None:
        print("\nAccount Number:", account.account_number)
        print("Account Holder:", account.name)
        print(f"Available Balance: Rs. {account.balance:.2f}")


def direct_transaction_history(bank):
    account = authenticated_account(bank)

    if account is not None:
        bank.show_history(account)


def main():
    bank = Bank()

    while True:
        title("BANKING MANAGEMENT SYSTEM")
        print(" 1. Open a New Bank Account")
        print(" 2. Customer Login")
        print(" 3. Staff / Admin Login")
        print(" 4. Search Account by Account Number")
        print(" 5. View All Bank Accounts")
        print(" 6. Deposit Money")
        print(" 7. Withdraw Money")
        print(" 8. Transfer Money")
        print(" 9. Check Account Balance")
        print("10. View Transaction History")
        print("11. Sort Accounts by Balance")
        print("12. Bank Summary and Statistics")
        print("13. Export Reports to CSV")
        print("14. View Recent Transactions")
        print("15. Save Data")
        print("16. Save and Exit")

        line()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_account_menu(bank)
            pause()

        elif choice == "2":
            customer_menu(bank)

        elif choice == "3":
            staff_menu(bank)

        elif choice == "4":
            number = input("Enter account number: ").strip()
            account = bank.find_account(number)

            if account:
                print("Account found.")
                print("Account Number:", account.account_number)
                print("Account Holder:", account.name)
                print("Account Type:", account.account_type)
                print("Status:", account.status)
            else:
                print("Account not found.")

            pause()

        elif choice == "5":
            if staff_login():
                bank.list_accounts()
            pause()

        elif choice == "6":
            direct_deposit(bank)
            pause()

        elif choice == "7":
            direct_withdrawal(bank)
            pause()

        elif choice == "8":
            direct_transfer(bank)
            pause()

        elif choice == "9":
            direct_balance_check(bank)
            pause()

        elif choice == "10":
            direct_transaction_history(bank)
            pause()

        elif choice == "11":
            if staff_login():
                bank.sort_accounts()
            pause()

        elif choice == "12":
            if staff_login():
                bank.show_summary()
            pause()

        elif choice == "13":
            if staff_login():
                print("\n1. Export all accounts")
                print("2. Export an account statement")
                report_choice = input("Choose report type: ").strip()

                if report_choice == "1":
                    path = bank.export_accounts()
                elif report_choice == "2":
                    number = input("Enter account number: ").strip()
                    account = bank.find_account(number)
                    path = bank.export_statement(account) if account else None
                else:
                    path = None
                    print("Invalid report type.")

                if path:
                    print("Report saved to:", path)
                elif report_choice in ("1", "2"):
                    print("Unable to create report.")

            pause()

        elif choice == "14":
            if staff_login():
                bank.show_recent_transactions()
            pause()

        elif choice == "15":
            if bank.save():
                print("All data saved successfully.")
            else:
                print("Unable to save data. Check your data folder.")
            pause()

        elif choice == "16":
            if bank.save():
                print("All records saved successfully.")
                print("Thank you for using the Banking Management System.")
                break

            print("Save failed. The application will remain open.")
            pause()

        else:
            print("Invalid choice. Please enter a number from 1 to 16.")
            pause()


if __name__ == "__main__":
    main()
