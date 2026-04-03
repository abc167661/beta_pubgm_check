import requests

# ================= 配置 =================
BOT_TOKEN = "你的机器人TOKEN"
CHAT_ID = "你的ID或频道ID"
# ========================================

def get_apk_urls():
    # 顺序：32位 在上，64位 在下
    targets = [
        ("32位", "https://web.gpubgm.com/m/download_android.html"),
        ("64位", "https://web.gpubgm.com/m/download_android_1.html")
    ]

    text = "获取当前最新安装包\n\n"

    for name, url in targets:
        try:
            resp = requests.get(url, timeout=10)
            html = resp.text
            pos = html.find(".apk")

            if pos == -1:
                text += f"❌ {name} 获取失败\n\n"
                continue

            start = html.rfind("http", 0, pos)
            link = html[start:pos+4]
            text += f"x{name}\n{link}\n\n"

        except:
            text += f"❌{name} 异常\n\n"

    return text

# 发送到 TG
def send_tg(text):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(api_url, json=payload)

# 主运行
content = get_apk_urls()
send_tg(content)
print("完成")
