import asyncio
from urllib.parse import urljoin
from playwright.async_api import async_playwright
from config.settings import USER_AGENT, REQUEST_TIMEOUT, MAX_RETRIES
from scraper.parsers import ProductParser
from utils.logger import setup_logger

logger = setup_logger("engine")


class ScraperEngine:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self._playwright = None
        self._browser = None
        self._context = None

    async def start(self):
        if not self._playwright:
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(
                headless=self.headless,
                args=["--disable-dev-shm-usage", "--no-sandbox", "--disable-gpu"]
            )

            # Один context на все
            self._context = await self._browser.new_context(
                user_agent=USER_AGENT
            )

            # Блокуємо сміття
            await self._context.route(
                "**/*.{png,jpg,jpeg,gif,svg,woff,woff2,ttf,otf,mp4,webm}",
                lambda route: route.abort()
            )

    async def stop(self):
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def get_product_urls(self, list_url: str, link_selector: str = None):
        import json
        import asyncio
        from urllib.parse import urlparse

        path = urlparse(list_url).path
        base_url = "https://www.elcykelpunkten.se"
        api_base = f"{base_url}/api/category"

        all_products = []
        seen = set()

        skip = 0
        limit = 32  # ⚠️ реальний розмір батчу у цього API

        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Referer": list_url
        }

        def fetch(api_url):
            import urllib.request
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as response:
                return json.loads(response.read().decode())

        try:
            while True:
                api_url = f"{api_base}?slug={path}&skip={skip}"
                logger.info(f"Fetching: {api_url}")

                data = await asyncio.to_thread(fetch, api_url)

                groups = (
                    data.get("result", {})
                        .get("primaryList", {})
                        .get("productGroups", [])
                )

                if not groups:
                    logger.info("No more groups → stopping.")
                    break

                found = 0

                for group in groups:
                    for product in group.get("products", []):
                        key = product.get("key")
                        link = product.get("link")

                        if not key or not link:
                            continue

                        if key in seen:
                            continue

                        seen.add(key)

                        variants = product.get("variants", [])
                        size_label = (
                            variants[0].get("label", "One Size")
                            if variants else "One Size"
                        )

                        full_url = (
                            f"{base_url}/products/{key}"
                            f"{link}?size={size_label.replace(' ', '%20')}"
                        )

                        all_products.append({
                            "url": full_url,
                            "title": product.get("title"),
                            "price": product.get("sellingPrice", {}).get("min"),
                            "in_stock": product.get("inStock")
                        })

                        found += 1

                logger.info(f"Batch: {found}, Total: {len(all_products)}")

                # 🧠 реальний стоп-критерій
                if found == 0:
                    break

                skip += limit

            return all_products
        except Exception as e:
            logger.error(f"Error: {e}")
            return None

    async def scrape_product(self, url: str):
        await self.start()

        for attempt in range(MAX_RETRIES):
            page = await self._context.new_page()

            try:
                await page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=REQUEST_TIMEOUT
                )

                data = await ProductParser.parse_details(page, url)
                await page.close()

                if data:
                    return data

            except Exception as e:
                logger.warning(f"[{attempt+1}] Failed {url}: {e}")
                await page.close()

        return None


    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.stop()