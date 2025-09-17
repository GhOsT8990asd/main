import os
import json
import requests
from google.cloud import storage
from google.oauth2 import service_account
from datetime import datetime

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

    # 🔐 Авторизация в GCP вручную
    key_path = "gcp_key.json"
    with open(key_path, "w") as f:
        f.write(os.environ["GCP_KEY"])

    credentials = service_account.Credentials.from_service_account_file(key_path)
    project_id = credentials.project_id

    # ☁️ Загрузка в GCS
    client = storage.Client(project=project_id, credentials=credentials)
    bucket = client.bucket("syrve-etl-storage")
    filename = f"syrve_olap_{datetime.today().strftime('%Y%m%d')}.json"
    blob = bucket.blob(filename)
    blob.upload_from_string(json.dumps(data), content_type="application/json")
    blob.make_public()

    print(f"✅ Uploaded: {blob.public_url}")

if __name__ == "__main__":
    run()
