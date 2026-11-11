#This file creates and connects to the local SQLite database

import os
import sqlite3

# The database file will be saved next to these Python files.
DATABASE_FILE = os.path.join(os.path.dirname(__file__), "inventory.db")


def get_connection(database_file=None):
    # Use the normal database unless a different one is given (for tests).
    if database_file is None:
        database_file = DATABASE_FILE

    connection = sqlite3.connect(database_file)

    # Rows can now be read by column name, like row "quantity"
    connection.row_factory = sqlite3.Row
    return connection


def create_database(database_file=None):
    connection = get_connection(database_file)

    try:
        # IF NOT EXISTS prevents the table from being recreated every time.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY COLLATE NOCASE,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity >= 0),
                low_stock_threshold INTEGER NOT NULL
                    CHECK (low_stock_threshold >= 0)
            )
        """)

        # Save the new table to the database file.
        connection.commit()
    finally:
        # Close the database connection even if something goes wrong.
        connection.close()