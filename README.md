# Banking Management System

A menu-driven educational banking simulation built with Python, OOP, and data structures.

## Features
- Savings and current accounts
- Customer login with PIN
- Deposit, withdrawal, and account-to-account transfer
- Transaction IDs, timestamps, and transaction history
- Change PIN
- Freeze and unfreeze accounts through the staff menu
- Account search, balance sorting, and bank summary
- JSON data persistence
- CSV exports for statements and account reports

## Project structure
```text
Banking_Management_System/
├── main.py
├── bank.py
├── models.py
├── storage.py
├── utils.py
├── README.md
├── data/
│   └── bank_data.json
└── reports/
    ├── accounts_export.csv
    └── statement_<account_number>.csv
```

The `data` and `reports` folders are created automatically. CSV reports appear after you export them.

## Run
1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Open Terminal and run:
   ```powershell
   python main.py
   ```
   If `python` is not on PATH, use the full Python executable path or `py main.py`.

## Demo staff login
- Password: `bankadmin123`

Change this demo password before presenting if you prefer. This is an educational project, not real banking software.

## DSA and OOP concepts
- Dictionary: account lookup by account number
- List: transaction ledger
- Queue: `deque` retains the 10 most recent transactions
- Searching: account lookup
- Sorting: accounts by balance
- Classes and objects: bank, accounts, transactions/data storage
- Encapsulation: PIN is held in a private attribute
- Inheritance: savings and current account classes
- Polymorphism: account-specific interest calculation
- File handling: JSON persistence and CSV report generation
- Exception handling: invalid input and storage errors

## Safety note
This project is for learning only. PINs are stored in plain text in the local JSON file, and the staff password is a demo password. Do not use real credentials or real money.
