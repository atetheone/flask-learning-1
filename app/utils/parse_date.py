from app.constants import errors


def parse_date(date_str: str):
    """Parse a date string into a datetime object"""
    from datetime import datetime
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError(errors.INVALID_DATE_FORMAT)
