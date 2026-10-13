import sqlite3
from datetime import datetime
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().with_name("biblio.db")


def migrate():
    if not DATABASE_PATH.is_file():
        raise FileNotFoundError(f"Không tìm thấy cơ sở dữ liệu: {DATABASE_PATH}")

    backup_path = DATABASE_PATH.with_name(
        f"{DATABASE_PATH.stem}.bak-{datetime.now():%Y%m%d-%H%M%S}{DATABASE_PATH.suffix}"
    )
    suffix = 1
    while backup_path.exists():
        backup_path = DATABASE_PATH.with_name(
            f"{DATABASE_PATH.stem}.bak-{datetime.now():%Y%m%d-%H%M%S}-{suffix}{DATABASE_PATH.suffix}"
        )
        suffix += 1

    source = sqlite3.connect(DATABASE_PATH)
    try:
        backup = sqlite3.connect(backup_path)
        try:
            source.backup(backup)
        finally:
            backup.close()
    finally:
        source.close()

    connection = sqlite3.connect(DATABASE_PATH)
    try:
        existing_tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        required_tables = {"category", "book"}
        missing_tables = required_tables - existing_tables
        if missing_tables:
            raise RuntimeError(
                "Thiếu bảng cần migrate: " + ", ".join(sorted(missing_tables))
            )

        with connection:
            for table, column in (
                ("category", "name_en"),
                ("book", "description_en"),
            ):
                columns = {
                    row[1] for row in connection.execute(f'PRAGMA table_info("{table}")')
                }
                if column not in columns:
                    connection.execute(
                        f'ALTER TABLE "{table}" ADD COLUMN "{column}" TEXT'
                    )
    finally:
        connection.close()

    print(f"Đã sao lưu cơ sở dữ liệu: {backup_path}")
    print("Đã kiểm tra/thêm các cột category.name_en và book.description_en.")


if __name__ == "__main__":
    migrate()
