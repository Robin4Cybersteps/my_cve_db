from pydantic import BaseModel
from typing import Literal, Optional

class CVEQuery(BaseModel):
    column: Literal["severity", "cvss_score", "cve_status", "cve_id"]
    operator: Literal["=", ">", "<", "!=", "IS NULL", "IS NOT NULL", "LIKE"]
    value: str | None

def is_db_empty(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cve")
    count = cursor.fetchone()[0]
    return count == 0

def get_last_entry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(published_date) AS last_date FROM cve")
    result = cursor.fetchone()
    return result["last_date"]

def get_cve_by_id(conn, cve_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cve WHERE cve_id = ?", (cve_id,))
    return cursor.fetchone()

def get_cves_by_severity(conn, severity):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cve WHERE severity = ?", (severity,))
    return cursor.fetchall()

def get_cves_by_keyword(conn, keyword):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cve WHERE cve_description LIKE ?", (f"%{keyword}%",))
    return cursor.fetchall()

def execute_query(conn, query: CVEQuery):
    cursor = conn.cursor()
    if query.operator in ("IS NULL", "IS NOT NULL"):
        sql = f"SELECT * FROM cve WHERE {query.column} {query.operator}"
        cursor.execute(sql)
    else:
        if query.operator == "LIKE":
            value = f"%{query.value}%"
        else:
            value = query.value
        sql = f"SELECT * FROM cve WHERE {query.column} {query.operator} ?"
        cursor.execute(sql, (value,))
    return cursor.fetchall()

def get_cwe_by_id(conn, cwe_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cwe WHERE cwe_id = ?", (cwe_id,))
    return cursor.fetchone()

def get_cves_by_cwe(conn, cwe_id):
    cursor = conn.cursor()
    cursor.execute("SELECT cve.* FROM cve JOIN cve_cwe ON cve.cve_id = cve_cwe.cve_id WHERE cve_cwe.cwe_id = ?", (f"CWE-{cwe_id}",))
    return cursor.fetchall()

def count_cves_by_severity(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT severity, COUNT(*) AS total FROM cve GROUP BY severity ORDER BY total DESC")
    return cursor.fetchall()

def count_cves_by_cwe(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT cwe.cwe_id, cwe.cwe_name, COUNT(cve_id) AS total FROM cve_cwe JOIN cwe ON cwe.cwe_id = cve_cwe.cwe_id GROUP BY cwe.cwe_id ORDER BY total DESC")
    return cursor.fetchall()