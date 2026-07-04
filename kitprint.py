#!/usr/bin/env python3
import argparse
import base64
import getpass
import http.client
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile

HOST = "iogate3.kanazawa-it.ac.jp"
PORT = 80
PATH = "/printers/netpr01c/.printer"
PRINTER_URI = f"ipp://{HOST}:80{PATH}"

CONFIG_DIR = os.path.expanduser("~/.config/kitprint")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")


def load_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"設定ファイルを読み込めません: {CONFIG_PATH}", file=sys.stderr)
        print(f"detail: {e}", file=sys.stderr)
        return {}


def save_config(config: dict) -> None:
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    os.chmod(CONFIG_PATH, 0o600)


def setup_config() -> None:
    print("KIT Print 初期設定")
    print("ユーザー名は <入学年度><学籍番号>@kit-ad01.kanazawa-it.ac.jp の形式です。")
    user = input("KIT user: ").strip()

    if not user:
        print("ユーザー名が空です。", file=sys.stderr)
        sys.exit(2)

    config = {
        "user": user
    }

    save_config(config)
    print(f"設定を保存しました: {CONFIG_PATH}")
    print("パスワードは保存しません。印刷時に毎回入力します。")


def ipp_attr(tag: int, name: str, value: str) -> bytes:
    name_b = name.encode("ascii")
    value_b = value.encode("utf-8")
    return (
        bytes([tag])
        + len(name_b).to_bytes(2, "big")
        + name_b
        + len(value_b).to_bytes(2, "big")
        + value_b
    )


def check_connection() -> None:
    try:
        with socket.create_connection((HOST, PORT), timeout=5):
            return
    except OSError as e:
        print(f"接続できません: {HOST}:{PORT}", file=sys.stderr)
        print("学内ネットワークまたはVPN接続を確認してください。", file=sys.stderr)
        print(f"detail: {e}", file=sys.stderr)
        sys.exit(2)


def convert_pdf_to_ps(pdf_path: str, ps_path: str) -> None:
    cupsfilter = shutil.which("cupsfilter")
    if not cupsfilter:
        print("cupsfilter が見つかりません。", file=sys.stderr)
        sys.exit(2)

    cmd = [
        cupsfilter,
        "-i", "application/pdf",
        "-m", "application/postscript",
        pdf_path,
    ]

    with open(ps_path, "wb") as out:
        result = subprocess.run(cmd, stdout=out, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print("PDFからPostScriptへの変換に失敗しました。", file=sys.stderr)
        print(result.stderr.decode("utf-8", errors="replace"), file=sys.stderr)
        sys.exit(1)


def build_ipp_print_job(ps_path: str, user: str, job_name: str) -> bytes:
    with open(ps_path, "rb") as f:
        document = f.read()

    body = bytearray()
    body += b"\x01\x00"              # IPP version 1.0
    body += b"\x00\x02"              # Print-Job
    body += (1).to_bytes(4, "big")   # request-id
    body += b"\x01"                  # operation-attributes-tag

    body += ipp_attr(0x47, "attributes-charset", "utf-8")
    body += ipp_attr(0x48, "attributes-natural-language", "ja")
    body += ipp_attr(0x45, "printer-uri", PRINTER_URI)
    body += ipp_attr(0x42, "requesting-user-name", user)
    body += ipp_attr(0x42, "job-name", job_name)
    body += ipp_attr(0x49, "document-format", "application/postscript")

    body += b"\x03"                  # end-of-attributes-tag
    body += document
    return bytes(body)


def send_print_job(ps_path: str, user: str, password: str, job_name: str) -> None:
    ipp_body = build_ipp_print_job(ps_path, user, job_name)
    token = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("ascii")

    headers = {
        "Content-Type": "application/ipp",
        "Authorization": f"Basic {token}",
        "Content-Length": str(len(ipp_body)),
    }

    conn = http.client.HTTPConnection(HOST, PORT, timeout=30)
    conn.request("POST", PATH, body=ipp_body, headers=headers)
    resp = conn.getresponse()
    data = resp.read()

    if resp.status != 200:
        print(f"HTTP error: {resp.status} {resp.reason}", file=sys.stderr)
        print(f"received: {len(data)} bytes", file=sys.stderr)
        sys.exit(1)

    if len(data) < 8:
        print("IPP応答が短すぎます。", file=sys.stderr)
        print(f"received: {len(data)} bytes", file=sys.stderr)
        sys.exit(1)

    ipp_version = f"{data[0]}.{data[1]}"
    ipp_status = int.from_bytes(data[2:4], "big")
    request_id = int.from_bytes(data[4:8], "big")

    print("HTTP 200 OK")
    print(f"IPP version: {ipp_version}")
    print(f"IPP status: 0x{ipp_status:04x}")
    print(f"request-id: {request_id}")

    if ipp_status == 0x0000:
        print("送信成功: プリンターで学生証をかざしてジョブを確認してください。")
    else:
        print("IPPエラーです。", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="KIT iogate3 にPDFまたはPostScript印刷ジョブを送信します。"
    )
    parser.add_argument("file", nargs="?", help="送信する .pdf または .ps ファイル")
    parser.add_argument("-u", "--user", help="KIT ADユーザー名")
    parser.add_argument("-n", "--name", help="ジョブ名")
    parser.add_argument("--setup", action="store_true", help="ユーザー設定を作成・更新する")
    args = parser.parse_args()

    if args.setup:
        setup_config()
        return

    if not args.file:
        print("印刷するファイルを指定してください。", file=sys.stderr)
        print("例: ./kitprint.py sample.pdf", file=sys.stderr)
        print("初期設定: ./kitprint.py --setup", file=sys.stderr)
        sys.exit(2)

    config = load_config()

    input_path = os.path.abspath(os.path.expanduser(args.file))
    if not os.path.exists(input_path):
        print(f"ファイルが存在しません: {input_path}", file=sys.stderr)
        sys.exit(2)

    user = args.user or config.get("user")
    if not user:
        print("KIT user が未設定です。", file=sys.stderr)
        print("./kitprint.py --setup を実行するか、-u で指定してください。", file=sys.stderr)
        sys.exit(2)

    password = getpass.getpass("KIT password: ")
    job_name = args.name or os.path.basename(input_path)

    check_connection()

    lower = input_path.lower()

    if lower.endswith(".ps"):
        send_print_job(input_path, user, password, job_name)

    elif lower.endswith(".pdf"):
        with tempfile.TemporaryDirectory() as tmpdir:
            ps_path = os.path.join(tmpdir, "output.ps")
            print("PDFをPostScriptに変換中...")
            convert_pdf_to_ps(input_path, ps_path)
            print("変換完了。送信中...")
            send_print_job(ps_path, user, password, job_name)

    else:
        print("対応している形式は .pdf と .ps です。", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
