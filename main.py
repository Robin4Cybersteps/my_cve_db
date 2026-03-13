from db_connector import start
from nvd_client import fetch_cves
from db_writer import save_cves
import db_reader

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
        show_menu()
        choice = input("Your choice: ")
        if choice == "1":
            print("Update database (fetch from NVD)")
            print("Coming soon...")
            # records = fetch_cves()
            # save_cves(conn, records)
        elif choice == "2":
            print("Search CVE by ID")
            print("Coming soon...")
        elif choice == "3":
            print("Filter CVEs by severity")
            print("Coming soon...")
        elif choice == "4":
            print("Filter CVEs by keyword")
            print("Coming soon...")
        elif choice == "5":
            print("Show CVEs by CWE")
            print("Coming soon...")
        elif choice == "6":
            print("Count CVEs by severity")
            print("Coming soon...")
        elif choice == "7":
            print("Count CVEs by CWE")
            print("Coming soon...")
        elif choice == "8":
            print("Ask AI")
            print("Coming soon...")
        elif choice == "0":
            print("Exit")
            print("¯\_(ツ)_/¯")
            conn.close()
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == '__main__':
    main()