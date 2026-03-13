from pydantic import BaseModel
from typing import Literal, Optional

class CVEQuery(BaseModel):
    column: Literal["severity", "cvss_score", "cve_status", "cve_id"]
    operator: Literal["=", ">", "<", "!=", "IS NULL", "IS NOT NULL"]
    value: str | None

def get_cve_by_id(conn, cve_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cve WHERE cve_id = ?", (cve_id,))
    return cursor.fetchone()

def get_cves_by_severity(conn, severity):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cve WHERE severity = ?", (severity,))
    return cursor.fetchall()

def execute_query(conn, query: CVEQuery):
    cursor = conn.cursor()
    if query.operator in ("IS NULL", "IS NOT NULL"):
        sql = f"SELECT * FROM cve WHERE {query.column} {query.operator}"
        cursor.execute(sql)
    else:
        sql = f"SELECT * FROM cve WHERE {query.column} {query.operator} ?"
        cursor.execute(sql, (query.value,))
    return cursor.fetchall()

def get_cwe_by_id(conn, cwe_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cwe WHERE cwe_id = ?", (cwe_id,))
    return cursor.fetchone()

def get_cves_by_cwe(conn, cwe_id):
    cursor = conn.cursor()
    cursor.execute("SELECT cve.* FROM cve JOIN cve_cwe ON cve.cve_id = cve_cwe.cve_id WHERE cve_cwe.cwe_id = ?", (cwe_id,))
    return cursor.fetchall()
