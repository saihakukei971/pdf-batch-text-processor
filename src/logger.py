#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ログ機能モジュール - ログ出力の設定と管理
"""

import os
import sys
from datetime import datetime
from loguru import logger
from src.utils import ensure_dir

def get_log_dir():
    """
    ログディレクトリのパスを取得

    Returns:
        str: ログディレクトリのパス
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(base_dir, "log")
    return log_dir

def get_log_file_path():
    """
    現在の日付に対応するログファイルパスを取得

    Returns:
        str: ログファイルのパス
    """
    today = datetime.now().strftime('%Y%m%d')
    log_dir = os.path.join(get_log_dir(), today)
    ensure_dir(log_dir)
    return os.path.join(log_dir, "実行ログ.txt")

def setup_logger():
    """
    ロガーを設定する

    Returns:
        Logger: 設定済みのロガーオブジェクト
    """
    # 既存のハンドラをクリア
    logger.remove()

    # コンソール出力の設定
    logger.add(
        sys.stderr,
        format="<level>{level: <8}</level> | <green>{time:YYYY-MM-DD HH:mm:ss}</green> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )

    # ファイル出力の設定
    log_file = get_log_file_path()
    logger.add(
        log_file,
        format="[{time:YYYY-MM-DD HH:mm:ss}] {level} - {message}",
        level="INFO",
        rotation="1 day",
        compression="zip"
    )

    return logger