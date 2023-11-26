import gpt
import tts_edge
from __init__ import url, url_live

from playwright.sync_api import sync_playwright
import time

def generate_response(message):
    danmu_response = gpt.gpt_response(message)
    return danmu_response

def response(message, danmu_input, danmu_enter, PreProcess=True):
    tts_edge.tts_response(message)
    if PreProcess:
        for i in range(len(message)//26+1):
            danmu_input.fill(f"Bot：{message[i*26:(i+1)*26]}", force=True)
            danmu_enter.click()
            time.sleep(1)
    else:
        danmu_input.fill(f"{message}", force=True)
        danmu_enter.click()
        time.sleep(1)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge")
    browser_interactive = p.chromium.launch_persistent_context(user_data_dir='./userdata',channel="msedge")
    page_monitor = browser.new_page()
    page_interactive = browser_interactive.pages[0]
    page_monitor.goto(url,wait_until="domcontentloaded")
    page_interactive.goto(url_live,wait_until="domcontentloaded")
    # initialize
    danmu_message = ""
    danmu_response = "启动!"
    time.sleep(5)
    chat_input = page_interactive.locator(".chat-input").last
    chat_enter = page_interactive.get_by_text("发送").last
    response(danmu_response, chat_input, chat_enter)
    page_interactive.route("**/*.flv**", lambda route: route.continue_(url='')) # abort flv
    
    str_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    file = open(f"./data/danmu{str_time}.txt", "w+")

    danmu_latest = page_monitor.locator(".danmaku-message").last
    content_latest = page_monitor.locator(".danmaku-content").last
    _ = 0
    while True:
        try:
            content_latest_text = content_latest.text_content()
            _ += 1
            if _ >= 360:
                _ = 0
                response("#切歌", chat_input, chat_enter, PreProcess=False) # 每半小时切歌防卡
                response("小猫咪正在努力工作呢~", chat_input, chat_enter)
                time.sleep(5)
                continue
        except:
            content_latest_text = ""
            danmu_response = "弹幕获取失败，重新连接"
            response(danmu_response, chat_input, chat_enter)
            print(f'Warning: 弹幕：{content_latest_text}|回复：{danmu_response}'.encode('GBK', 'ignore').decode('GBK'), file=file)
        if 'Bot：' in content_latest_text:
            time.sleep(5) # 无人发言时，每5秒检查一次
            continue
        danmu_latest_text = danmu_latest.text_content()
        if '秦秋枫1' in content_latest_text:
            continue
        elif '点歌' in content_latest_text or '切歌' in content_latest_text:
            if '#点歌 ' in content_latest_text:
                danmu_response = '小猫咪收到啦，正在点歌~'
            elif '#切歌' in content_latest_text:
                danmu_response = '小猫咪收到啦，正在切歌~'
            else:
                danmu_response = '请输入正确的指令，包括#'
            response(danmu_response, chat_input, chat_enter)
            print(f'弹幕：{content_latest_text}|回复：{danmu_response}'.encode('GBK', 'ignore').decode('GBK'), file=file)
            file.flush()
            continue
        elif '#' in content_latest_text and ('想玩雪风' or '清秋枫' in content_latest_text):
            danmu_response = '小猫咪收到啦，正在处理~'
            response(danmu_response, chat_input, chat_enter)
            print(f'弹幕：{content_latest_text}|回复：{danmu_response}'.encode('GBK', 'ignore').decode('GBK'), file=file)
            file.flush()
            continue
        elif danmu_latest_text == content_latest_text:
            if "赠送的" in content_latest_text:
                response(content_latest_text, chat_input, chat_enter)
                print(f'弹幕：{danmu_latest_text}|回复：{danmu_latest_text}'.encode('GBK', 'ignore').decode('GBK'), file=file)
            continue
        else:
            danmu_response = generate_response(danmu_latest_text)
            response(danmu_response, chat_input, chat_enter)
            print(f'弹幕：{danmu_latest_text}|回复：{danmu_response}'.encode('GBK', 'ignore').decode('GBK'), file=file)
        file.flush()
        time.sleep(20) # 有人发言时，冷却20秒
        