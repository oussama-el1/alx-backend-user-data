#!/usr/bin/env python3
"""
0. Regex-ing : filter_datum
"""
import re
import logging


def filter_datum(fields, redaction, message, separator) -> object:
    """
    filter_datum
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
