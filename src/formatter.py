#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
整形処理モジュール - テキストの改行・句点処理
"""

import re
from src.logger import setup_logger
from src.settings import load_settings

logger = setup_logger()

def format_text(text, config=None):
    """
    テキストを整形処理する

    Args:
        text (str): 整形前のテキスト
        config (dict, optional): 整形設定。指定しない場合は設定ファイルから読み込み

    Returns:
        str: 整形後のテキスト
    """
    if not config:
        settings = load_settings()
        config = settings.get('formatting', {})

    logger.info("テキスト整形開始")

    if not text:
        logger.warning("空のテキストが入力されました")
        return ""

    # 行ごとに分割
    sentences = text.splitlines()
    result_lines = []

    # 整形フラグ
    is_first_line = True
    in_quote = False

    for line in sentences:
        processed_line = line.strip()

        # 空行はスキップ
        if len(processed_line) <= 2:
            result_lines.append("")
            continue

        # タブの削除
        if config.get('remove_tab', True):
            processed_line = processed_line.replace('\t', '')

        # スペースの削除
        if config.get('remove_space', True) and not config.get('english_mode', False):
            processed_line = processed_line.replace(' ', '').replace('　', '')

        # 箇条書きの処理
        if is_bullet_point(processed_line, config):
            if result_lines and not result_lines[-1].endswith('\n'):
                result_lines[-1] += '\n'
            result_lines.append(processed_line)
            continue

        # 段落処理
        if config.get('paragraph_break', False):
            if not is_first_line and len(processed_line) > 2 and (processed_line[0] == ' ' or processed_line[0] == '　'):
                if result_lines and not result_lines[-1].endswith('\n'):
                    result_lines[-1] += '\n'
                # 字下げを追加（全角スペース2つ）
                processed_line = '　　' + processed_line.lstrip()

        is_first_line = False

        # 「」の処理
        if processed_line.startswith('「'):
            in_quote = True
            if result_lines and not result_lines[-1].endswith('\n'):
                result_lines[-1] += '\n'

        # 改行処理
        processed_line = insert_line_breaks(processed_line, in_quote, config)

        # 「」内の処理
        if in_quote and '」' in processed_line:
            if not config.get('quote_break_inside', False):
                # 「」内は改行しない設定の場合
                processed_line = processed_line.replace('」\n', '」')
                processed_line += '\n'

            in_quote = False

        result_lines.append(processed_line)

    # 結果を結合
    result = '\n'.join(result_lines)

    logger.info(f"テキスト整形完了: {len(sentences)}行 -> {len(result.splitlines())}行")
    return result

def is_bullet_point(line, config):
    """
    行が箇条書きかどうかを判定

    Args:
        line (str): 判定する行
        config (dict): 設定

    Returns:
        bool: 箇条書きならTrue
    """
    if not line:
        return False

    bullet_symbols = config.get('bullet_symbols', ['・', '●', '〇', '■', '□', '◆', '◇', '▲', '△', '▼', '▽'])
    custom_bullets = config.get('custom_bullets', [])

    if isinstance(custom_bullets, str):
        custom_bullets = custom_bullets.split(',')

    all_bullets = bullet_symbols + custom_bullets

    return len(line) > 0 and line[0] in all_bullets

def insert_line_breaks(text, in_quote, config):
    """
    設定に基づいて改行を挿入

    Args:
        text (str): 改行を挿入するテキスト
        in_quote (bool): 「」内かどうか
        config (dict): 設定

    Returns:
        str: 改行挿入後のテキスト
    """
    # 改行対象の文字
    break_chars = []

    if config.get('break_at_kuten', True):
        break_chars.append('。')

    if config.get('break_at_dot', False):
        break_chars.append('．')

    # その他の改行文字
    custom_breaks = config.get('custom_break_chars', [])
    if isinstance(custom_breaks, str):
        custom_breaks = custom_breaks.split(',')

    break_chars.extend(custom_breaks)

    # 改行の挿入
    for char in break_chars:
        if char in text:
            text = text.replace(char, char + '\n')

    # 英文用のピリオド処理
    if config.get('english_mode', False):
        text = re.sub(r'\. +([A-Z])', r'.\n\1', text)

    # 「」内の処理
    if in_quote and config.get('quote_break_inside', False):
        if config.get('add_closing_quote', True):
            # 改行を一旦「」で置換し、後で」\nに置換
            text = text.replace('\n', '」「')
            text = text.replace('「」', '')  # 空の「」を削除
            text = text.replace('」', '」\n')

    return text