#!/usr/bin/env python3
"""
filtered_logger module
Handles filtering of personal identifiable information (PII) in log records.
"""

import re
import logging
from typing import List
import os
import mysql.connector

PII_FIELDS: tuple = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Replaces field values with redaction string using regex.
    """
    pattern = rf"({'|'.join(fields)})=.*?{separator}"
    return re.sub(
        pattern,
        lambda m: f"{m.group(1)}={redaction}{separator}",
        message
    )


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class that redacts specified fields from log messages.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format and redact log message fields.
        """
        original = super().format(record)
        return filter_datum(
            self.fields,
            self.REDACTION,
            original,
            self.SEPARATOR
        )


def get_logger() -> logging.Logger:
    """
    Returns a configured logger that redacts PII fields.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to a MySQL database using credentials from environment variables.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    if database is None:
        raise ValueError(
            "Missing required env variable: PERSONAL_DATA_DB_NAME"
        )

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main() -> None:
    """
    Connects to DB, retrieves user data,
    logs each entry with PII fields redacted.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [
        desc[0] for desc in cursor.description
    ]
    logger = get_logger()
    for row in cursor:
        parts = [
            f"{field}={str(value)}"
            for field, value in zip(field_names, row)
        ]
        msg = "; ".join(parts) + ";"
        logger.info(msg)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
