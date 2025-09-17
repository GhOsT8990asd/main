import os
import json
import requests
from datetime import datetime

os.makedirs("public", exist_ok=True)
with open("public/.keep", "w") as f:
    f.write("")  # пустой файл

def run():
    # 🔐 Авторизация в Syrve
    login = "roman"
    password = "5002207f2329a5481a580f69a11a0f54b4b83875"
    auth_url = f"https://alimer-comert-co.syrve.online/resto/api/auth?login={login}&pass={password}"
    token = requests.get(auth_url).text.strip()

    # 📊 Получение OLAP-отчёта
    olap_url = (
        "https://alimer-comert-co.syrve.online/resto/api/v2/reports/olap/byPresetId/"
        "0f032c52-7afb-4b48-87ae-79c5f3ebdfa4"
        f"?key={token}&dateFrom=2025-04-01&dateTo=2025-10-01"
    )
    data = requests.get(olap_url).json()

    # 📁 Сохранение в файл для GitHub Pages
    os.makedirs("public", exist_ok=True)
    filename = f"public/syrve_olap_{datetime.today().strftime('%Y%m%d')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved locally: {filename}")

if __name__ == "__main__":
    run()
