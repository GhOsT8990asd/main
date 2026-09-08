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

# 🚪 Новая функция логаута
def logout_syrve(host, token):
    if not token:
        return
    url = f"https://{host}/resto/api/logout?key={token}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ Сессия закрыта на сервере: {host}")
        else:
            print(f"⚠️ Ошибка логаута на {host}. Код: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Ошибка сети при логауте {host}: {e}")

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
host1 = "alimer-comert-co.syrve.online"
token1 = None
data1 = []
try:
    token1 = get_token(host1)
    data1 = get_olap_data(host1, "0f032c52-7afb-4b48-87ae-79c5f3ebdfa4", token1, date_from, date_to)
finally:
    logout_syrve(host1, token1) # Сработает в любом случае, даже при ошибке

# 🍺 Сервер 2: beer-house
host2 = "beer-house.syrve.online"
token2 = None
data2 = []
try:
    token2 = get_token(host2)
    data2 = get_olap_data(host2, "e4894e06-a6d8-4ce6-8333-f73f9dbaeb1c", token2, date_from, date_to)
finally:
    logout_syrve(host2, token2) # Сработает в любом случае, даже при ошибке

# 🔗 Объединение строк
combined = data1 + data2

# 💾 Сохранение
filename = "public/syrve_combined.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(combined, f, ensure_ascii=False)

print(f"✅ Saved: {filename}")
