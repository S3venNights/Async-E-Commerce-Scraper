import re
try:
    re.search(r"Årsmodell[:\s]+(20\d{2})", "Årsmodell 2024")
    print("Success 1")
except Exception as e:
    print(f"Error 1: {e}")

try:
    # Testing mileage regex
    re.search(r"(\d+[\s\d]*)\s*(km|mil|ODO)", "1200 km", re.IGNORECASE)
    print("Success 2")
except Exception as e:
    print(f"Error 2: {e}")
