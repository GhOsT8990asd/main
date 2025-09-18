import os
import json
import requests
from datetime import datetime, timedelta

os.makedirs("public", exist_ok=True)

# 🔐 Авторизация
login = "roman"
password = "5002207f2329a5481a580f69a11a0f54b4b83875"

def get_token(host):
    url = f"https://{host}/resto/api/auth?login={login}&pass={password}"
    return requests.get(url).text.strip()

def get_olap_data(host, preset_id, token, date_from, date_to):
    url = (
        f"https://{host}/resto/api/v2/reports/olap/byPresetId/{preset_id}"
        f"?key={token}&dateFrom={date_from}&dateTo={date_to}"
    )
    response = requests.get(url).json()
    return response.get("data", [])

# 📅 Диапазон дат
date_from = "2025-04-01"
date_to = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

# 🏪 Сервер 1: alimer-comert-co
token1 = get_token("alimer-comert-co.syrve.online")
data1 = get_olap_data("alimer-comert-co.syrve.online", "0f032c52-7afb-4b48-87ae-79c5f3ebdfa4", token1, date_from, date_to)

# 🍺 Сервер 2: beer-house
token2 = get_token("beer-house.syrve.online")
data2 = get_olap_data("beer-house.syrve.online", "e4894e06-a6d8-4ce6-8333-f73f9dbaeb1c", token2, date_from, date_to)

# 🔗 Объединение строк
combined = data1 + data2

# 💾 Сохранение
filename = "public/syrve_combined.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(combined, f, ensure_ascii=False)

print(f"✅ Saved: {filename}")
