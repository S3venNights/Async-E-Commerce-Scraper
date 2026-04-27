import re
import json
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger("parser")


class ProductParser:
    @staticmethod
    async def parse_details(page, url):
        try:
            data = {
                "url": url,
                "title": await ProductParser._get_title(page),
                "price": await ProductParser._get_price(page),
                "regular_price": await ProductParser._get_regular_price(page),
                "mileage": await ProductParser._get_mileage(page),
                "age": await ProductParser._get_age(page),
                "last_seen_timestamp": datetime.utcnow().isoformat()
            }
            return data

        except Exception as e:
            logger.error(f"Parsing error on {url}: {e}")
            return None

    @staticmethod
    async def _get_title(page):
        # JSON-LD first
        ld = await ProductParser._get_jsonld(page)
        if ld and ld.get("name"):
            return ld["name"].strip()

        el = await page.query_selector("h1")
        return (await el.inner_text()).strip() if el else "N/A"

    @staticmethod
    async def _get_price(page):
        ld = await ProductParser._get_jsonld(page)
        if ld:
            offers = ld.get("offers")
            if isinstance(offers, dict):
                return offers.get("price")
            if isinstance(offers, list) and offers:
                return offers[0].get("price")

        el = await page.query_selector(".text-tertiary.text-3xl")
        if not el:
            el = await page.query_selector("[data-cy='product-price']")

        return (await el.inner_text()).strip() if el else "N/A"

    @staticmethod
    async def _get_regular_price(page):
        el = await page.query_selector("xpath=//*[contains(., 'Rek.') or contains(., 'Nypris')]")
        if el:
            text = (await el.inner_text()).replace("kr", "").strip()
            return text
        return "N/A"

    @staticmethod
    async def _get_mileage(page):
        el = await page.query_selector("xpath=//*[contains(., 'ODO') or contains(., 'Distans')]")
        if not el:
            return "N/A"

        text = await el.inner_text()

        match = re.search(r"(\d[\d\s]*)\s*(km|mil)", text, re.IGNORECASE)
        return match.group(0) if match else text.strip()

    @staticmethod
    async def _get_age(page):
        ld = await ProductParser._get_jsonld(page)
        if ld and "releaseDate" in ld:
            return ld["releaseDate"]

        el = await page.query_selector(
            "xpath=//*[contains(., 'Årsmodell') or contains(., 'Model year')]"
        )
        if el:
            return (await el.inner_text()).strip()

        return "N/A"

    @staticmethod
    async def _get_jsonld(page):
        scripts = await page.query_selector_all("script[type='application/ld+json']")

        for s in scripts:
            try:
                raw = await s.inner_text()
                data = json.loads(raw)

                if isinstance(data, list):
                    for item in data:
                        if item.get("@type") == "Product":
                            return item

                if isinstance(data, dict) and data.get("@type") == "Product":
                    return data

            except:
                continue

        return None