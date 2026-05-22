from pathlib import Path
from contextlib import contextmanager
import hashlib
import hmac
import secrets
import sqlite3

import pandas as pd


DB_PATH = Path(__file__).resolve().with_name("receipts.db")

RECEIPT_COLUMNS = [
    "id",
    "user_id",
    "date",
    "store_name",
    "items",
    "category",
    "total_amount",
    "vat",
    "tax_deductible",
    "status",
]


@contextmanager
def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120000,
    ).hex()

    return f"{salt}${password_hash}"


def _verify_password(password, stored_password):
    try:
        salt, expected_hash = stored_password.split("$", 1)
    except ValueError:
        return False

    candidate = _hash_password(password, salt).split("$", 1)[1]
    return hmac.compare_digest(candidate, expected_hash)


def init_db():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT NOT NULL,
                store_name TEXT NOT NULL,
                items TEXT,
                category TEXT,
                total_amount REAL NOT NULL DEFAULT 0,
                vat REAL NOT NULL DEFAULT 0,
                tax_deductible TEXT,
                status TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        receipt_columns = {
            row[1] for row in conn.execute("PRAGMA table_info(receipts)").fetchall()
        }

        if "user_id" not in receipt_columns:
            conn.execute("ALTER TABLE receipts ADD COLUMN user_id INTEGER")

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_receipts_user_id
            ON receipts (user_id)
            """
        )

        conn.commit()


def create_user(username, password):
    init_db()

    username = username.strip().lower()
    if not username:
        return False, "Username is required.", None

    if len(password) < 6:
        return False, "Password must be at least 6 characters.", None

    password_hash = _hash_password(password)

    try:
        with _connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
                """,
                (username, password_hash),
            )
            conn.commit()
            return True, "Account created successfully.", cursor.lastrowid
    except sqlite3.IntegrityError:
        return False, "That username is already registered.", None


def verify_user(username, password):
    init_db()

    username = username.strip().lower()

    with _connect() as conn:
        row = conn.execute(
            """
            SELECT id, username, password_hash
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

    if row is None:
        return False, None

    user_id, stored_username, stored_password = row
    if not _verify_password(password, stored_password):
        return False, None

    return True, {"id": user_id, "username": stored_username}


def insert_receipt(
    user_id,
    date,
    store_name,
    items,
    category,
    total_amount,
    vat,
    tax_deductible,
    status,
):
    init_db()

    if user_id is None:
        raise ValueError("A signed-in user is required to save receipts.")

    with _connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO receipts (
                user_id,
                date,
                store_name,
                items,
                category,
                total_amount,
                vat,
                tax_deductible,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                int(user_id),
                str(date),
                store_name,
                items,
                category,
                float(total_amount),
                float(vat),
                tax_deductible,
                status,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def delete_receipt(receipt_id, user_id):
    init_db()

    if user_id is None:
        return False

    with _connect() as conn:
        cursor = conn.execute(
            """
            DELETE FROM receipts
            WHERE id = ?
              AND user_id = ?
            """,
            (int(receipt_id), int(user_id)),
        )
        conn.commit()
        return cursor.rowcount > 0


def delete_all_receipts(user_id):
    init_db()

    if user_id is None:
        return 0

    with _connect() as conn:
        cursor = conn.execute(
            """
            DELETE FROM receipts
            WHERE user_id = ?
            """,
            (int(user_id),),
        )
        conn.commit()
        return cursor.rowcount


def get_receipts_for_user(user_id):
    init_db()

    if user_id is None:
        return pd.DataFrame(columns=RECEIPT_COLUMNS)

    with _connect() as conn:
        df = pd.read_sql_query(
            """
            SELECT
                id,
                user_id,
                date,
                store_name,
                items,
                category,
                total_amount,
                vat,
                tax_deductible,
                status
            FROM receipts
            WHERE user_id = ?
            ORDER BY date DESC, id DESC
            """,
            conn,
            params=(int(user_id),),
        )

    if df.empty:
        return pd.DataFrame(columns=RECEIPT_COLUMNS)

    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)
    df["vat"] = pd.to_numeric(df["vat"], errors="coerce").fillna(0)

    return df
