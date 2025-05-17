#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
バッチ処理モジュール - フォルダ内のPDFファイル一括処理
"""

import os
import glob
from datetime import datetime
from src.formatter import format_text
from src.utils import read_pdf_text, save_text, split_text
from src.logger import setup_logger
from src.schema import SplitMode

logger = setup_logger()

def process_folder(folder_path, split_mode=SplitMode.FULL):
    """
    指定フォルダ内のすべてのPDFファイルを処理

    Args:
        folder_path (str): 処理するPDFファイルが含まれるフォルダパス
        split_mode (SplitMode): 分割モード（全体・半分・三分割）

    Returns:
        tuple: (成功数, 失敗数)
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"指定されたパスはフォルダではありません: {folder_path}")

    # 実行日時
    timestamp = datetime.now().strftime('%Y%m%d')

    # PDFファイル一覧を取得
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))

    if not pdf_files:
        logger.warning(f"フォルダ内にPDFファイルが見つかりません: {folder_path}")
        return 0, 0

    success_count = 0
    error_count = 0

    for pdf_file in pdf_files:
        try:
            # ファイル名（拡張子なし）
            file_name = os.path.splitext(os.path.basename(pdf_file))[0]

            # PDFをテキストに変換
            raw_text = read_pdf_text(pdf_file)

            if not raw_text:
                logger.error(f"{file_name}.pdf → PDFの内容を読み取れません")
                error_count += 1
                continue

            # テキスト整形
            formatted_text = format_text(raw_text)

            # 分割して保存
            parts = split_text(formatted_text, split_mode)

            # 保存
            for i, part in enumerate(parts):
                part_suffix = "" if len(parts) == 1 else f"_part{i+1}"
                output_filename = f"{file_name}_{timestamp}整形後{part_suffix}.txt"

                # 保存
                output_path = os.path.join("outputs", output_filename)
                save_text(part, output_path)

            # ログ記録
            split_info = "" if split_mode == SplitMode.FULL else f" ({split_mode.value}分割保存)"
            logger.info(f"{file_name}.pdf → 成功{split_info}")
            success_count += 1

        except Exception as e:
            logger.error(f"{os.path.basename(pdf_file)} → 処理失敗: {str(e)}")
            error_count += 1

    return success_count, error_count