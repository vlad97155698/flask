from flask import Flask, request, jsonify
import psycopg2
import pandas as pd
from datetime import datetime

app = Flask(__name__)

DB_PARAMS = {
    "host": "185.174.136.110",
    "dbname": "bot_db",
    "user": "postgres",
    "password": "Qwertyasd1411"
}
@app.route("/get-stats", methods=["POST"])
def get_stats():
    data = request.get_json()
    start = data.get("start_date")
    end = data.get("end_date")

    if not start:
        return jsonify({"error": "No start date"}), 400

    query = """
        SELECT
            manager_id,
            total_calls,
            manager_name,
            manager_first_name,
            manager_last_name,
            manager_username,
            current_client_id,
            current_client_name,
            total_umnik,
            total_peredan,
            total_perezvon,
            total_spisali,
            total_ne_sushestvuet,
            total_molodye,
            total_ne_dozvon,
            total_kompaniya,
            total_potracheno
        FROM manager_calls
        WHERE import_date >= %s
        """ + ("AND import_date <= %s" if end else "")

    params = [start] + ([end] if end else [])

    df = pd.read_sql(query, conn, params=params)
    conn.close()
    result = df.fillna(0).to_dict(orient="records")
    return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
