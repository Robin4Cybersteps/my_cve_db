from db_connector import start
from nvd_client import fetch_cves
from db_writer import save_cves
from helpers import print_results, print_detail, print_total_per_cwe, print_total_per_severity
import db_reader
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    print("""
        ====== Project 3 - OWN CVE DB ======
        1. Update database (fetch from NVD)
        2. Search CVE by ID
        3. Filter CVEs by severity
        4. Filter CVEs by keyword
        5. Show CVEs by CWE
        ============ Statistics ============
        6. Count CVEs by severity
        7. Count CVEs by CWE
        ================ AI ================
        8. Ask AI
        ====================================
        0. Exit
        """)


def main():
    conn = start()
    while True:
        clear_screen()
        show_menu()
        choice = input("Your choice: ")
        if choice == "1":
            print("Update database (fetch from NVD)")
            print("Coming soon...")
            # records = fetch_cves()
            # save_cves(conn, records)
            input("Press Enter to continue...")
        elif choice == "2":
            print("Search CVE by ID")
            cve_id = input("Please enter the CVE-ID: ")
            results = db_reader.get_cve_by_id(conn, cve_id)
            if results:
                print(print_detail(results))
            else:
                print("CVE not found.")
            input("Press Enter to continue...")
        elif choice == "3":
            print("Filter CVEs by severity")
            severity = input("Enter severity (LOW/MEDIUM/HIGH/CRITICAL): ").upper()
            results = db_reader.get_cves_by_severity(conn, severity)
            print(print_results(results))
            input("Press Enter to continue...")
        elif choice == "4":
            print("Filter CVEs by keyword")
            keyword = input("Please enter a keyword: ")
            results = db_reader.get_cves_by_keyword(conn, keyword)
            print(print_results(results))
            input("Press Enter to continue...")
        elif choice == "5":
            print("Show CVEs by CWE")
            cwe_id = "CWE-89"
            results = db_reader.get_cves_by_cwe(conn, cwe_id)
            print(print_results(results))
            input("Press Enter to continue...")
        elif choice == "6":
            print("Count CVEs by severity")
            results = db_reader.count_cves_by_severity(conn)
            print(print_total_per_severity(results))
            input("Press Enter to continue...")
        elif choice == "7":
            print("Count CVEs by CWE")
            results = db_reader.count_cves_by_cwe(conn)
            print(print_total_per_cwe(results))
            input("Press Enter to continue...")
        elif choice == "8":
            print("Ask AI")
            print("Coming soon...")
            input("Press Enter to continue...")
        elif choice == "0":
            print("Exit")
            print("¯\_(ツ)_/¯")
            conn.close()
            break
        else:
            print("Invalid choice, please try again.")
            input("Press Enter to continue...")


if __name__ == '__main__':
    main()