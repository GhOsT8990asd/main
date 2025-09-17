import os
import json
import requests
from datetime import datetime

os.makedirs("public", exist_ok=True)

def run():
    # 🔐 Авторизация в Syrve
    login = "roman"
    password = "5002207f2329a5481a580f69a11a0f54b4b83875"
    auth_url = f"https://alimer-comert-co.syrve.online/resto/api/auth?login={login}&pass={password}"
    token = requests.get(auth_url).text.strip()

    # 📅 Динамический диапазон дат
    date_from = "2025-04-01"
    date_to = datetime.today().strftime("%Y-%m-%d")

    # 📊 Получение OLAP-отчёта
    olap_url = (
        "https://alimer-comert-co.syrve.online/resto/api/v2/reports/olap/byPresetId/"
        "0f032c52-7afb-4b48-87ae-79c5f3ebdfa4"
        f"?key={token}&dateFrom={date_from}&dateTo={date_to}"
    )
    data = requests.get(olap_url).json()

    # 📁 Сохранение JSON
    filename = f"public/syrve_olap_{datetime.today().strftime('%Y%m%d')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved: {filename}")

if __name__ == "__main__":
    run()
