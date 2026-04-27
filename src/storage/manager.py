import logging
import sys
import os

# Ensure we can find config
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from config.settings import OUTPUT_JSON_DIR, OUTPUT_CSV_DIR, OUTPUT_HTML_DIR
from storage.json_storage import JSONStorage
from storage.csv_storage import CSVStorage
from storage.html_exporter import HTMLExporter
from utils.logger import setup_logger

logger = setup_logger("storage")

class StorageManager:
    def __init__(self):
        # Ensure subdirectories exist
        for d in [OUTPUT_JSON_DIR, OUTPUT_CSV_DIR, OUTPUT_HTML_DIR]:
            if not os.path.exists(d):
                os.makedirs(d)

        self.json = JSONStorage(output_dir=OUTPUT_JSON_DIR)
        self.csv = CSVStorage(output_dir=OUTPUT_CSV_DIR)
        self.html = HTMLExporter(output_dir=OUTPUT_HTML_DIR)

    def save_all(self, data):
        if not data:
            logger.warning("No data to save.")
            return

        json_path = self.json.save(data)
        csv_path = self.csv.save(data)
        html_path = self.html.export(data)

        logger.info(f"Results exported: JSON={json_path}, CSV={csv_path}, HTML={html_path}")
        return json_path, csv_path, html_path
