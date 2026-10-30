"""Creational pattern: Singleton database connection manager."""
import sqlite3
from pathlib import Path


class DatabaseManager:
    _instances = {}

    def __new__(cls, db_name="expenses.db"):
        key = str(db_name)
        if key not in cls._instances:
            instance = super().__new__(cls)
            instance._initialized = False
            cls._instances[key] = instance
        return cls._instances[key]

    def __init__(self, db_name="expenses.db"):
        if self._initialized:
            return
        self.db_name = str(db_name)
        self._connection = None
        self._initialized = True

    @classmethod
    def get_instance(cls, db_name="expenses.db"):
        return cls(db_name)

    def get_connection(self):
        if self._connection is None:
            if self.db_name != ":memory:":
                Path(self.db_name).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
            self._connection = sqlite3.connect(self.db_name)
            self._connection.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT ''
                )
            """)
            columns = {row[1] for row in self._connection.execute("PRAGMA table_info(expenses)")}
            if "description" not in columns:
                self._connection.execute(
                    "ALTER TABLE expenses ADD COLUMN description TEXT NOT NULL DEFAULT ''"
                )
            self._connection.commit()
        return self._connection

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    @classmethod
    def clear_instances(cls):
        for instance in cls._instances.values():
            instance.close()
        cls._instances.clear()
