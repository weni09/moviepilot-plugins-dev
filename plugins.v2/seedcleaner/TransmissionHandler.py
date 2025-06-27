from pathlib import Path
from typing import List, Dict, Optional, Union, Literal
from urllib.parse import urlparse

from transmission_rpc import Client

from app.log import logger
from app.plugins.seedcleaner.DataModel import TorrentModel

TRANSMISSION = "transmission"


class TransmissionHandler:
    def __init__(self, name: str):
        self.client = None
        self.name: str = name

    def connect(self, host='localhost', port=9091, username: str = "", password: str = ""):
        """连接到Transmission"""
        try:
            protocol: Literal["http", "https"] = "http"
            if host.startswith(("http://", "https://")):
                parsed_url = urlparse(host)
                scheme = parsed_url.scheme
                if scheme in ("http", "https"):
                    protocol = scheme
                host = parsed_url.hostname or host
            self.client = Client(
                protocol=protocol,
                host=host,
                port=port,
                username=username,
                password=password
            )
            logger.info(
                f"{self.name} 当前APP版本:{self.client.get_session().version},"
                f"RPC-API版本:{self.client.get_session().rpc_version},"
                f"RPC-API最小支持版本:{self.client.get_session().rpc_version_minimum}")
            return True
        except Exception as e:
            logger.error(f"连接{TRANSMISSION}:{host}:{port}失败: {e}")
            return False

    def disconnect(self):
        """断开与Transmission的连接"""
        self.client = None
        logger.debug(f"已断开与{self.name} ({TRANSMISSION})的连接")

    @staticmethod
    def _get_domain(url):
        try:
            parsed = urlparse(url)
            if parsed.hostname:
                return parsed.hostname
            else:
                return ""
        except Exception as e:
            logger.error(f"获取域名失败: {e}")
            return ""

    def get_all_torrents(self) -> Dict[str, TorrentModel]:
        """获取所有种子信息"""
        if not self.client:
            logger.warning("未连接到Transmission")
            return {}
        try:
            torrent_list = self.client.get_torrents()
            torrents_info = {}
            for torrent in torrent_list:
                trackers = [self._get_domain(str(tracker.announce)) for tracker in torrent.trackers]
                files = [{"name": file.name, "size": file.size} for file in torrent.get_files()]
                files.sort(key=lambda x: x['name'] + str(x['size']))
                data_path = Path(torrent.download_dir) / torrent.name
                torrents_info[torrent.hashString]: TorrentModel = TorrentModel(
                    client=TRANSMISSION,
                    client_name=self.name,
                    id=torrent.id,
                    save_path=torrent.download_dir,
                    name=torrent.name,
                    total_size=torrent.total_size,
                    hash=torrent.hashString,
                    trackers=trackers,
                    file_count=len(files),
                    first_file=(files[0]['name'], files[0]['size']),
                    end_file=(files[-1]['name'], files[-1]['size']),
                    data_missing=(not data_path.exists()) and not Path(str(data_path)+".part").exists()
                )
            logger.info(f"下载器 '{self.name}' (类型:{TRANSMISSION}) 获取种子: {len(torrents_info)} 个")
            return torrents_info
        except Exception as e:
            logger.warning(f"获取种子信息失败: {e}")
            return {}

    def delete_torrent(self, torrent_id: Union[str, int] | List[Union[str, int]], delete_files=False):
        """删除指定的种子（通过ID）"""
        if not self.client:
            logger.error("未连接到Transmission")
            return False
        try:
            if len(torrent_id) == 0:
                logger.info("没有指定种子ID,无需删除")
                return True
            self.client.remove_torrent(ids=torrent_id, delete_data=delete_files)
            logger.info(f"{self.name} 已删除 {len(torrent_id)} 个种子 {'(包含文件)' if delete_files else '(仅种子)'}")
            return True
        except Exception as e:
            logger.error(f"删除种子失败: {e}")
            return False

    def build_torrent_list(self) -> Dict[str, TorrentModel]:
        return self.get_all_torrents()
