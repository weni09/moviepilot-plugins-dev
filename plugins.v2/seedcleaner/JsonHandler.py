# !/usr/bin/env python
# -*-coding:utf-8 -*-
# ===================================================
# @Time : 2025/6/17 14:25                           
# @Author : weni09                                  
# @File : DataHandler.py
# @Description：
# ===================================================
import json
from pathlib import Path
from app.log import logger


class JsonHandler:
    def __init__(self, json_path: Path):
        self.save_path = json_path

    def save_to_json(self, data: dict):
        try:
            with self.save_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"保存json文件失败: {e}")

    def load_from_json(self) -> dict:
        try:
            if not self.save_path.exists():
                logger.warning(f"json文件不存在:{self.save_path}")
                return {}
            with self.save_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            logger.warning(f"加载json文件失败: {e}")
            return {}
