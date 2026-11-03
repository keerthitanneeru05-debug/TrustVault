import sqlite3

DATABASE = "trustvault.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            owner_id INTEGER NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (owner_id) REFERENCES users(id)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            document_id INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            details TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (document_id) REFERENCES documents(id)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS document_shares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            owner_id INTEGER NOT NULL,
            shared_with INTEGER NOT NULL,
            permission TEXT NOT NULL DEFAULT 'view',
            shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (document_id) REFERENCES documents(id),
            FOREIGN KEY (owner_id) REFERENCES users(id),
            FOREIGN KEY (shared_with) REFERENCES users(id),
            UNIQUE(document_id, shared_with)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    init_db()
    print("TrustVault database initialized successfully!")