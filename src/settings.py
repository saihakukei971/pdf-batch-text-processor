#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
設定管理モジュール - 設定の読み込みと管理
"""

import os
import toml
from src.schema import AppSettings
from src.logger import setup_logger

logger = setup_logger()

def get_config_path():
    """
    設定ファイルのパスを取得

    Returns:
        str: 設定ファイルのパス
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "config", "settings.toml")

def load_settings():
    """
    設定ファイルから設定を読み込む

    Returns:
        AppSettings: アプリケーション設定
    """
    config_path = get_config_path()

    # デフォルト設定
    settings = AppSettings()

    # 設定ファイルが存在すれば読み込み
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = toml.load(f)

            # Pydanticモデルにデータを渡す
            settings = AppSettings(**config_data)
            logger.info(f"設定ファイルを読み込みました: {config_path}")
        except Exception as e:
            logger.error(f"設定ファイル読み込みエラー: {str(e)}")
    else:
        logger.warning(f"設定ファイルが見つかりません。デフォルト設定を使用します: {config_path}")
        # デフォルト設定ファイルの保存
        save_settings(settings)

    return settings

def save_settings(settings):
    """
    設定をファイルに保存

    Args:
        settings (AppSettings): 保存する設定

    Returns:
        bool: 保存成功したかどうか
    """
    config_path = get_config_path()

    try:
        # ディレクトリがなければ作成
        os.makedirs(os.path.dirname(config_path), exist_ok=True)

        # 設定ファイルに書き込み
        with open(config_path, "w", encoding="utf-8") as f:
            toml.dump(settings.dict(), f)

        logger.info(f"設定ファイルを保存しました: {config_path}")
        return True
    except Exception as e:
        logger.error(f"設定ファイル保存エラー: {str(e)}")
        return False