from datetime import datetime


def get_system_time() -> datetime:
    return datetime.now()


def get_time_dif(late: datetime, early: datetime) -> float:
    return (late - early).total_seconds()
