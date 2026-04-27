import os
from datetime import datetime


class HTMLExporter:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export(self, data: list, filename: str = None):
        if not data:
            return None

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.html"

        filepath = os.path.join(self.output_dir, filename)

        rows_html = ""

        for item in data:
            rows_html += f"""
            <tr>
                <td>
                    <a href="{item.get('url', '#')}" target="_blank" class="product-link">
                        {item.get('title', 'N/A')}
                    </a>
                </td>
                <td class="price">{item.get('price', 'N/A')}</td>
                <td><span class="badge">-</span></td>
                <td>{'In stock' if item.get('in_stock') else 'Out of stock'}</td>
                <td class="timestamp">{item.get('last_seen_timestamp', '-')}</td>
            </tr>
            """

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Scraping Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            padding: 30px;
        }}
        .container {{
            max-width: 1100px;
            margin: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}
        th, td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
            text-align: left;
        }}
        th {{
            background: #f0f0f0;
        }}
        .price {{
            font-weight: bold;
            color: green;
        }}
        .product-link {{
            color: #2563eb;
            text-decoration: none;
        }}
        .badge {{
            background: #e5e7eb;
            padding: 3px 8px;
            border-radius: 6px;
        }}
    </style>
</head>
<body>
<div class="container">

    <h2>Scraping Report</h2>
    <p>Total items: {len(data)}</p>

    <table>
        <thead>
            <tr>
                <th>Product</th>
                <th>Price</th>
                <th>SKU</th>
                <th>Stock</th>
                <th>Timestamp</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>

</div>
</body>
</html>
        """

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        return filepath