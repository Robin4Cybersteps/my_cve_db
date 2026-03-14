from tabulate import tabulate
import textwrap
from datetime import datetime, timedelta

def start_date_calculator(last_date, end_date):
    last_datetime = datetime.strptime(last_date, "%Y-%m-%dT%H:%M:%S.%f")
    diff = end_date - last_datetime
    if diff.days > 120:
        start_date = end_date - timedelta(days=120)
    else:
        start_date = last_datetime
    return start_date


def truncate(text, length=50):
    if text and len(text) > length:
        return text[:length] + "..."
    return text

def print_any(results):
    if not results:
        return "No results found."

    return tabulate(results, headers="keys", tablefmt="github")

def print_results(results):
    if not results:
        return "No results found."

    filtered = []
    for row in results:
        filtered.append({
            "cve_id": row["cve_id"],
            "severity": row["severity"],
            "cvss_score": row["cvss_score"],
            "cve_status": row["cve_status"],
            "published_date": row["published_date"]
        })

    clean_entries = tabulate(filtered, headers="keys", tablefmt="github")

    return clean_entries


def print_cve_details(result):
    if not result:
        return "No results found."

    cve_id = result["cve_id"]
    severity = result["severity"]
    cvss_score = result["cvss_score"]
    cve_status = result["cve_status"]
    published_date = result["published_date"]
    description = textwrap.fill(result["cve_description"], width=80, subsequent_indent="        ")

    formatted_string = f"""
        CVE-ID:      {cve_id}
        Severity:    {severity}
        Score:       {cvss_score}
        Status:      {cve_status}
        Published:   {published_date}

        Description:
        {description}
        """
    return formatted_string


def print_cwe_details(result):
    if not result:
        return "No results found."

    cwe_id = result["cwe_id"]
    cwe_name = result["cwe_name"]

    formatted_string = f"""
        CWE-ID:      {cwe_id}
        Description:
        {cwe_name}
        """
    return formatted_string


def print_total_per_cwe(results):
    if not results:
        return "No results found."

    filtered = []
    for row in results:
        filtered.append({
            "cwe_id": row["cwe_id"],
            "cwe_name": truncate(row["cwe_name"]),
            "total": row["total"]
        })

    clean_entries = tabulate(filtered, headers="keys", tablefmt="github")

    return clean_entries



def print_total_per_severity(results):
    if not results:
        return "No results found."

    filtered = []
    for row in results:
        filtered.append({
            "severity": row["severity"],
            "total": row["total"]
        })

    clean_entries = tabulate(filtered, headers="keys", tablefmt="github")

    return clean_entries