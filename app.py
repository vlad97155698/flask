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
    try:
        data = request.get_json()
        date_str = data.get("date")  # формат "01.04.2025"
        if not date_str:
            return jsonify({"error": "No date provided"}), 400

        import_date = datetime.strptime(date_str, "%d.%m.%Y").date()

        conn = psycopg2.connect(**DB_PARAMS)
        query = """
            SELECT
                manager_first_name,
                total_calls,
                total_peredan,
                total_umnik,
                total_ne_sushestvuet,
                total_kompaniya,
                total_potracheno,
                total_ne_dozvon
            FROM manager_calls
            WHERE import_date = %s
        """
        df = pd.read_sql(query, conn, params=[import_date])
        conn.close()

        result = df.fillna(0).to_dict(orient="records")
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
