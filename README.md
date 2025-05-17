# pdf-text-formatter

## 📘 概要
PDFをテキストに変換し、「文章が読みやすくなるよう」改行や句読点を自動整形するPythonツールです。テキストの自然な区切りを認識し、文章の構造を保ちながら読みやすい形に変換します。実務で扱うPDFレポートやマニュアルの引用・編集作業を効率化するために開発しました。

**主なユースケース**: 
- 会議資料からの引用文作成
- 報告書からの要約作成
- PDFマニュアルからの手順抽出

本ツールは当初、広告主・広告代理店での業務効率化のために開発しましたが、以下のような幅広い業界・業務でも活用可能です：

**様々な業界での活用例**：
- **法務・法律**: 契約書や判例文書からの条項抽出・整形
- **医療・製薬**: 論文や臨床報告書からの要点整理
- **金融・投資**: 有価証券報告書やマーケットレポートの分析
- **教育・研究**: 学術論文や教材からの引用・参考文献作成
- **製造業**: 技術マニュアルや仕様書の可読性向上
- **不動産**: 重要事項説明書や契約書の条項整理
- **IT・技術**: APIドキュメントやリファレンスの読みやすい形への変換

## 🚀 主な機能

| 機能 | 説明 |
|------|------|
| 📂 **バッチ処理** | フォルダ内のPDFファイルを一括変換・整形・保存 |
| 🧾 **高度な整形** | 句点/括弧/段落を認識し自然な読みやすさを実現 |
| 🔢 **柔軟な分割** | 「全文・半分・三分割」から選べる保存方法 |
| 🪵 **詳細ログ** | 日付別フォルダに処理内容を自動記録 |
| 💻 **マルチUI** | GUI・CLIどちらでも操作可能 |

## 💡 技術スタック

```
Python 3.9+
├── pdfplumber - PDF解析エンジン
├── loguru - 構造化ログ出力
├── pydantic - 型定義・バリデーション
├── PySimpleGUI - モダンなGUIフレームワーク
├── dynaconf - 設定管理
└── typer - CLIインターフェース
```

## ⚙️ アーキテクチャ

本ツールは以下の設計原則に基づいています：

1. **責務の分離**: 各モジュールが単一責任を持つ設計
2. **型安全**: Pydanticによる厳格な型チェックでバグを防止
3. **柔軟な設定**: 外部ファイルでの設定管理
4. **充実したログ**: 障害特定やパフォーマンス分析が容易

### 処理フロー

```
PDF読み取り → テキスト抽出 → 整形処理(句読点/改行/括弧) → 分割 → ファイル保存 → ログ記録
```

## 🔧 セットアップと実行

### インストール

```bash
# リポジトリのクローン
git clone https://github.com/yourusername/pdf-text-formatter.git
cd pdf-text-formatter

# 依存パッケージのインストール
pip install -r requirements.txt
```

### バッチ実行（Windows）

Windows環境では、以下の`run.bat`ファイルを使って簡単に実行できます：

```bat
@echo off
setlocal enabledelayedexpansion

REM ======= PDFテキスト整形ツール バッチ実行 =======
echo PDF整形ツール起動中...

REM 環境変数設定
set PYTHONPATH=%~dp0
set OUTPUT_DIR=%~dp0outputs
set LOG_DIR=%~dp0log

REM 入力パラメータ処理
set PDF_FOLDER=%1
set SPLIT_MODE=%2

if "%PDF_FOLDER%"=="" (
    echo エラー: PDFフォルダが指定されていません。
    echo 使用方法: run.bat PDFフォルダパス [分割モード(full/half/third)]
    exit /b 1
)

if "%SPLIT_MODE%"=="" (
    set SPLIT_MODE=full
)

REM 出力先ディレクトリ確認
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM 実行日付取得
for /f "tokens=1-3 delims=/" %%a in ('echo %date%') do (
    set DAY=%%a
    set MONTH=%%b
    set YEAR=%%c
)
set DATE_STAMP=%YEAR%%MONTH%%DAY%

echo 処理開始: %DATE_STAMP%
echo 入力フォルダ: %PDF_FOLDER%
echo 分割モード: %SPLIT_MODE%
echo 出力先: %OUTPUT_DIR%

REM Python実行
python main.py --folder "%PDF_FOLDER%" --split %SPLIT_MODE%

if %ERRORLEVEL% NEQ 0 (
    echo エラーが発生しました。ログを確認してください。
) else (
    echo 処理完了！
    echo 結果は %OUTPUT_DIR% フォルダに保存されました。
)

echo ログファイル: %LOG_DIR%\%DATE_STAMP%\実行ログ.txt

endlocal
```

### バッチ実行（Linux/macOS）

Linux/macOSでは、以下の`run.sh`スクリプトを使用します：

```bash
#!/bin/bash

# ======= PDFテキスト整形ツール バッチ実行 =======
echo "PDF整形ツール起動中..."

# 引数チェック
if [ -z "$1" ]; then
    echo "エラー: PDFフォルダが指定されていません。"
    echo "使用方法: ./run.sh PDFフォルダパス [分割モード(full/half/third)]"
    exit 1
fi

# 入力パラメータ処理
PDF_FOLDER="$1"
SPLIT_MODE="${2:-full}"  # デフォルトはfull

# 環境変数設定
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="$SCRIPT_DIR"
OUTPUT_DIR="$SCRIPT_DIR/outputs"
LOG_DIR="$SCRIPT_DIR/log"

# 出力先ディレクトリ確認
mkdir -p "$OUTPUT_DIR"

# 実行日付取得
DATE_STAMP=$(date +%Y%m%d)

echo "処理開始: $DATE_STAMP"
echo "入力フォルダ: $PDF_FOLDER"
echo "分割モード: $SPLIT_MODE"
echo "出力先: $OUTPUT_DIR"

# Python実行
python3 main.py --folder "$PDF_FOLDER" --split "$SPLIT_MODE"

if [ $? -ne 0 ]; then
    echo "エラーが発生しました。ログを確認してください。"
else
    echo "処理完了！"
    echo "結果は $OUTPUT_DIR フォルダに保存されました。"
fi

echo "ログファイル: $LOG_DIR/$DATE_STAMP/実行ログ.txt"
```

### GUI起動方法

```bash
# GUI起動（対話的に操作）
python main.py
```

### CLIモード直接実行

```bash
# フォルダ内のPDFを全て処理（全文保存）
python main.py --folder ./sample_pdfs --split full

# 三分割で保存
python main.py --folder ./sample_pdfs --split third
```

### GUI実行画面

```
+------------------------- PDFテキスト整形ツール v2.0 -------------------------+
|                                                                              |
|  ファイル(F)  ヘルプ(H)                                                      |
|                                                                              |
|  PDFファイルを整形して.txtに変換するツール                                   |
|  --------------------------------------------------------------------        |
|                                                                              |
|  入力フォルダ [C:\Users\user\Documents\PDF資料\_____________] [参照]         |
|                                                                              |
|  分割方式    (●) 全体    ( ) 半分    ( ) 三分割                              |
|                                                                              |
|  出力先フォルダ: C:\Users\user\pdf-text-formatter\outputs\                   |
|  --------------------------------------------------------------------        |
|                                                                              |
|  処理設定:                                                                   |
|  [✓] 。(句点)で改行    [ ] ．(ドット)で改行    [ ] 段落(字下げ)で改行        |
|  [✓] 「」の中は改行しない    [✓] 改行時に"」"を付ける                        |
|  [✓] タブを削除    [✓] スペースを削除                                       |
|  --------------------------------------------------------------------        |
|                                                                              |
|  [    実行    ] [ ログを表示 ] [    終了    ]                                |
|                                                                              |
|  +------------------------------------------------------------------+        |
|  | フォルダ「C:\Users\user\Documents\PDF資料」内のPDFファイルを処理 |        |
|  | しています...                                                    |        |
|  | 分割モード: full                                                 |        |
|  | 営業資料.pdf → 成功                                              |        |
|  | 技術仕様書.pdf → 成功                                            |        |
|  | 会議議事録.pdf → 成功                                            |        |
|  | 処理完了: 3ファイル成功, 0ファイル失敗                          |        |
|  | 出力先: C:\Users\user\pdf-text-formatter\outputs\                |        |
|  +------------------------------------------------------------------+        |
|                                                                              |
+------------------------------------------------------------------------------+
```

### CLI実行画面（コマンドプロンプト）

```
C:\Users\user\pdf-text-formatter>run.bat C:\Users\user\Documents\PDF資料 third
PDF整形ツール起動中...
処理開始: 20250518
入力フォルダ: C:\Users\user\Documents\PDF資料
分割モード: third
出力先: C:\Users\user\pdf-text-formatter\outputs

フォルダ「C:\Users\user\Documents\PDF資料」内のPDFファイルを処理しています...
分割モード: third
営業資料.pdf → 成功 (3分割保存)
技術仕様書.pdf → 成功 (3分割保存)
会議議事録.pdf → 成功 (3分割保存)
処理完了: 3ファイル成功, 0ファイル失敗
出力先: C:\Users\user\pdf-text-formatter\outputs

処理完了！
結果は C:\Users\user\pdf-text-formatter\outputs フォルダに保存されました。
ログファイル: C:\Users\user\pdf-text-formatter\log\20250518\実行ログ.txt

C:\Users\user\pdf-text-formatter>
```

### ログファイル例 (実行ログ.txt)

```
[2025-05-18 09:15:23] INFO - PDFテキスト整形ツール v2.0 起動
[2025-05-18 09:15:24] INFO - 設定ファイルを読み込みました: C:\Users\user\pdf-text-formatter\config\settings.toml
[2025-05-18 09:15:25] INFO - 処理開始: 入力フォルダ=C:\Users\user\Documents\PDF資料, 分割モード=third
[2025-05-18 09:15:26] INFO - 「営業資料.pdf」の処理を開始
[2025-05-18 09:15:27] INFO - PDFからテキスト抽出完了: 25241文字
[2025-05-18 09:15:28] INFO - テキスト整形完了: 128行 → 247行
[2025-05-18 09:15:29] INFO - 分割保存: part1=82行, part2=82行, part3=83行
[2025-05-18 09:15:29] INFO - 「営業資料.pdf」→ 成功 (3分割保存)
[2025-05-18 09:15:30] INFO - 「技術仕様書.pdf」の処理を開始
[2025-05-18 09:15:31] INFO - PDFからテキスト抽出完了: 18765文字
[2025-05-18 09:15:32] INFO - テキスト整形完了: 94行 → 156行
[2025-05-18 09:15:32] INFO - 分割保存: part1=52行, part2=52行, part3=52行
[2025-05-18 09:15:33] INFO - 「技術仕様書.pdf」→ 成功 (3分割保存)
[2025-05-18 09:15:34] INFO - 「会議議事録.pdf」の処理を開始
[2025-05-18 09:15:35] INFO - PDFからテキスト抽出完了: 8354文字
[2025-05-18 09:15:36] INFO - テキスト整形完了: 42行 → 79行
[2025-05-18 09:15:36] INFO - 分割保存: part1=26行, part2=26行, part3=27行
[2025-05-18 09:15:37] INFO - 「会議議事録.pdf」→ 成功 (3分割保存)
[2025-05-18 09:15:38] INFO - 処理完了: 成功=3, 失敗=0
```

## 📊 出力例

処理結果は以下のような構成で保存されます：

```
outputs/
├── 報告書A_20250518整形後_part1.txt
├── 報告書A_20250518整形後_part2.txt
└── ...

log/
└── 20250518/
    └── 実行ログ.txt
```

## 🧠 工夫した点

### 1. 処理精度の向上
- **箇条書き認識**: 各種記号（・◯■▲など）を自動検出
- **括弧内処理**: 「」内の文は改行しないよう特殊処理
- **英文対応**: 英語文章のピリオド処理にも対応

### 2. 保守性と拡張性
- **設定外部化**: .tomlファイルで挙動を細かく調整可能
- **型システム**: Pydanticによる型安全な設計
- **モジュール分離**: 機能ごとに責務を分離し拡張性を確保

### 3. 運用性の向上
- **詳細ログ**: 日付別・処理別に構造化されたログ出力
- **エラー処理**: 異常系を適切にハンドリングし安定動作
- **二重UI**: GUI/CLI両対応で様々な利用シーンに対応

## 🔍 実装の詳細

### テキスト整形アルゴリズム

本ツールの核となる整形ロジックは、自然言語処理の知見を活かした独自のルールベースアルゴリズムを実装しています：

1. **文の区切り認識**: 句点や記号を検出し適切な改行を挿入
2. **箇条書き処理**: リスト形式を維持しつつ整形
3. **括弧内処理**: 「」内の文章構造を保持する特殊ルール
4. **段落認識**: インデントや先頭スペースから段落を検出

カスタム可能なルールセットにより、業務文書や技術文書など様々な文書タイプに対応できます。

## 📝 今後の展望

- マルチPDF同時処理のスレッド化
- 正規表現ベースの高度なカスタムルール
- 特定業界向けの専用整形プリセット
- OCR機能の統合（画像PDFへの対応）
