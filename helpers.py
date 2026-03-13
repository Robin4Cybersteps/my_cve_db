from tabulate import tabulate
import textwrap

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


def print_detail(result):
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
