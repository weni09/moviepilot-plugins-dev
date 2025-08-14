import json
from typing import Tuple, List, Union, Dict

from pydantic import BaseModel, Field


class DownloaderInfoModel(BaseModel):
    name: str = ""
    type: str = ""  # 下载器类型: qbittorrent,transmission
    host: str = ""
    port: int = 0
    username: str = ""
    password: str = ""


class DownloaderModel(BaseModel):
    system: List[DownloaderInfoModel] = []
    custom: List[DownloaderInfoModel] = []


class ConfigModel(BaseModel):
    enable: bool = True
    exclude_paths: str = ""
    extra_dir_paths: str = ""
    downloaders: DownloaderModel = DownloaderModel()


class MissingOptions(BaseModel):
    seed: bool = Field(default=False, description="种子")
    file: bool = Field(default=False, description="源文件")


class FilterModel(BaseModel):
    path: str = ""
    client_name: str = ""
    client: str = ""
    size_limit: Tuple[int | None, int | None] = ()  # 前端默认单位为MB
    seeds_limit: Tuple[int | None, int | None] = ()
    live_time: int = 0  # 单位默认:天


class SearchModel(BaseModel):
    missingOptions: MissingOptions
    auxOption: str = "all"
    removeOption: str = "all"
    trackerInput: str = ""
    existingSeedData: bool = False
    name: str = ""
    page: int = 1
    limit: int = 50
    sortBy: Tuple[str, str] = ("name", "asc")
    filter: FilterModel


class ClearModel(BaseModel):
    type: str = ""  # 要清理对象的类型: torrent(种子)，file(缺失种子的源文件)
    hash: str = ""
    path: str = ""  # 仅删除源文件时，填写文件路径
    name: str = ""
    size: int = 0
    client_name: str = ""  # 下载器名称
    data_missing: bool = False
    removeOption: str = ""  # all # only_torrent


class TorrentModel(BaseModel):
    client: str = ""  # 下载器类型
    client_name: str = ""  # 下载器名称
    id: Union[str, int] = ""
    save_path: str = ""
    hash: str = ""
    total_size: int = 0
    name: str = ""
    file_count: int = 0
    first_file: Tuple = ()
    end_file: Tuple = ()
    trackers: List = []
    index: str = ""
    data_missing: bool = False
    seeds: int = 0
    status: str = ""
    error: str = ""
    created_at: str = ""


class MissingTorrentFileModel(BaseModel):
    type: str = "file"
    name: str = ""
    size: int = 0
    path: str = ""
    hash: str = ""


class ResponseModel(BaseModel):
    code: str = ""
    message: str = ""
    data: Union[List, Dict] = None

    def dict(self, *args, **kwargs):
        if self.data:
            return {
                "code": self.code,
                "message": self.message,
                "data": self.data,
            }
        else:
            return {
                "code": self.code,
                "message": self.message,
            }

    def __repr__(self):
        return self.json()

    def __call__(self, *args, **kwargs):
        return self.json()

    def json(self, *args, **kwargs):
        return json.dumps(self.dict(), *args, **kwargs)


class ResponseSuccessModel(ResponseModel):
    code: str = "ok"
    message: str = "成功"


class ResponseFailedModel(ResponseModel):
    code: str = "error"
    message: str = "错误"
