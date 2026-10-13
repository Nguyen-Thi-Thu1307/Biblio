from sqlalchemy import inspect

from .extensions import db


def migrate_social_auth_schema():
    if db.engine.dialect.name != "sqlite":
        inspector = inspect(db.engine)
        if "user" not in inspector.get_table_names():
            return
        columns = {column["name"]: column for column in inspector.get_columns("user")}
        if not columns["password_hash"]["nullable"]:
            raise RuntimeError(
                "Không thể tự chuyển đổi cột mật khẩu trên hệ quản trị này."
            )
        return

    connection = db.engine.raw_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys=OFF")
        cursor.execute("BEGIN IMMEDIATE")
        columns = cursor.execute("PRAGMA table_info(user)").fetchall()
        if not columns:
            connection.commit()
            return
        password_column = next(
            (column for column in columns if column[1] == "password_hash"), None
        )
        if password_column is None:
            raise RuntimeError("Bảng user không có cột password_hash.")
        if not password_column[3]:
            connection.commit()
            return
        cursor.execute(
            """
            CREATE TABLE user_social_auth_new (
                id INTEGER NOT NULL PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(120) NOT NULL UNIQUE,
                password_hash VARCHAR(255),
                full_name VARCHAR(100),
                role VARCHAR(20),
                is_active BOOLEAN
            )
            """
        )
        cursor.execute(
            """
            INSERT INTO user_social_auth_new
                (id, username, email, password_hash, full_name, role, is_active)
            SELECT id, username, email, password_hash, full_name, role, is_active
            FROM user
            """
        )
        cursor.execute("DROP TABLE user")
        cursor.execute("ALTER TABLE user_social_auth_new RENAME TO user")
        connection.commit()
    finally:
        try:
            connection.rollback()
            cursor.execute("PRAGMA foreign_keys=ON")
        finally:
            cursor.close()
            connection.close()
