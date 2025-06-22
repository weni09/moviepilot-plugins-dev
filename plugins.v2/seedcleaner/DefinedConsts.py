from urllib.parse import urlparse

QBITTORRENT = "qbittorrent"
TRANSMISSION = "transmission"

ALL_SELECTED = "all"  # 全部
NO_AUX = "no_aux"  # 无辅
HAS_AUX = "has_aux"  # 有辅
ONLY_TORRENT = "only_torrent"  # 仅种子
ONLY_DATA = "only_data"  # 仅数据 # 废弃，只有删种子和删除全部（种子和文件）

DOWNLOADER_CONFIG_TYPE_SYSTEM = "system"
DOWNLOADER_CONFIG_TYPE_CUSTOM = "custom"

VIDEO_SUFFIX_LIST = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm',
                     '.mpeg', '.mpg', '.3gp', '.ts', '.m4v', '.rmvb', '.rm', '.vob', '.asf', '.ogv']

TORRENT_INFO_FILE_NAME = "torrent_info.json"

