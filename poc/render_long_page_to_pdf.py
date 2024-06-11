# Script Name: render_long_page_to_pdf_with_scroll.py

from selenium import webdriver
from setup_chromedriver import setup_chromedriver
import base64
import time

def save_pdf_from_base64(pdf_base64, output_pdf_path):
    with open(output_pdf_path, 'wb') as pdf_file:
        pdf_file.write(base64.b64decode(pdf_base64))

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # ページの最下部までスクロール
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # スクロール後に新しいコンテンツがロードされるのを待つ
        time.sleep(2)
        
        # 新しい高さを取得
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        
        last_height = new_height

def render_html_to_long_pdf(url, output_pdf_path, initial_wait=3):
    driver = setup_chromedriver()

    try:
        # URLを開く
        driver.get(url)
        
        # ページの完全な読み込みを待つ
        driver.execute_script("return document.readyState") == "complete"
        
        # スクロールを開始する前に待つ
        print(f"Waiting for {initial_wait} seconds before starting to scroll...")
        time.sleep(initial_wait)
        
        # ページを下端までスクロールしてコンテンツをロード
        scroll_to_bottom(driver)
        
        # ページの全体の高さと幅を取得
        total_height = driver.execute_script("return document.body.scrollHeight")
        viewport_width = driver.execute_script("return document.documentElement.clientWidth")
        
        # ページ全体をPDFとして保存
        result = driver.execute_cdp_cmd("Page.printToPDF", {
            "paperWidth": viewport_width / 96,  # 96 DPI でインチに変換
            "paperHeight": total_height / 96,   # 96 DPI でインチに変換
            "printBackground": True,
            "scale": 1
        })
        
        # base64でエンコードされたPDFデータをデコードして保存
        pdf_base64 = result['data']
        save_pdf_from_base64(pdf_base64, output_pdf_path)
        
        print(f"PDFが正常に生成されました: {output_pdf_path}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        driver.quit()

def main():
    url = 'https://www.yahoo.co.jp'  # PDFに変換するURL
    output_pdf_path = 'yahoo_long.pdf'   # 出力PDFファイル
    initial_wait = 3  # スクロールを開始する前の待機時間（秒）
    render_html_to_long_pdf(url, output_pdf_path, initial_wait)

if __name__ == "__main__":
    main()
