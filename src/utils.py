#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ユーティリティモジュール - 補助関数
"""

import os
import pdfplumber
from datetime import datetime
from src.schema import SplitMode

def ensure_dir(dir_path):
    """
    ディレクトリが存在することを確認し、存在しなければ作成

    Args:
        dir_path (str): ディレクトリパス

    Returns:
        str: 作成されたディレクトリパス
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    return dir_path

def read_pdf_text(pdf_path):
   """
   PDFファイルからテキストを抽出

   Args:
       pdf_path (str): PDFファイルのパス

   Returns:
       str: 抽出されたテキスト
   """
   text = ""
   try:
       with pdfplumber.open(pdf_path) as pdf:
           for page in pdf.pages:
               page_text = page.extract_text()
               if page_text:
                   text += page_text + "\n"
   except Exception as e:
       raise ValueError(f"PDFファイルの読み込みに失敗しました: {str(e)}")

   return text

def get_output_path(file_name, timestamp=None, part=None):
   """
   出力ファイルのパスを生成

   Args:
       file_name (str): 元のファイル名（拡張子なし）
       timestamp (str, optional): タイムスタンプ
       part (int, optional): 分割番号

   Returns:
       str: 出力ファイルパス
   """
   if timestamp is None:
       timestamp = datetime.now().strftime('%Y%m%d')

   part_suffix = "" if part is None else f"_part{part}"
   output_filename = f"{file_name}_{timestamp}整形後{part_suffix}.txt"

   output_dir = ensure_dir("outputs")
   return os.path.join(output_dir, output_filename)

def split_text(text, split_mode=SplitMode.FULL):
   """
   テキストを指定されたモードで分割

   Args:
       text (str): 分割するテキスト
       split_mode (SplitMode): 分割モード

   Returns:
       list: 分割されたテキスト
   """
   if split_mode == SplitMode.FULL:
       return [text]

   lines = text.splitlines()
   line_count = len(lines)

   if line_count <= 1:
       return [text]

   if split_mode == SplitMode.HALF:
       # 半分に分割
       mid = line_count // 2
       return [
           "\n".join(lines[:mid]),
           "\n".join(lines[mid:])
       ]

   elif split_mode == SplitMode.THIRD:
       # 三分割
       third = line_count // 3
       return [
           "\n".join(lines[:third]),
           "\n".join(lines[third:2*third]),
           "\n".join(lines[2*third:])
       ]

   return [text]  # デフォルト

def save_text(text, output_path):
   """
   テキストをファイルに保存

   Args:
       text (str): 保存するテキスト
       output_path (str): 出力ファイルパス

   Returns:
       bool: 保存成功したかどうか
   """
   try:
       # ディレクトリがなければ作成
       os.makedirs(os.path.dirname(output_path), exist_ok=True)

       # ファイルに書き込み
       with open(output_path, "w", encoding="utf-8") as f:
           f.write(text)

       return True
   except Exception as e:
       raise IOError(f"ファイル保存エラー: {str(e)}")