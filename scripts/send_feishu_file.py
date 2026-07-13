import argparse
import json
import mimetypes
import os
import uuid
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_CHAT_ID = "oc_ab3da5be78816bc84a94449b371fa1ca"
DEFAULT_CONFIG = Path.home() / ".openclaw-autoclaw" / "openclaw.json"

TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
FILE_URL = "https://open.feishu.cn/open-apis/im/v1/files"
MESSAGE_URL = "https://open.feishu.cn/open-apis/im/v1/messages"


def request_json(url: str, *, method: str = "POST", headers: dict | None = None, body: bytes | None = None) -> dict:
    request = urllib.request.Request(url, method=method, headers=headers or {}, data=body)
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Feishu API HTTP {error.code}: {detail}") from error
    return json.loads(payload)


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8-sig"))


def load_credentials(config_path: Path) -> tuple[str, str]:
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    if app_id and app_secret:
        return app_id, app_secret

    if not config_path.exists():
        raise SystemExit(
            "Missing Feishu credentials. Set FEISHU_APP_ID/FEISHU_APP_SECRET "
            f"or create {config_path}."
        )

    config = load_config(config_path)
    feishu = config.get("channels", {}).get("feishu", {})
    app_id = feishu.get("appId") or feishu.get("app_id")
    app_secret = feishu.get("appSecret") or feishu.get("app_secret")
    if not app_id or not app_secret:
        raise SystemExit("Feishu credentials were not found in config.")
    return app_id, app_secret


def load_chat_id(config_path: Path, explicit_chat_id: str | None) -> str:
    if explicit_chat_id:
        return explicit_chat_id

    env_chat_id = os.environ.get("FEISHU_CHAT_ID")
    if env_chat_id:
        return env_chat_id

    config = load_config(config_path)
    feishu = config.get("channels", {}).get("feishu", {})
    return feishu.get("chatId") or feishu.get("chat_id") or DEFAULT_CHAT_ID


def get_tenant_token(app_id: str, app_secret: str) -> str:
    body = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode("utf-8")
    response = request_json(
        TOKEN_URL,
        headers={"Content-Type": "application/json"},
        body=body,
    )
    if response.get("code") != 0:
        raise SystemExit(f"Failed to get tenant_access_token: {response}")
    return response["tenant_access_token"]


def encode_multipart(fields: dict[str, str], files: dict[str, tuple[str, bytes, str]]) -> tuple[bytes, str]:
    boundary = f"----WorldModelRadar{uuid.uuid4().hex}"
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                value.encode("utf-8"),
                b"\r\n",
            ]
        )
    for name, (filename, content, content_type) in files.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                (
                    f'Content-Disposition: form-data; name="{name}"; '
                    f'filename="{filename}"\r\n'
                ).encode(),
                f"Content-Type: {content_type}\r\n\r\n".encode(),
                content,
                b"\r\n",
            ]
        )
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), boundary


def upload_file(token: str, path: Path, file_type: str) -> str:
    filename = path.name
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    body, boundary = encode_multipart(
        {"file_type": file_type, "file_name": filename},
        {"file": (filename, path.read_bytes(), content_type)},
    )
    response = request_json(
        FILE_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        body=body,
    )
    if response.get("code") != 0:
        raise SystemExit(f"Failed to upload file to Feishu: {response}")
    return response["data"]["file_key"]


def send_file_message(token: str, chat_id: str, file_key: str) -> dict:
    params = urllib.parse.urlencode({"receive_id_type": "chat_id"})
    body = json.dumps(
        {
            "receive_id": chat_id,
            "msg_type": "file",
            "content": json.dumps({"file_key": file_key}),
        }
    ).encode("utf-8")
    response = request_json(
        f"{MESSAGE_URL}?{params}",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        body=body,
    )
    if response.get("code") != 0:
        raise SystemExit(f"Failed to send Feishu file message: {response}")
    return response


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload a file and send it to a Feishu chat.")
    parser.add_argument("file", type=Path, help="File to send.")
    parser.add_argument("--chat-id", default=None)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--file-type", default="stream")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    path = args.file.resolve()
    if not path.exists() or not path.is_file():
        raise SystemExit(f"File not found: {path}")

    chat_id = load_chat_id(args.config, args.chat_id)
    if args.dry_run:
        print(json.dumps({"file": str(path), "chat_id": chat_id, "dry_run": True}, indent=2))
        return

    app_id, app_secret = load_credentials(args.config)
    token = get_tenant_token(app_id, app_secret)
    file_key = upload_file(token, path, args.file_type)
    response = send_file_message(token, chat_id, file_key)
    print(json.dumps({"sent": True, "chat_id": chat_id, "file": str(path), "response": response}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
