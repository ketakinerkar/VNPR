from app.db.connection import get_connection


def user_exists(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


def create_user(
    fullname,
    address,
    username,
    email,
    phone,
    gender,
    age,
    password
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users
        (
            Fullname,
            address,
            username,
            Email,
            Phoneno,
            Gender,
            age,
            password
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        fullname,
        address,
        username,
        email,
        phone,
        gender,
        age,
        password
    ))

    conn.commit()
    conn.close()


import re


def password_check(passwd):

    if len(passwd) < 6:
        return False

    if not any(c.isdigit() for c in passwd):
        return False

    if not any(c.isupper() for c in passwd):
        return False

    if not any(c.islower() for c in passwd):
        return False

    if not any(c in "$@#%" for c in passwd):
        return False

    return True


def valid_email(email):

    return re.match(
        r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',
        email
    )