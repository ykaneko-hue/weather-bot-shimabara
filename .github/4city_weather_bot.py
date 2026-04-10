import time
import requests
import json
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# --- サーバー用設定（画面なし） ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def send_weather():
    # ブラウザ起動
    browser = webdriver.Chrome(options=chrome_options)
    
    # 1. 日本時間の日付を計算（標準時+9時間）
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_jp = now_utc + datetime.timedelta(hours=9)
    weeks = ["月", "火", "水", "木", "金", "土", "日"]
    week_jp = weeks[now_jp.weekday()]
    today_str = now_jp.strftime(f"%m月%d日({week_jp})")

    # 2. 都市リスト（課題②）
    city_list = [
        {"name": "弘前市", "url": "https://tenki.jp/forecast/2/5/3110/2202/"},
        {"name": "名古屋市", "url": "https://tenki.jp/forecast/5/26/5110/23100/"},
        {"name": "金沢市", "url": "https://tenki.jp/forecast/4/20/5610/17201/"},
        {"name": "島原市", "url": "https://tenki.jp/forecast/9/45/8410/42203/"}
    ]

    webhook_url = "https://chat.googleapis.com/v1/spaces/AAQAf_-uwLs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=KrziqM2lPWiOYAioPMvC7bmN7yKT0lOKQc2kGfeXvCg"
    
    try:
        for city in city_list:
            browser.get(city["url"])
            time.sleep(3)

            # 抜き出し（Jupyterで成功した最強のXPath）
            weather_text = browser.find_element(By.XPATH, "//*[@class='weather-telop']").text
            high_val = browser.find_element(By.XPATH, "//*[contains(@class, 'high-temp')]//span[@class='value']").text
            low_val = browser.find_element(By.XPATH, "//*[contains(@class, 'low-temp')]//span[@class='value']").text

            message = f"""【{city['name']}の天気と気温】
日付：{today_str}
天気：{weather_text}
気温：
最高 {high_val}℃
最低 {low_val}℃"""

            # 送信
            requests.post(webhook_url, data=json.dumps({"text": message}))
            print(f"{city['name']}の送信完了")
            time.sleep(1) # 連続送信によるエラー防止

    except Exception as e:
        print(f"エラー発生: {e}")
    finally:
        browser.quit()

if __name__ == "__main__":
    send_weather()
