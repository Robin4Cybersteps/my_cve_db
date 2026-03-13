from pathlib import Path
import csv

PATH_CSV = "./cwe_list.csv"

def save_cves(conn, records):

    cursor = conn.cursor()

    for record in records:

        cve_id = record.get("cve_id")
        published = record.get("published")
        last_modified = record.get("lastModified")
        status = record.get("status")
        description = record.get("description")
        cvss_score = record.get("cvss_score")
        severity = record.get("severity")
        cwe_id = record.get("cwe_id")

        # write in cve table
        cursor.execute("""
            INSERT OR REPLACE INTO cve (
                cve_id,
                cve_description,
                published_date,
                cvss_score,
                severity,
                cve_status
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (cve_id, description, published, cvss_score, severity, status))

        if record.get("cwe_id"):
            # write in cwe table
            cursor.execute("INSERT OR IGNORE INTO cwe (cwe_id) VALUES (?)", (cwe_id,))
            # write in cve_cwe table
            cursor.execute("INSERT OR IGNORE INTO cve_cwe (cve_id, cwe_id) VALUES (?, ?)", (cve_id, cwe_id))

    conn.commit()


def import_cwe_list(conn):

    cursor = conn.cursor()

    if Path.exists(PATH_CSV):
        with open("cwe_list.csv", "r") as f:
            reader = csv.DictReader(f)
            updated = 0
            for row in reader:
                cwe_id = "CWE-" + row["CWE-ID"]
                name = row["Name"]
                cursor.execute("UPDATE cwe SET cwe_name = ? WHERE cwe_id = ?", (name, cwe_id))
                updated += cursor.rowcount
            conn.commit()
            print(f"Updated {updated} CWE entries.")
    else:
        raise FileNotFoundError("CWE list not found")


if __name__ == "__main__":
    from db_connector import start
    conn = start()
    import_cwe_list(conn)