#!/usr/bin/env python3
"""A module for filtering logs.
"""
import logging
import csv
import os
import mysql.connector
import re


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    def __init__(self, fields):
        self.fields = fields
        super(RedactingFormatter, self).__init__("[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s")

    def format(self, record):
        record.message = filter_datum(record.message, self.fields)
        return super().format(record)

def filter_datum(message, fields):
    for field in fields:
        pattern = r"(?<!\w){}(?!\w)".format(re.escape(field))
        message = re.sub(pattern, "***", message)
    return message

def get_logger():
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger

def get_db():
    credentials = {
        "user": os.getenv("PERSONAL_DATA_DB_USERNAME"),
        "password": os.getenv("PERSONAL_DATA_DB_PASSWORD"),
        "host": os.getenv("PERSONAL_DATA_DB_HOST"),
        "database": os.getenv("PERSONAL_DATA_DB_NAME"),
    }
    return mysql.connector.connect(**credentials)

PII_FIELDS = ("email", "phone_number", "address", "credit_card", "social_security")

def main():
    db = get_db()
    cursor = db.cursor()

    query = "SELECT * FROM users"
    cursor.execute(query)
    rows = cursor.fetchall()

    logger = get_logger()
    logger.info("Filtered fields:\n")
    for row in rows:
        filtered_row = [row[field] for field in PII_FIELDS]
        logger.info(filtered_row)

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()

