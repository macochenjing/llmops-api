# -*- coding: utf-8 -*-

"""
@Time   : 2025/1/7 17:10
@Author : chenjingmaco@gmail.com
@File   : app.py
"""

from datetime import datetime
import uuid
from sqlalchemy import (
    Column,
    UUID,
    String,
    Text,
    DateTime,
    PrimaryKeyConstraint,
    Index,
    text,
)
from internal.extension.database_extension import db

class App(db.Model):
    """ai应用基础模型类型"""
    __tablename__ = "app"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_app_id"),
        Index("idx_app_account_id", "account_id")
    )

    # id = Column(UUID, default=uuid.uuid4, nullable=False)
    # account_id = Column(UUID, nullable=False)
    # name = Column(String(255), default="", nullable=False)
    # icon = Column(String(255), default="", nullable=False)
    # description = Column(Text, default="", nullable=False)
    # status = Column(String(255), default="", nullable=False)
    # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    # created_at = Column(DateTime, default=datetime.now, nullable=False)

    id = Column(UUID, nullable=False, server_default=text("uuid_generate_v4()"))
    account_id = Column(UUID)
    name = Column(String(255), nullable=False, server_default=text("''::character varying")) #变成可变长度
    icon = Column(String(255), nullable=False, server_default=text("''::character varying")) #变成可变长度
    description = Column(Text, nullable=False, server_default=text("''::text"))
    status = Column(String(255), nullable=False, server_default=text("''::character varying")) #变成可变长度
    updated_at = Column(DateTime, onupdate=datetime.now, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP(0)"),
                        server_onupdate=text("CURRENT_TIMESTAMP(0)"))
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP(0)"))