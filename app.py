from flask import Flask, request, jsonify
import psycopg2
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Параметры подключения к БД
DB_PARAMS = {
    "host": "185.174.136.110",  # замени на свой IP
    "dbname": "your_db_name",
    "user": "your_user",
    "password": "your_password"
}

@app.route("/get-stats", methods=["POST"])
def get_stats():
    try:
        data = request.get_json()
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if not start_date:
            return jsonify({"error": "start_date is required"}), 400

        # Преобразуем в формат даты
        start = datetime.strptime(start_date, "%d.%m.%Y").date()
        params = [start]
        query = """
            SELECT
                manager_id,
                manager_first_name,
                SUM(total_calls) AS total_calls,
                SUM(total_umnik) AS total_umnik,
                SUM(total_potracheno) AS total_potracheno,
                SUM(total_kompaniya) AS total_kompaniya,
                SUM(total_ne_sushestvuet) AS total_ne_sushestvuet,
                SUM(total_ne_dozvon) AS total_ne_dozvon,
                SUM(total_peredan) AS total_peredan,
                SUM(total_perezvon) AS total_perezvon,
                SUM(total_spisali) AS total_spisali,
                SUM(total_molodye) AS total_molodye
            FROM manager_calls
            WHERE import_date >= %s
        """

        if end_date:
            end = datetime.strptime(end_date, "%d.%m.%Y").date()
            query += " AND import_date <= %s"
            params.append(end)

        query += " GROUP BY manager_id, manager_first_name ORDER BY manager_id"

        conn = psycopg2.connect(**DB_PARAMS)
        df = pd.read_sql(query, conn, params=params)
        conn.close()

        return jsonify(df.fillna(0).to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return "API is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
