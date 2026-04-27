## Async E-Commerce Scraper
A high-performance, asynchronous web scraping framework built with Python, Playwright, and Asyncio. This tool efficiently extracts product data through a hybrid API/Browser approach and exports it into multiple structured formats.

## Features
Hybrid Extraction Strategy: Combines fast JSON API discovery for product lists with Playwright browser automation for deep-page scraping.

Controlled Concurrency: Uses asyncio.Semaphore to manage browser load and prevent rate-limiting.

Multi-Format Export: Simultaneously generates JSON, CSV, and a styled HTML report.

Smart Resource Management: Aborts unnecessary requests (images, fonts, media) to reduce bandwidth by up to 60%.

Professional Logging: Color-coded console output and rotating file logs for production-grade monitoring.

## Installation & Setup
1. Clone the Repository
Bash
git clone https://github.com/your-username/scraper-pro.git
cd scraper-pro
2. Setup Virtual Environment
Bash
# Create environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
3. Install Dependencies
This project requires Playwright and its browser binaries.

Bash
pip install -r requirements.txt
playwright install chromium
⚙️ Configuration
Before running, you can customize the behavior in config/settings.py:

CONCURRENCY_LIMIT: Adjust based on your CPU/RAM (default is 10).

SELECTORS: Centralized XPath/CSS selectors for easy maintenance.

LIST_URL: The target category URL to scrape.

## Execution
Run the Full Scraper
The engine will discover products via API and then scrape details using headless Chromium:

Bash
python src/main.py
Run Regex Tests
To validate extraction patterns for mileage, year, or prices:

Bash
python scratch/test_regex.py

## Project Structure
    Plaintext
    ├── config/             # Global settings and selectors
    ├── logs/               # Log files (scraper.log)
    ├── output/             # Scraped data (JSON, CSV, HTML reports)
    ├── scratch/            # Experimental scripts and regex tests
    ├── src/
    │   ├── scraper/        # Core logic: Engine and Parsers
    │   ├── storage/        # Persistence layer: CSV, JSON, HTML exporters
    │   ├── utils/          # Logger and shared utilities
    │   └── main.py         # Application entry point
    └── requirements.txt    # Project dependencies

## License

This project is licensed under the MIT License.

## Credits

This project uses Playwright by Microsoft, licensed under the Apache License 2.0.

See the LICENSE file for details.