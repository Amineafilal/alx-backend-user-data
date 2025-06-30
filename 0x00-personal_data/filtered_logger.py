#!/usr/bin/env python3
"""
Module for filtering and logging personal data securely.

This module provides functionality to obfuscate sensitive information
in log messages and connect to databases securely.
"""

import logging
import mysql.connector
import os
import re
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscate specified fields in a log message using regex.

    Args:
        fields: List of field names to obfuscate
        redaction: String to replace field values with
        message: Log message containing field=value pairs
        separator: Character separating fields in the message

    Returns:
        Log message with specified fields obfuscated
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for filtering sensitive data in logs.

    This formatter obfuscates specified fields in log records
    to prevent sensitive information from appearing in logs.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with fields to redact.

        Args:
            fields: List of field names to obfuscate in log messages
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record with sensitive fields obfuscated.

        Args:
            record: LogRecord instance to format

        Returns:
            Formatted log message with sensitive fields redacted
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Create and configure a logger for user data with PII filtering.

    Returns:
        Configured Logger instance that filters PII fields
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connect to the database using environment variables.

    Returns:
        MySQL database connection object
    """
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
    return connection


def main() -> None:
    """
    Main function to retrieve and display filtered user data.

    Connects to the database, retrieves all users, and displays
    their information with PII fields obfuscated.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    logger = get_logger()

    for row in cursor:
        message = "name={}; email={}; phone={}; ssn={}; password={}; " \
                  "ip={}; last_login={}; user_agent={};".format(*row)
        logger.info(message)

        cursor.close()
        db.close()


if __name__ == "__main__":
    main()
