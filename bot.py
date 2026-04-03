import requests

# ================= 配置 =================
BOT_TOKEN = "你的机器人TOKEN"
CHAT_ID = "你的ID或频道ID"  #频道要加-100
# ========================================

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
    "Referer": "https://web.gpubgm.com/",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

def get_apk_urls():
    # 顺序：32位 在上，64位 在下
    targets = [
        ("32位", "https://web.gpubgm.com/m/download_android.html"),
        ("64位", "https://web.gpubgm.com/m/download_android_1.html")
    ]

    text = "获取当前最新安装包\n\n"

    for name, url in targets:
        try:
            # 发起请求
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()  # 网络错误直接抛出
            html = resp.text

            # 查找 APK 
            pos = html.find(".apk")
            if pos == -1:
                text += f"❌ {name} 获取失败\n\n"
                continue

            start = html.rfind("http", 0, pos)
            link = html[start:pos+4]
            
            # 校验链接是否有效
            if link.startswith("http"):
                text += f"x{name}\n{link}\n\n"
            else:
                text += f"❌ {name} 链接无效\n\n"

        except Exception as e:
            text += f"❌ {name} 请求异常：{str(e)[:20]}\n\n"

    return text

# 发送到 TG
def send_tg(text):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    try:
        requests.post(api_url, json=payload, timeout=10)
    except:
        print("发送失败")

# 主运行
if __name__ == "__main__":
    content = get_apk_urls()
    send_tg(content)
    print("完成")
