from datetime import datetime, timezone, timedelta


def format_timestamp_to_time(timestamp: int) -> str:
    """
    将时间戳转换为东八区时间格式 "YYYY-MM-DD HH:MM:SS"
    """
    # 直接使用东八区创建datetime对象
    china_time = datetime.fromtimestamp(timestamp, tz=timezone(timedelta(hours=8)))
    return china_time.strftime("%Y-%m-%d %H:%M:%S")

