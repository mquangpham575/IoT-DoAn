from datetime import datetime


def now_local_string() -> str:
    """
    Return local timestamp in a format that is easy to display on dashboard.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
