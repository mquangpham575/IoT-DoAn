from datetime import datetime, timedelta, timezone


def now_local_string() -> str:
    """
    Return local timestamp (UTC+7) in a format that is easy to display on dashboard.
    """
    vntime = datetime.now(timezone.utc) + timedelta(hours=7)
    return vntime.strftime("%Y-%m-%d %H:%M:%S")
