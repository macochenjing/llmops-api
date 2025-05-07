# -*- coding: utf-8 -*-

"""
@Time   : 2025/5/7 13:03
@Author : chenjingmaco@gmail.com
@File   : __init__.py
"""

from .github_oauth import GithubOAuth
from .oauthbase import OAuthUserInfo, OAuth

__all__ = ["OAuthUserInfo", "OAuth", "GithubOAuth"]