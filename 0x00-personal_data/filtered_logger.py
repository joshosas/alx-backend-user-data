#!/usr/bin/env python3
"""A module for filtering logs.
"""
import re


def filter_datum(fields, redaction, message, separator):
    return re.sub(r'({0})(?={1})'.format('|'.join(fields), re.escape(separator)), redaction, message)

