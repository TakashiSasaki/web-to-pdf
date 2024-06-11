# pdf_utils.py

import time

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
