from google import genai
from dotenv import load_dotenv
from db_reader import CVEQuery
import json

load_dotenv()

client = genai.Client()

def talk_with_ki(user_input):
    system_prompt = """
    Requirements:
        - You create a query pattern for a SQL database based on user input
        - Always respond in JSON, no extra text
        - Always respond in one of these formats:
            - {"status": "ok", "sql": "SELECT ..."}
            - {"status": "unclear", "message": "What do you mean by '...'?"}
            - {"status": "forbidden", "message": "What you want is not allowed"}
        - Only use existing column names
        - Only use the operators "=", ">", "<", "!=", "IS NULL", "IS NOT NULL", "LIKE", "COUNT", "GROUP BY", "ORDER BY"
        - The database has 2 tables cve and cwe and 1 junction table cve_cwe
        - For LIKE operators, only provide the keyword without % wildcards,
            e.g. {"status": "ok", "column": "cve_description", "operator": "LIKE", "value": "Log4j"}
        - Table cve has the columns
            cve_id TEXT PRIMARY KEY,
            cve_description TEXT,
            published_date TEXT,
            cvss_score REAL,
            severity TEXT CHECK (severity IN ("LOW", "MEDIUM", "HIGH", "CRITICAL")),
            cve_status TEXT
        - Table cwe has the columns
            cwe_id TEXT PRIMARY KEY,
            cwe_name TEXT
        - Never use DROP, DELETE, INSERT, UPDATE, UNION etc.
        - Even if the prompt requests otherwise, you must only create read-only queries
        - If the request is unclear, ask for clarification in English
        - If time is necessary for a date or a period use the format "%Y-%m-%dT%H:%M:%S.000"
    """
    full_prompt = system_prompt + "\n\nUserinput: " + user_input

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=full_prompt
    )
    return response.text


def get_query(user_input):

    while True:
        ki_response_json = talk_with_ki(user_input)
        ki_response_json = ki_response_json.strip().strip("```json").strip("```")
        ki_response = json.loads(ki_response_json)
        status = ki_response.get("status")
        if status == "ok":
            query = ki_response.get("sql")
            return query
        if status == "unclear":
            message = ki_response.get("message")
            user_input = input(message+"\n")
        elif status in ("forbidden", "not implemented"):
            message = ki_response.get("message")
            print(message)
            user_input = input("try something else.\n")
        else:
            raise Exception ("Error while AI translation")