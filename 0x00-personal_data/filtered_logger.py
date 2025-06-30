#!/usr/bin/env python3
"""
A module for logging, PII filtering, and database interaction.
It provides tools to handle user data securely by redacting
personally identifiable information from logs.
"""
import re
import logging
from typing import List
import os
import mysql.connector
from mysql.connector import connection

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message using a single regex.

    Args:
        fields (List[str]): A list of strings representing fields to obfuscate.
        redaction (str): The string to replace the field value with.
        message (str): The log line string.
        separator (str): The character separating fields in the log line.

    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class to filter PII from log records.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the RedactingFormatter.

        Args:
            fields (List[str]): A list of strings representing fields to
                                obfuscate in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a LogRecord, redacting sensitive information.

        It filters the message of the log record using `filter_datum` before
        passing it to the parent class's format method.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted and redacted log string.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger named 'user_data'.

    The logger is configured to log INFO level messages, not to propagate
    to other loggers, and to use a StreamHandler with a
    RedactingFormatter.

    Returns:
        logging.Logger: A configured logger object for user data.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """
    Returns a connector to the secure database.

    This function connects to the database using credentials stored
    in environment variables.

    Returns:
        mysql.connector.connection.MySQLConnection: A connection object to
                                                    the database.
    """
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    cnx = mysql.connector.connect(user=username,
                                  password=password,
                                  host=host,
                                  database=db_name)
    return cnx


def main():
    """
    Main function to retrieve user data, log it with redaction.

    This function fetches user records from a database and logs them
    to the console with PII fields obfuscated. It runs when the
    module is executed as a script.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    field_names = [i[0] for i in cursor.description]

    for row in cursor:
        message_parts = [f"{field}={value}" for field, value in
                         zip(field_names, row)]
        message = "; ".join(message_parts) + ";"
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
