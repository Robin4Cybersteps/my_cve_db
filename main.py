from db_connector import start
from nvd_client import fetch_cves
from db_writer import save_cves

if __name__ == '__main__':
    print("Starte Programm - Öffne oder erstelle Datenbank")
    conn = start()
    print("Beginne Datenabruf")
    records = fetch_cves()
    print(f"Gefunden: {len(records)} CVEs")
    save_cves(conn, records)
    print(f"Gespeichert: {len(records)} CVEs in DB")
    conn.close()