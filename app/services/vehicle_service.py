from app.db.connection import get_connection

def register_vehicle(
    fullname,
    address,
    email,
    phone,
    gender,
    age,
    photo_path,
    car_no,
    chassis_no
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO number_plates
        (
            Fullname,
            address,
            Email,
            Phoneno,
            Gender,
            age,
            photo,
            car_no,
            chassis_no
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        fullname,
        address,
        email,
        phone,
        gender,
        age,
        photo_path,
        car_no,
        chassis_no
    ))

    conn.commit()
    conn.close()