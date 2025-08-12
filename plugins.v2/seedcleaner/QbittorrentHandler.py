# !/usr/bin/env python
# -*-coding:utf-8 -*-
# ===================================================
# @Time : 2025/6/19 13:53                           
# @Author : weni09                                  
# @File : DownloaderHandler.py
# @Description：
# ===================================================
from pathlib import Path
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse

import qbittorrentapi
from qbittorrentapi import TorrentInfoList, Version, Client, TorrentState, TorrentDictionary, Tracker, TrackersList
from app.plugins.seedcleaner.DefinedConsts import TorrentStatus
from app.log import logger
from app.plugins.seedcleaner.DataModel import TorrentModel

QBITTORRENT = "qbittorrent"


class QbittorrentHandler:
    def __init__(self, name: str):
        self.client: Client = None
        self.name = name
        self.supported_app_versions = list(Version.supported_app_versions())
        self.supported_api_versions = list(Version.supported_api_versions())
        self.supported_app_versions.sort(key=lambda x: x)
        self.supported_api_versions.sort(key=lambda x: x)
        logger.debug(f"支持的APP版本{self.supported_app_versions},支持的API版本{self.supported_api_versions}")
        self.uncompleted_suffix = ".!qB"

    def connect(self, host='localhost', port=8080, username='admin', password='admin'):
        """连接到Qbittorrent"""
        try:
            self.client = qbittorrentapi.Client(
                host=host,
                port=port,
                username=username,
                password=password
            )
            logger.info(f"{self.name} 当前APP版本:{self.client.app_version()},"
                        f"API版本{self.client.app_web_api_version()}")
            return True
        except qbittorrentapi.LoginFailed as e:
            logger.error(f"登录{QBITTORRENT}:{host}:{port}失败: {e}")
            return False
        except Exception as e:
            logger.error(f"连接{QBITTORRENT}:{host}:{port}失败: {e}")
            return False

    def disconnect(self):
        """断开与Qbittorrent的连接"""
        if self.client:
            self.client.auth_log_out()
            self.client = None
            logger.debug(f"已断开与{self.name} ({QBITTORRENT})的连接")

    def get_all_torrents(self) -> list[Any] | TorrentInfoList:
        """获取所有种子信息"""
        if not self.client:
            logger.warning("未连接到Qbittorrent")
            return []

        try:
            torrents = self.client.torrents_info()
            return torrents
        except Exception as e:
            logger.warning(f"获取种子信息失败: {e}")
            return []

    def get_torrent_contents(self, torrent_hash) -> List[Dict[str, Any]]:
        """获取指定种子的内容列表（文件名和大小）

        Args:
            torrent_hash (str): 种子的哈希值
        Returns:
            list: 包含文件名和大小的字典列表，例如 [{'name': 'file1.txt', 'size': 12345}, ...]
        """
        if not self.client:
            print("未连接到Qbittorrent")
            return []

        try:
            # 获取种子的文件信息
            files = self.client.torrents_files(torrent_hash=torrent_hash)
            contents = [{"name": file['name'], "size": file['size']} for file in files]
            contents.sort(key=lambda x: x['name'] + str(x['size']))
            return contents
        except Exception as e:
            logger.error(f"获取种子内容失败: {e}")
            return []

    def get_torrent_trackers(self, torrent_hash) -> TrackersList:
        """
        获取种子的Trackers
        :param torrent_hash: 种子hash
        :return: TrackersList
        """
        return self.client.torrents_trackers(torrent_hash=torrent_hash)

    def get_torrent_trackers_domains(self, torrent_hash) -> List[str]:
        """
        获取种子的Trackers域名
        :param torrent_hash: 种子hash
        :return: TrackersList
        """
        trackers = self.get_torrent_trackers(torrent_hash)
        urls = set()
        for tracker in trackers:
            if str(tracker['url']).startswith('http'):
                urls.add(str(tracker['url']))
        if not trackers:
            return []

        def _get_domain(url):
            try:
                parsed = urlparse(url)
                if parsed.hostname:
                    return parsed.hostname
                else:
                    return ""
            except Exception as e:
                return ""

        return [_get_domain(_url) for _url in urls]

    def get_torrent_trackers_msg(self, torrent_hash: str) -> List[str]:
        """
        获取种子的Trackers信息
        :param torrent_hash: 种子hash
        :return: TrackersList
        """
        trackers = self.get_torrent_trackers(torrent_hash)
        msg = set()
        for tracker in trackers:
            if str(tracker['url']).startswith('http') and tracker['msg']:
                msg.add(tracker['msg'])
        return list(msg)

    def _get_only_one_error_msg(self, torrent: TorrentDictionary) -> str:
        msg_list = self.get_torrent_trackers_msg(torrent.hash)
        if len(msg_list) > 0 and torrent.state_enum.is_errored:
            return msg_list[0]
        return ""

    def delete_torrent(self, torrent_hash: str | List[str] = "", delete_files=False):
        """删除指定的种子（通过hash）

        Args:
            torrent_hash (str): 种子的哈希值
            torrent_name （str): 种子名称，可选
            delete_files (bool): 是否同时删除文件，默认False
        """
        if not self.client:
            logger.error("未连接到Qbittorrent")
            return False
        try:
            if len(torrent_hash) == 0:
                logger.info("没有指定种子ID,无需删除")
                return True
            # 调用 qbittorrentapi 删除种子
            self.client.torrents_delete(torrent_hashes=torrent_hash, delete_files=delete_files)
            logger.info(f"{self.name} 已删除 {len(torrent_hash)} 个种子 {'(包含文件)' if delete_files else '(仅种子)'}")
            return True
        except Exception as e:
            logger.error(f"{self.name} 删除种子失败: {e}")
            return False

    def _is_missing_file(self, torrent: TorrentDictionary, data_path: Path = None) -> bool:
        if torrent.state_enum == TorrentState.MISSING_FILES:
            return True
        if data_path and (not data_path.exists() and not data_path.with_suffix(self.uncompleted_suffix).exists()):
            return True
        return False

    def get_torrent_status_text(self, torrent: TorrentDictionary, data_path: Path = None) -> str:
        if self._is_missing_file(torrent, data_path):
            return TorrentStatus.MISSING_FILES.value
        if torrent.state_enum.is_downloading:
            return TorrentStatus.DOWNLOADING.value
        if torrent.state_enum.is_uploading:
            return TorrentStatus.UPLOADING.value
        if torrent.state_enum.is_complete:
            return TorrentStatus.COMPLETED.value
        if torrent.state_enum.is_checking:
            return TorrentStatus.CHECKING.value
        if torrent.state_enum == TorrentState.ERROR:
            return TorrentStatus.ERROR.value
        if torrent.state_enum.is_paused or torrent.state_enum.is_stopped:
            return TorrentStatus.STOPPED.value
        return TorrentStatus.UNKNOWN.value

    def build_torrent_list(self) -> Dict[str, TorrentModel]:
        torrent_list: TorrentInfoList = self.get_all_torrents()
        res_dict: Dict[str, TorrentModel] = {}
        for torrent in torrent_list:
            torrent_file_list = self.get_torrent_contents(torrent.hash)
            first_file_tuple = ()
            end_file_tuple = ()
            if len(torrent_file_list) > 0:
                first_file_tuple = (torrent_file_list[0]['name'], torrent_file_list[0]['size'])
                end_file_tuple = (torrent_file_list[-1]['name'], torrent_file_list[-1]['size'])
            data_path = Path(torrent.save_path) / torrent.name
            torrent_model = TorrentModel(
                client=QBITTORRENT,
                client_name=self.name,
                id=torrent.hash,
                save_path=torrent.save_path,
                name=torrent.name,
                total_size=torrent.total_size,
                hash=torrent.hash,
                trackers=self.get_torrent_trackers_domains(torrent.hash),
                file_count=len(torrent.files),
                first_file=first_file_tuple,
                end_file=end_file_tuple,
                data_missing=self._is_missing_file(torrent, data_path),
                # 添加做种人数和种子状态
                seeds=torrent.num_complete if hasattr(torrent, 'num_complete') else 0,
                status=self.get_torrent_status_text(torrent, data_path),
                error=self._get_only_one_error_msg(torrent)
            )
            res_dict[torrent.hash] = torrent_model
        logger.info(f"下载器 '{self.name}' (类型:{QBITTORRENT}) 获取种子: {len(res_dict)} 个")
        return res_dict
