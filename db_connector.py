from pathlib import Path
import sqlite3

PATH_DB = "./my_own_cve.db"
PATH_SQL = "./schema.sql"

def init_db(path_db, path_sql):
    if Path(path_sql).exists():
        try:
            with open(path_sql, 'r') as f:
                sql_script = f.read()
                print(sql_script)
                conn = sqlite3.connect(path_db)
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.executescript(sql_script)
                conn.commit()
                return conn
        except:
            raise Exception ("Error while creating DB")
    else:
        raise FileNotFoundError ("No schema.sql found, cant't create DB")

def open_db(path):
    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except:
        raise Exception ("Failed to open DB")

def start():
    if Path(PATH_DB).exists():
        conn = open_db(PATH_DB)
    else:
        conn = init_db(PATH_DB, PATH_SQL)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn