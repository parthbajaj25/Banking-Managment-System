import csv
import json
import os
from pathlib import Path


class Storage:
    def __init__(self, data_dir="data", reports_dir="reports"):
        self.data_dir = Path(data_dir)
        self.reports_dir = Path(reports_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
        self.data_file = self.data_dir / "bank_data.json"

    def load(self):
        if not self.data_file.exists():
            return {"accounts": [], "transactions": []}
        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                data = json.load(file)
            return {
                "accounts": data.get("accounts", []),
                "transactions": data.get("transactions", [])
            }
        except (OSError, json.JSONDecodeError):
            raise RuntimeError("Bank data could not be read. Keep a backup before editing the data file.")

    def save(self, data):
        temporary = self.data_file.with_suffix(".tmp")
        try:
            with temporary.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            os.replace(temporary, self.data_file)
            return True
        except OSError:
            if temporary.exists():
                temporary.unlink()
            return False

    def export_csv(self, filename, rows, fieldnames):
        path = self.reports_dir / filename
        try:
            with path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            return str(path)
        except OSError:
            return None
