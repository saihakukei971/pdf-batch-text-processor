#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PDFTextFormatter-Batch - GUIモジュール
PySimpleGUIを使用したGUIインターフェース
"""

import PySimpleGUI as sg
import os
import threading
import webbrowser
from datetime import datetime
from src.batch import process_folder
from src.logger import setup_logger, get_log_file_path
from src.settings import load_settings
from src.schema import SplitMode
from src.utils import ensure_dir

# ロガーのセットアップ
logger = setup_logger()

def create_layout(settings):
    """GUIレイアウトを生成する"""
    # メニューバー
    menu_def = [
        ['ファイル', ['終了']],
        ['ヘルプ', ['ログを開く', 'バージョン情報']]
    ]

    # メインレイアウト
    layout = [
        [sg.Menu(menu_def)],
        [sg.Text('PDFファイルを整形して.txtに変換するツール', font=('Helvetica', 12))],
        [sg.Text('_' * 80)],
        [sg.Text('入力フォルダ', size=(15, 1)),
         sg.Input(key='-FOLDER-', size=(50, 1)),
         sg.FolderBrowse('参照', key='-BROWSE-', target='-FOLDER-')],
        [sg.Text('分割方式', size=(15, 1)),
         sg.Radio('全体', 'SPLIT', key='-FULL-', default=True),
         sg.Radio('半分', 'SPLIT', key='-HALF-'),
         sg.Radio('三分割', 'SPLIT', key='-THIRD-')],
        [sg.Text('出力先フォルダ:', size=(15, 1)),
         sg.Text(os.path.abspath('./outputs/'), key='-OUTPUT_PATH-', size=(50, 1))],
        [sg.Text('_' * 80)],
        [sg.Text('処理設定:')],
        [sg.Checkbox('。(句点)で改行', default=True, key='-KUTEN-'),
         sg.Checkbox('．(ドット)で改行', key='-DOT-'),
         sg.Checkbox('段落(字下げ)で改行', key='-DANRAKU-')],
        [sg.Checkbox('「」の中は改行しない', default=True, key='-QUOTE_NOLINE-'),
         sg.Checkbox('改行時に"」"を付ける', default=True, key='-ADD_QUOTE-')],
        [sg.Checkbox('タブを削除', default=True, key='-TAB-'),
         sg.Checkbox('スペースを削除', default=True, key='-SPACE-')],
        [sg.Text('_' * 80)],
        [sg.Button('実行', key='-EXECUTE-', size=(10, 1)),
         sg.Button('ログを表示', key='-VIEW_LOG-', size=(15, 1)),
         sg.Button('終了', key='-EXIT-', size=(10, 1))],
        [sg.Output(size=(80, 10), key='-OUTPUT-')]
    ]

    return layout

def get_split_mode(values):
    """GUIの値から分割モードを取得"""
    if values['-HALF-']:
        return SplitMode.HALF
    elif values['-THIRD-']:
        return SplitMode.THIRD
    else:
        return SplitMode.FULL

def process_with_progress(folder_path, split_mode, window):
    """進捗表示付きでフォルダを処理"""
    try:
        success_count, error_count = process_folder(folder_path, split_mode)
        window.write_event_value('-PROCESS_COMPLETE-', (success_count, error_count))
    except Exception as e:
        logger.error(f"処理中にエラーが発生しました: {str(e)}")
        window.write_event_value('-PROCESS_ERROR-', str(e))

def open_log_file():
    """現在日付のログファイルを開く"""
    log_file = get_log_file_path()
    if os.path.exists(log_file):
        if os.name == 'nt':  # Windows
            os.startfile(log_file)
        else:  # macOS/Linux
            webbrowser.open(f'file://{os.path.abspath(log_file)}')
    else:
        sg.popup_error(f"ログファイルが見つかりません: {log_file}")

def start_gui():
    """GUIアプリケーションを起動"""
    # 設定の読み込み
    settings = load_settings()

    # GUIテーマの設定
    sg.theme('DefaultElement')

    # レイアウトの作成
    layout = create_layout(settings)

    # ウィンドウの作成
    window = sg.Window('PDFテキスト整形ツール v2.0', layout, finalize=True)

    # 出力ディレクトリの作成
    output_dir = os.path.abspath('./outputs/')
    ensure_dir(output_dir)

    # メインイベントループ
    while True:
        event, values = window.read()

        # ウィンドウが閉じられたら終了
        if event == sg.WINDOW_CLOSED or event == '終了' or event == '-EXIT-':
            break

        # バージョン情報表示
        elif event == 'バージョン情報':
            sg.popup('PDFテキスト整形ツール', 'バージョン: 2.0.0', '制作日: 2025年5月')

        # ログファイルを開く
        elif event == 'ログを開く' or event == '-VIEW_LOG-':
            open_log_file()

        # 実行ボタン
        elif event == '-EXECUTE-':
            folder_path = values['-FOLDER-']
            if not folder_path:
                sg.popup_error('入力フォルダを選択してください。')
                continue

            if not os.path.isdir(folder_path):
                sg.popup_error(f"指定されたパスはフォルダではありません: {folder_path}")
                continue

            split_mode = get_split_mode(values)

            # 処理中表示に更新
            window['-EXECUTE-'].update(disabled=True)
            window['-OUTPUT-'].update('')
            print(f"フォルダ「{folder_path}」内のPDFファイルを処理しています...")
            print(f"分割モード: {split_mode.value}")

            # 別スレッドで処理を実行
            threading.Thread(
                target=process_with_progress,
                args=(folder_path, split_mode, window),
                daemon=True
            ).start()

        # 処理完了イベント
        elif event == '-PROCESS_COMPLETE-':
            success_count, error_count = values[event]
            print(f"処理完了: {success_count}ファイル成功, {error_count}ファイル失敗")
            print(f"出力先: {os.path.abspath('./outputs/')}")
            window['-EXECUTE-'].update(disabled=False)

            if success_count > 0:
                sg.popup_notify('処理完了', f'{success_count}ファイルの変換に成功しました')

            if error_count > 0:
                print(f"エラーの詳細はログファイルを確認してください")

        # 処理エラーイベント
        elif event == '-PROCESS_ERROR-':
            error_message = values[event]
            print(f"エラー: {error_message}")
            print("詳細はログファイルを確認してください")
            window['-EXECUTE-'].update(disabled=False)
            sg.popup_error(f"処理中にエラーが発生しました: {error_message}")

    # ウィンドウを閉じる
    window.close()