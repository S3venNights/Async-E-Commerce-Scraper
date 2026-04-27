import csv
import os
from datetime import datetime


class CSVStorage:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save(self, data: list, filename: str = None):
        if not data:
            return None

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraped_data_{timestamp}.csv"

        filepath = os.path.join(self.output_dir, filename)

        # 🧠 FIX: збираємо ВСІ можливі поля, а не тільки перший елемент
        fieldnames = sorted({key for item in data for key in item.keys()})

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()

            for row in data:
                # 🧠 FIX: гарантуємо відсутні поля
                safe_row = {key: row.get(key, "") for key in fieldnames}
                writer.writerow(safe_row)

        return filepath