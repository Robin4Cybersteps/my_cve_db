from db_connector import start
from ai_translator import get_query
from nvd_client import fetch_cves
from db_writer import save_cves, import_cwe_list
import helpers
import db_reader
import os
from datetime import datetime, timedelta

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    print("""
        ====== Project 3 - OWN CVE DB ======
        1. Update database (fetch from NVD)
        2. Search CVE by ID
        3. Search CWE by ID
        4. Filter CVEs by severity
        5. Filter CVEs by keyword
        6. Show CVEs by CWE
        ============ Statistics ============
        7. Count CVEs by severity
        8. Count CVEs by CWE
        ================ AI ================
        9. Ask AI
        ====================================
        0. Exit
        """)


def main():
    conn = start()
    if db_reader.is_db_empty(conn):
        print("Database is empty. Starting initial fetch...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=120)
        end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S.000")
        start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S.000")
        records = fetch_cves(start_date, end_date)
        save_cves(conn, records)
        import_cwe_list(conn)

    while True:
        clear_screen()
        show_menu()
        choice = input("Your choice: ")

        if choice == "1":
            print("Update database (fetch from NVD)")
            last_date = db_reader.get_last_entry(conn)
            end_date = datetime.now()
            start_date = helpers.start_date_calculator(last_date, end_date)
            end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S.000")
            start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S.000")
            records = fetch_cves(start_date, end_date)
            print(f"New entries found: {len(records)}")
            save_cves(conn, records)
            import_cwe_list(conn)
            input("Press Enter to continue...")

        elif choice == "2":
            print("Search CVE by ID")
            cve_id = input("Please enter the CVE-ID: ")
            result = db_reader.get_cve_by_id(conn, cve_id)
            if result:
                print(helpers.print_cve_details(result))
            else:
                print("CVE not found.")
            input("Press Enter to continue...")

        elif choice == "3":
            print("Search CWE by ID")
            cwe_id = input("Please enter only the numbers of the CWE-ID: ")
            result = db_reader.get_cwe_by_id(conn, cwe_id)
            if result:
                print(helpers.print_cwe_details(result))
            else:
                print("CWE not found.")
            input("Press Enter to continue...")

        elif choice == "4":
            print("Filter CVEs by severity")
            severity = input("Enter severity (LOW / MEDIUM / HIGH / CRITICAL): ").upper()
            results = db_reader.get_cves_by_severity(conn, severity)
            print(helpers.print_results(results))
            print(f"--- Total: {len(results)} ---")
            input("Press Enter to continue...")

        elif choice == "5":
            print("Filter CVEs by keyword")
            keyword = input("Please enter a keyword: ")
            results = db_reader.get_cves_by_keyword(conn, keyword)
            print(helpers.print_results(results))
            print(f"--- Total: {len(results)} ---")
            input("Press Enter to continue...")

        elif choice == "6":
            print("Show CVEs by CWE")
            cwe_id = input("Please enter the only numbers of the CWE-ID: ")
            results = db_reader.get_cves_by_cwe(conn, cwe_id)
            print(helpers.print_results(results))
            print(f"--- Total: {len(results)} ---")
            input("Press Enter to continue...")

        elif choice == "7":
            print("Count CVEs by severity")
            results = db_reader.count_cves_by_severity(conn)
            print(helpers.print_total_per_severity(results))
            input("Press Enter to continue...")

        elif choice == "8":
            print("Count CVEs by CWE")
            results = db_reader.count_cves_by_cwe(conn)
            print(helpers.print_total_per_cwe(results))
            input("Press Enter to continue...")

        elif choice == "9":
            print("Ask AI")
            user_input = input("What do you want to know?\n")
            query = get_query(user_input)
            results = db_reader.execute_ai_query(conn, query)
            print(helpers.print_any(results))
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