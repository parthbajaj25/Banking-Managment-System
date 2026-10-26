from datetime import datetime


class BankAccount:
    def __init__(self, account_number, name, phone, email, pin, balance=0.0, status="Active"):
        self.account_number = str(account_number)
        self.name = name
        self.phone = phone
        self.email = email
        self.__pin = str(pin)
        self.balance = float(balance)
        self.status = status
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.account_type = "General"

    def verify_pin(self, pin):
        return self.__pin == str(pin)

    def change_pin(self, old_pin, new_pin):
        if not self.verify_pin(old_pin):
            raise ValueError("Current PIN is incorrect.")
        if not new_pin.isdigit() or len(new_pin) != 4:
            raise ValueError("New PIN must contain exactly four digits.")
        self.__pin = new_pin

    def set_pin_from_storage(self, pin):
        self.__pin = str(pin)

    def deposit(self, amount):
        if self.status != "Active":
            raise ValueError("This account is frozen.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        self.balance = round(self.balance + amount, 2)

    def withdraw(self, amount):
        if self.status != "Active":
            raise ValueError("This account is frozen.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance = round(self.balance - amount, 2)

    def calculate_interest(self):
        return 0.0

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "pin": self.__pin,
            "balance": self.balance,
            "status": self.status,
            "created_at": self.created_at,
            "account_type": self.account_type
        }


class SavingsAccount(BankAccount):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.account_type = "Savings"

    def calculate_interest(self):
        return round(self.balance * 0.04, 2)


class CurrentAccount(BankAccount):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.account_type = "Current"

    def calculate_interest(self):
        return 0.0


def account_from_dict(data):
    account_type = data.get("account_type", "Savings")
    cls = CurrentAccount if account_type == "Current" else SavingsAccount
    account = cls(
        data["account_number"],
        data["name"],
        data.get("phone", ""),
        data.get("email", ""),
        data.get("pin", "0000"),
        data.get("balance", 0),
        data.get("status", "Active")
    )
    account.created_at = data.get("created_at", account.created_at)
    return account
