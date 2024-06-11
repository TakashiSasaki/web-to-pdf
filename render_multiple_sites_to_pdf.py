# Script Name: render_multiple_sites_to_pdf.py

from selenium import webdriver
from setup_chromedriver import setup_chromedriver
import base64
import time
import os
import hashlib

A4_HEIGHT_INCH = 11.69  # A4の縦の長さ（インチ）

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

def get_pdf_base64_from_html(driver, url, initial_wait=3):
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

        # 縦の長さがA4の縦の長さより短い場合にはA4の縦の長さを使用
        total_height_inch = max(total_height / 96, A4_HEIGHT_INCH)
        
        # ページ全体をPDFとして保存
        result = driver.execute_cdp_cmd("Page.printToPDF", {
            "paperWidth": viewport_width / 96,  # 96 DPI でインチに変換
            "paperHeight": total_height_inch,   # 96 DPI でインチに変換
            "printBackground": True,
            "scale": 1
        })
        
        return result['data']
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

def save_base64_pdf_to_file(pdf_base64, output_pdf_path):
    output_tmp_path = output_pdf_path + '.tmp'
    try:
        # base64でエンコードされたPDFデータをデコードして一時ファイルに保存
        with open(output_tmp_path, 'wb') as pdf_file:
            pdf_file.write(base64.b64decode(pdf_base64))
        
        # 一時ファイルを最終的なPDFファイルにリネーム
        os.rename(output_tmp_path, output_pdf_path)
        
        print(f"PDFが正常に生成されました: {output_pdf_path}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        if os.path.exists(output_tmp_path):
            os.remove(output_tmp_path)

def generate_pdf_filename(url):
    # URLのSHA1ハッシュを計算し、16進数のファイル名に変換
    sha1_hash = hashlib.sha1(url.encode()).hexdigest()
    return f"{sha1_hash}.pdf"

def main():
    urls = [
        'https://www.yahoo.co.jp',
        'https://www.example.com',
        'https://www.example.net',
        'https://www.example.org',
    ]
    
    driver = setup_chromedriver()
    
    try:
        initial_wait = 3  # スクロールを開始する前の待機時間（秒）
        for url in urls:
            output_pdf_path = generate_pdf_filename(url)
            pdf_base64 = get_pdf_base64_from_html(driver, url, initial_wait)
            if pdf_base64:
                save_base64_pdf_to_file(pdf_base64, output_pdf_path)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
