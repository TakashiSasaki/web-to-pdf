# Script Name: render_multiple_sites_to_pdf.py

from selenium import webdriver
from setup_chromedriver import setup_chromedriver
from pdf_utils import get_pdf_base64_from_html, scroll_to_bottom
import base64
import time
import os
import hashlib

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
