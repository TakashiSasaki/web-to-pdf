# Script Name: render_sample_to_pdf.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from setup_chromedriver import setup_chromedriver
import base64
import os

def save_pdf_from_base64(pdf_base64, output_pdf_path):
    with open(output_pdf_path, 'wb') as pdf_file:
        pdf_file.write(base64.b64decode(pdf_base64))

def wait_for_page_load(driver, timeout=30):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

def render_html_to_pdf(url, output_pdf_path):
    driver = setup_chromedriver()

    try:
        # URLを開く
        driver.get(url)
        
        # ページの完全な読み込みを待つ
        wait_for_page_load(driver)
        
        # Chrome DevToolsプロトコルを使用してPDFを生成
        result = driver.execute_cdp_cmd("Page.printToPDF", {
            "format": "A4",
            "printBackground": True
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
    urls_and_paths = [
        (f'file:///{os.path.abspath("sample.html")}', 'sample.pdf')
    ]
    
    for url, path in urls_and_paths:
        render_html_to_pdf(url, path)

if __name__ == "__main__":
    main()
