import logging
import re

class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        fields = record.getMessage().split(self.SEPARATOR)
        redacted_fields = filter_datum(fields, self.REDACTION, self.SEPARATOR)
        record.msg = self.SEPARATOR.join(redacted_fields)
        return super().format(record)


def filter_datum(fields, redaction, separator):
    return re.sub(r'({0})(?={1})'.format('|'.join(fields), re.escape(separator)), redaction, separator.join(fields))


# Usage example
logger = logging.getLogger("example_logger")
formatter = RedactingFormatter()
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Log message example
message = "Sensitive data: 123456789; Password: mypassword; API Key: abcdefg"
logger.warning(message)
