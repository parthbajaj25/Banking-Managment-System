from datetime import datetime
from collections import deque
from models import BankAccount, SavingsAccount, CurrentAccount, account_from_dict
from storage import Storage


class Bank:
    def __init__(self):
        self.storage = Storage()
        saved = self.storage.load()
        self.accounts = {}
        self.transactions = list(saved["transactions"])
        self.recent_transactions = deque(self.transactions[-10:], maxlen=10)

        for item in saved["accounts"]:
            account = account_from_dict(item)
            self.accounts[account.account_number] = account

    def save(self):
        data = {
            "accounts": [account.to_dict() for account in self.accounts.values()],
            "transactions": self.transactions
        }
        return self.storage.save(data)

    def create_account(self, name, phone, email, pin, account_type, initial_deposit):
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        if not phone.strip():
            raise ValueError("Phone number cannot be empty.")
        if not pin.isdigit() or len(pin) != 4:
            raise ValueError("PIN must contain exactly four digits.")
        if initial_deposit < 0:
            raise ValueError("Opening deposit cannot be negative.")
        if account_type not in ("1", "2"):
            raise ValueError("Invalid account type.")

        number = str(max([int(key) for key in self.accounts if key.isdigit()] or [100000]) + 1)
        cls = CurrentAccount if account_type == "2" else SavingsAccount
        account = cls(number, name.strip(), phone.strip(), email.strip(), pin, initial_deposit)
        self.accounts[number] = account

        if initial_deposit > 0:
            self.record(number, "Opening Deposit", initial_deposit, "Account opened")
        if not self.save():
            self.accounts.pop(number, None)
            raise RuntimeError("Could not save the new account.")
        return account

    def find_account(self, account_number):
        return self.accounts.get(str(account_number))

    def authenticate(self, account_number, pin):
        account = self.find_account(account_number)
        if account and account.verify_pin(pin) and account.status == "Active":
            return account
        return None

    def record(self, account_number, kind, amount, details=""):
        item = {
            "transaction_id": "TXN" + datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "account_number": str(account_number),
            "type": kind,
            "amount": round(float(amount), 2),
            "details": details
        }
        self.transactions.append(item)
        self.recent_transactions.append(item)

    def deposit(self, account, amount):
        try:
            account.deposit(amount)
            self.record(account.account_number, "Deposit", amount)
            if not self.save():
                raise RuntimeError("Deposit changed in memory but saving failed. Do not close the app; check storage.")
            print(f"Deposit successful. New balance: Rs. {account.balance:.2f}")
        except ValueError as error:
            print(error)

    def withdraw(self, account, amount):
        try:
            account.withdraw(amount)
            self.record(account.account_number, "Withdrawal", amount)
            if not self.save():
                raise RuntimeError("Withdrawal changed in memory but saving failed. Do not close the app; check storage.")
            print(f"Withdrawal successful. New balance: Rs. {account.balance:.2f}")
        except ValueError as error:
            print(error)

    def transfer(self, sender, recipient_number, amount):
        recipient = self.find_account(recipient_number)
        if not recipient:
            print("Recipient account not found.")
            return
        if recipient.account_number == sender.account_number:
            print("You cannot transfer to the same account.")
            return
        if sender.status != "Active" or recipient.status != "Active":
            print("Both accounts must be active.")
            return
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
        if amount > sender.balance:
            print("Insufficient balance.")
            return

        old_sender = sender.balance
        old_recipient = recipient.balance
        old_count = len(self.transactions)
        sender.balance = round(sender.balance - amount, 2)
        recipient.balance = round(recipient.balance + amount, 2)
        self.record(sender.account_number, "Transfer Sent", amount, f"To {recipient.account_number}")
        self.record(recipient.account_number, "Transfer Received", amount, f"From {sender.account_number}")

        if not self.save():
            sender.balance = old_sender
            recipient.balance = old_recipient
            self.transactions = self.transactions[:old_count]
            self.recent_transactions = deque(self.transactions[-10:], maxlen=10)
            print("Transfer cancelled because records could not be saved.")
            return
        print(f"Transfer successful. New balance: Rs. {sender.balance:.2f}")

    def show_account(self, account):
        print("\nACCOUNT OVERVIEW")
        print("-" * 42)
        print("Account number :", account.account_number)
        print("Name           :", account.name)
        print("Phone          :", account.phone)
        print("Email          :", account.email or "Not provided")
        print("Account type   :", account.account_type)
        print("Status         :", account.status)
        print("Created on     :", account.created_at)
        print(f"Balance        : Rs. {account.balance:.2f}")
        print(f"Indicative annual interest: Rs. {account.calculate_interest():.2f}")
        print("-" * 42)

    def show_history(self, account):
        history = [item for item in self.transactions if item["account_number"] == account.account_number]
        if not history:
            print("No transactions found.")
            return
        print("\nTRANSACTION HISTORY")
        for item in history:
            print(
                f"{item['timestamp']} | {item['transaction_id']} | "
                f"{item['type']} | Rs. {item['amount']:.2f} | {item['details']}"
            )

    def list_accounts(self):
        if not self.accounts:
            print("No accounts available.")
            return
        print(f"\n{'Account':<12}{'Name':<24}{'Type':<12}{'Status':<12}{'Balance':>12}")
        print("-" * 72)
        for account in self.accounts.values():
            print(f"{account.account_number:<12}{account.name[:22]:<24}{account.account_type:<12}{account.status:<12}{account.balance:>12.2f}")

    def sort_accounts(self):
        for account in sorted(self.accounts.values(), key=lambda item: item.balance, reverse=True):
            print(f"{account.account_number} | {account.name} | Rs. {account.balance:.2f}")

    def show_recent_transactions(self):
        if not self.recent_transactions:
            print("No transactions available.")
            return
        for item in reversed(self.recent_transactions):
            print(f"{item['timestamp']} | {item['account_number']} | {item['type']} | Rs. {item['amount']:.2f}")

    def show_summary(self):
        total_balance = sum(account.balance for account in self.accounts.values())
        savings = sum(account.account_type == "Savings" for account in self.accounts.values())
        current = sum(account.account_type == "Current" for account in self.accounts.values())
        frozen = sum(account.status == "Frozen" for account in self.accounts.values())
        print("\nBANK SUMMARY")
        print("Total accounts       :", len(self.accounts))
        print("Savings accounts     :", savings)
        print("Current accounts     :", current)
        print("Frozen accounts      :", frozen)
        print(f"Combined balances    : Rs. {total_balance:.2f}")
        print("Recorded transactions:", len(self.transactions))

    def toggle_account_status(self, number):
        account = self.find_account(number)
        if not account:
            raise ValueError("Account not found.")
        account.status = "Frozen" if account.status == "Active" else "Active"
        if not self.save():
            account.status = "Active" if account.status == "Frozen" else "Frozen"
            raise ValueError("Could not save account status.")

    def export_statement(self, account):
        history = [item for item in self.transactions if item["account_number"] == account.account_number]
        fields = ["transaction_id", "timestamp", "account_number", "type", "amount", "details"]
        return self.storage.export_csv(f"statement_{account.account_number}.csv", history, fields)

    def export_accounts(self):
        rows = [{
            "account_number": a.account_number,
            "name": a.name,
            "phone": a.phone,
            "email": a.email,
            "account_type": a.account_type,
            "status": a.status,
            "balance": a.balance,
            "created_at": a.created_at
        } for a in self.accounts.values()]
        fields = ["account_number", "name", "phone", "email", "account_type", "status", "balance", "created_at"]
        return self.storage.export_csv("accounts_export.csv", rows, fields)

    def change_pin(self, account, old_pin, new_pin):
        account.change_pin(old_pin, new_pin)
        if not self.save():
            raise RuntimeError("PIN changed in memory, but saving failed.")
