import html
import json
import os
import sys

import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TAG = os.getenv("TAG")
RUN_ID = os.getenv("RUN_ID")

IS_STABLE = "-" not in TAG

CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "@MiniClashPro")
# The public Bot API stops at 50 MB, which is under every APK and dmg here, so
# the workflow starts a local Bot API server and posts through that instead.
# It serves the same methods with a 2 GB cap; the public one still has 50 MB,
# and one oversized file fails the whole media group.
API_BASE = os.getenv("TELEGRAM_API_URL", "http://localhost:8081")
LOCAL_API = "localhost" in API_BASE or "127.0.0.1" in API_BASE
UPLOAD_LIMIT = 2000 * 1024 * 1024 if LOCAL_API else 45 * 1024 * 1024

DIST_DIR = os.path.join(os.getcwd(), "dist")
# Rendered by `tool/changelog.dart render telegram`: plain bullets, already
# truncated to fit the caption limit. release.md carries the download table and
# would blow past that limit.
release = os.path.join(os.getcwd(), "telegram.md")

text = ""

media = []
files = {}

i = 1

releaseKeywords = [
    "windows-amd64-setup",
    "android-arm64",
    "macos-arm64",
    "macos-amd64"
]

for file in os.listdir(DIST_DIR):
    file_path = os.path.join(DIST_DIR, file)
    if os.path.isfile(file_path):
        file_lower = file.lower()
        if (
            any(kw in file_lower for kw in releaseKeywords)
            and os.path.getsize(file_path) <= UPLOAD_LIMIT
        ):
            file_key = f"file{i}"
            media.append({
                "type": "document",
                "media": f"attach://{file_key}"
            })
            files[file_key] = open(file_path, 'rb')
            i += 1

if TAG:
    text += f"\n<b>{html.escape(TAG)}</b>\n"

if IS_STABLE:
    text += f"\nhttps://github.com/MinimaxFlora/MiniClash/releases/tag/{TAG}\n"
else:
    text += f"\nhttps://github.com/MinimaxFlora/MiniClash/actions/runs/{RUN_ID}\n"

if os.path.exists(release):
    text += "\n"
    with open(release, 'r') as f:
        text += f.read()
    text += "\n"

# A 403 only says the bot is not in the channel, never which bot the secret
# belongs to, so name the token's bot and its membership before the attempt.
me = requests.get(f"{API_BASE}/bot{TELEGRAM_BOT_TOKEN}/getMe", timeout=30).json()
bot = me.get("result") or {}
print(f"Bot: @{bot.get('username')} (id {bot.get('id')})")
member = requests.get(
    f"{API_BASE}/bot{TELEGRAM_BOT_TOKEN}/getChatMember",
    params={"chat_id": CHAT_ID, "user_id": bot.get("id")},
    timeout=30,
).json()
print(
    f"Membership in {CHAT_ID}: {member.get('result', {}).get('status')} "
    f"{member.get('description', '')}".rstrip()
)

# HTML, not Markdown: the caption carries changelog entries written by whoever
# wrote the commit, and HTML is the one Telegram parse mode with a defined
# escape for them. `tool/changelog.dart render telegram` emits matching markup.
if len(media) > 1:
    media[-1]["caption"] = text
    media[-1]["parse_mode"] = "HTML"
    request = {
        "url": f"{API_BASE}/bot{TELEGRAM_BOT_TOKEN}/sendMediaGroup",
        "data": {"chat_id": CHAT_ID, "media": json.dumps(media)},
        "files": files,
    }
elif media:
    # A media group needs two items, and one installer under the upload limit
    # is the normal case once the APKs outgrow it.
    request = {
        "url": f"{API_BASE}/bot{TELEGRAM_BOT_TOKEN}/sendDocument",
        "data": {
            "chat_id": CHAT_ID,
            "document": "attach://file1",
            "caption": text,
            "parse_mode": "HTML",
        },
        "files": files,
    }
else:
    request = {
        "url": f"{API_BASE}/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        "data": {
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": "true",
        },
        "files": None,
    }

try:
    response = requests.post(
        request["url"],
        data=request["data"],
        files=request["files"],
        timeout=300
    )
finally:
    for handle in files.values():
        handle.close()

# A rejected caption comes back as a 400 with a description, not an exception.
# Without this the release job stays green while the announcement never posted.
try:
    payload = response.json()
except ValueError:
    payload = None

print("Response JSON:", payload if payload is not None else response.text)

if not response.ok or not (payload or {}).get("ok"):
    description = (payload or {}).get("description", response.text)
    print(f"Telegram rejected the release post: {description}", file=sys.stderr)
    sys.exit(1)
