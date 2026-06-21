from app.db.connection import get_connection


def get_logs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            car_no,
            owner_email,
            entry_time,
            exit_time
        FROM vehicle_logs
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows