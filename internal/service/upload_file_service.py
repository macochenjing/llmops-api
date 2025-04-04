# -*- coding: utf-8 -*-

"""
@Time   : 2025/4/4 14:38
@Author : chenjingmaco@gmail.com
@File   : upload_file_service.py
"""
from dataclasses import dataclass

from injector import inject

from internal.model import UploadFile
from pkg.sql.sqlalchemy import SQLAlchemy
from .base_service import BaseService


@inject
@dataclass
class UploadFileService(BaseService):
    """上传文件记录服务"""
    db: SQLAlchemy

    def create_upload_file(self, **kwargs) -> UploadFile:
        """创建文件上传记录"""
        return self.create(UploadFile, **kwargs)
