import asyncio
import logging
import sys
import os
from datetime import datetime

# Add root and src to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, "src"))

from config.settings import LIST_URL, CONCURRENCY_LIMIT, SELECTORS
from scraper.engine import ScraperEngine
from storage.manager import StorageManager
from utils.logger import setup_logger

# Initialize professional logger
logger = setup_logger("main", logging.INFO)

async def main():
    start_time = datetime.now()
    logger.info(f"Starting Scraper PRO v1 at {start_time}")
    
    storage = StorageManager()
    
    async with ScraperEngine(headless=True) as scraper:
        # Step 1: Get products with basic info from API
        products = await scraper.get_product_urls(LIST_URL, SELECTORS["product_link"])
        logger.info(f"Discovered {len(products)} products via API.")
        
        if not products:
            logger.error("No products found. Check API or network.")
            return

        # Step 2: Concurrent scraping for details (Mileage, Year, etc.)
        semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
        
        async def scrape_with_semaphore(product_info, index, total):
            url = product_info["url"]
            async with semaphore:
                logger.info(f"[{index}/{total}] Scraping details: {url}")
                details = await scraper.scrape_product(url)
                
                # Merge API info with detailed info
                final_data = product_info.copy()
                if details:
                    # Update with details from page, but keep API info as fallback
                    for key, val in details.items():
                        if val and val != "N/A":
                            final_data[key] = val
                
                await asyncio.sleep(0.3)
                return final_data

        tasks = [
            scrape_with_semaphore(p, i + 1, len(products)) 
            for i, p in enumerate(products)
        ]
        
        results = await asyncio.gather(*tasks)
        all_data = [r for r in results if r]
        
        # Step 3: Export results
        storage.save_all(all_data)
        
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"Scraping completed in {duration}. Total records: {len(all_data)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Scraper stopped by user.")
    except Exception as e:
        logger.error(f"Critical error: {e}", exc_info=True)
