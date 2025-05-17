#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PDFTextFormatter-Batch - メインエントリーポイント
PDFを読み取り、改行や句読点を整形し .txt に変換・保存する自動ツール
"""

import sys
import os
import argparse
from datetime import datetime
from src.batch import process_folder
from src.logger import setup_logger
from src.settings import load_settings
from src.schema import SplitMode
import PySimpleGUI as sg

logger = setup_logger()

def parse_arguments():
    """コマンドライン引数をパース"""
    parser = argparse.ArgumentParser(description='PDFテキスト整形ツール')
    parser.add_argument('--folder', '-f', help='処理するPDFが含まれるフォルダパス')
    parser.add_argument('--split', '-s', choices=['full', 'half', 'third'],
                        default='full', help='分割モード (full=全体, half=半分, third=三分割)')
    return parser.parse_args()

def run_cli():
    """CLIモードで実行"""
    args = parse_arguments()

    if not args.folder:
        print("エラー: フォルダパスを指定してください (--folder オプション)")
        sys.exit(1)

    if not os.path.isdir(args.folder):
        print(f"エラー: 指定されたパスはフォルダではありません: {args.folder}")
        sys.exit(1)

    settings = load_settings()
    split_mode = SplitMode(args.split)

    try:
        success_count, error_count = process_folder(args.folder, split_mode)
        logger.info(f"処理完了: 成功={success_count}, 失敗={error_count}")
        print(f"処理完了: {success_count}ファイル成功, {error_count}ファイル失敗")
    except Exception as e:
        logger.error(f"処理中にエラーが発生しました: {str(e)}")
        print(f"エラー: {str(e)}")
        sys.exit(1)

def run_gui():
    """GUIモードで実行"""
    from gui_app import start_gui
    start_gui()

if __name__ == "__main__":
    # 引数が指定されている場合はCLIモード、そうでない場合はGUIモード
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_gui()