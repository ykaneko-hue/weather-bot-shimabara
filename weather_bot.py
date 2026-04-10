import time
import requests
import json
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# --- サーバー用設定（画面なしで動かす） ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def send_weather():
    # ブラウザ起動
    browser = webdriver.Chrome(options=chrome_options)
    
    # 1. 日本時間の日付を計算（GitHubサーバーは標準時なので+9時間する）
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_jp = now_utc + datetime.timedelta(hours=9)
    weeks = ["月", "火", "水", "木", "金", "土", "日"]
    week_jp = weeks[now_jp.weekday()]
    today_str = now_jp.strftime(f"%m月%d日({week_jp})")

    # 2. 島原市の天気
    url = "https://tenki.jp/forecast/9/45/8410/42203/"
    webhook_url = "https://chat.googleapis.com/v1/spaces/AAQAf_-uwLs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=KrziqM2lPWiOYAioPMvC7bmN7yKT0lOKQc2kGfeXvCg"
    
    try:
        browser.get(url)
        time.sleep(3)

        # 抜き出し（属性指定のXPath）
        weather_text = browser.find_element(By.XPATH, "//*[@class='weather-telop']").text
        high_val = browser.find_element(By.XPATH, "//*[contains(@class, 'high-temp')]//span[@class='value']").text
        low_val = browser.find_element(By.XPATH, "//*[contains(@class, 'low-temp')]//span[@class='value']").text

        message = f"""【島原市の天気と気温】
日付：{today_str}
天気：{weather_text}
気温：
最高 {high_val}℃
最低 {low_val}℃"""

        # 送信
        requests.post(webhook_url, data=json.dumps({"text": message}))
        print(f"成功: {today_str} の情報を送信しました。")

    except Exception as e:
        print(f"エラー発生: {e}")
    finally:
        browser.quit()

if __name__ == "__main__":
    send_weather()
