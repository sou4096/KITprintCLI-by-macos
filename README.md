# KIT Print CLI

macOSから金沢工業大学学内プリンターへ、PDFまたはPostScriptを直接送信するCLIツールです。
また、このツールはベータ版のため、今後仕様が変わる可能性が高いです。詳細はこのREADMEや今後追加予定のリリースノートを確認してください。現時点では、PDFまたはPostScriptファイルの送信を主な対象としており、白黒印刷、両面印刷、部数指定、Wordからの直接印刷などは今後の対応予定です。

## 現在のバージョン

現在の最新版は `v0.2.0-beta` です。

このバージョンでは、PDFまたはPostScriptファイルをmacOSからKIT学内プリンターへ送信できます。

## 概要

このツールは、PDFをPostScriptに変換し、HTTP Basic認証付きのIPP 1.0 Print-Jobとして `iogate3.kanazawa-it.ac.jp` に送信します。

## 対応環境

- macOS
- Python 3.9以上推奨
- 学内ネットワークまたはVPN接続

## インストール

以下のコマンドでリポジトリをダウンロードします。
```bash
git clone https://github.com/sou4096/KITprintCLI-by-macos.git ~/kitprint
```

その後、以下のコマンドを実行してください。
```bash
cd ~/kitprint
./install.sh
source ~/.zprofile
```

インストールが完了したら、次のコマンドで kitprint が使用できる状態になっているか確認してください。

```bash
which kitprint
```

以下のように表示されればインストール完了です。

```text
/Users/ユーザー名/bin/kitprint
```
## 初期設定
初回のみ以下の情報を入力して、ユーザー情報を保存してください。
まず、以下のコマンドを実行します。
```bash
kitprint --setup
```

ユーザー名は以下の形式になります。
```text
<入学年度><学籍番号>@kit-ad01.kanazawa-it.ac.jp
```

入学年度2024年、学籍番号が1234567の場合
```text
例：
20241234567@kit-ad01.kanazawa-it.ac.jp
```

入力したユーザー名は `~/.config/kitprint/config.json` に保存されます。

## 使い方

印刷したいPDFファイルまたはPostScriptファイルのパスを指定して実行します。

```bash
kitprint /path/to/file.pdf
```

例として、デスクトップにある `sample.pdf` を印刷する場合は、以下のように実行します。

```bash
kitprint ~/Desktop/sample.pdf
```

実行するとパスワードの入力を求められます。入力しても表示されませんが、入力はされているので安心してください。

```text
KIT password:
```

パスワードはKITのAD認証パスワードを入力します。初期パスワードの場合は、以下の形式です。
```text
hYYMMDD
```

例として、平成18年4月22日生まれの場合は以下のようになります。
```text
h180422
```

パスワードを入力して送信に成功すると、以下のようなメッセージが表示されます。

```text
HTTP 200 OK
IPP version: 1.0
IPP status: 0x0000
送信成功: プリンターで学生証をかざしてジョブを確認してください。
```

現在のフォルダ(カレントディレクトリ)にあるファイルを印刷する場合は、ファイル名だけでも指定できます。

```bash
kitprint sample.pdf
```

ジョブ名を指定したい場合は、`-n` オプションを使用します。

```bash
kitprint ~/Desktop/sample.pdf -n "report"
```

一時的に別のユーザー名を指定したい場合は、`-u` オプションを使用します。

```bash
kitprint ~/Desktop/sample.pdf -u "2024xxxxxxx@kit-ad01.kanazawa-it.ac.jp"
```

### 両面印刷

長辺とじの両面印刷を行う場合:

```bash
kitprint sample.pdf --duplex
```

または明示的に指定する場合:

```bash
kitprint sample.pdf --duplex long
```

短辺とじの両面印刷を行う場合:

```bash
kitprint sample.pdf --duplex short
```

### 片面印刷

片面印刷を明示する場合:

```bash
kitprint sample.pdf --simplex
```

## 注意事項
- このツールの使用には、Windowsと同じように学内ネットワーク、またはVPNの接続が必要です。
- PDFによっては、レイアウトや用紙サイズの影響で印刷結果が崩れる場合があります。
- WordやPowerPointのファイルを直接送信することはできません。PDFに書き出してから使用してください。
- 現段階では、カラー、片面印刷しか対応していません。
- パスワードは設定ファイルに保存されません。印刷時に毎回入力してください。

## 今後の予定
- 白黒印刷への対応
- 部数指定への対応
- GUI版の作成
- macOSアプリケーション化
- Wordなどの印刷画面から直接送信する仕組みの検討

## 対応状況

| 機能 | 状態 |
|---|---|
| PDF印刷 | 対応済み |
| PostScript印刷 | 対応済み |
| KIT ADユーザー設定保存 | 対応済み |
| 片面印刷 | 対応済み |
| 両面印刷（長辺とじ） | 対応済み |
| 両面印刷（短辺とじ） | 対応済み |
| 白黒印刷 | 調査中 |
| 部数指定 | 未対応 |
| GUI | 未対応 |

## アンインストール

以下のコマンドで、インストールしたコマンドと設定ファイルを削除できます。
```bash
rm -f ~/bin/kitprint
rm -rf ~/.config/kitprint
```

リポジトリ本体も削除する場合は、以下も実行してください。
```bash
rm -rf ~/kitprint
```
