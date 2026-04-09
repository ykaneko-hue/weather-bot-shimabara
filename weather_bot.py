import time
import requests
import json
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# --- サーバー用設定（画面なしで動かすための必須設定） ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def send_weather():
    # 自動操作用のブラウザを起動（サーバー設定を適用）
    browser = webdriver.Chrome(options=chrome_options)

    # 指定webページを開く
    browser.get("https://tenki.jp/forecast/9/45/8410/42203/")
    time.sleep(3) # 読み込み待ち

    # --- 日本時間の日付を取得 ---
    # サーバーの時差対策として +9時間 しています
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    weeks = ["月", "火", "水", "木", "金", "土", "日"]
    week_jp = weeks[now.weekday()]
    today_str = now.strftime(f"%m月%d日({week_jp})")

    # --- Webページより抜き出し（あなたのXPathをそのまま使用） ---
    try:
        weather_text = browser.find_element(By.XPATH, "/html/body/div[3]/section/div[2]/div[4]/section[1]/div[2]/div[1]/p").text
        high_val = browser.find_element(By.XPATH,"/html/body/div[3]/section/div[2]/div[4]/section[1]/div[2]/div[2]/dl/dd[1]/span[1]").text
        low_val = browser.find_element(By.XPATH,"/html/body/div[3]/section/div[2]/div[4]/section[1]/div[2]/div[2]/dl/dd[3]/span[1]").text

        # ---- chatに送る文面（こだわりのレイアウト） ------
        message = f"""【島原市の天気と気温】
日付：{today_str}
天気：{weather_text}
気温：
最高 {high_val}℃
最低 {low_val}℃"""

        # Google Chat 送信
        webhook_url = "https://chat.googleapis.com/v1/spaces/AAQAf_-uwLs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=KrziqM2lPWiOYAioPMvC7bmN7yKT0lOKQc2kGfeXvCg"
        data = {"text": message}
        requests.post(webhook_url, data=json.dumps(data))
        
        print(f"成功：{today_str} の情報を送信しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

    finally:
        browser.quit()

if __name__ == "__main__":
    send_weather()
