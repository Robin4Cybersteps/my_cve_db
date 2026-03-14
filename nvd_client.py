import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NVD_API_KEY")
BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def fetch_cves(start_date, end_date):
    results_per_page = 2000
    headers = {"apiKey": API_KEY} if API_KEY else {}
    params = {"pubStartDate": start_date, "pubEndDate": end_date, "resultsPerPage": results_per_page}
    start_index = 0
    cve_records = []

    while True:
        params["startIndex"] = start_index
        response = requests.get(BASE_URL, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error while fetch data from NVD: {response.status_code}")
            break

        data = response.json()
        vulnerabilities = data.get("vulnerabilities", [])
        if not vulnerabilities:
            break

        total = data.get("totalResults")

        for v in vulnerabilities:
            metrics = v["cve"].get("metrics", {}).get("cvssMetricV31", [])
            primary = next((m for m in metrics if m.get("type") == "Primary"), None)
            weakness = v["cve"].get("weaknesses", [])
            cve_records.append({
                "cve_id": v["cve"].get("id"),
                "published": v["cve"].get("published", ""),
                "lastModified": v["cve"].get("lastModified", ""),
                "status": v["cve"].get("vulnStatus", ""),
                "description": next(
                    (d["value"] for d in v["cve"].get("descriptions", []) if d["lang"] == "en"),
                    ""
                ),
                "cvss_score": primary.get("cvssData").get("baseScore") if primary else None,
                "severity": primary.get("cvssData").get("baseSeverity") if primary else None,
                "cwe_id": weakness[0].get("description")[0].get("value") if weakness else None,
            })

        if start_index + results_per_page >= total:
            break
        else:
            start_index += results_per_page
            time.sleep(6)

    return cve_records