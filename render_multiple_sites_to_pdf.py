# Script Name: render_multiple_sites_to_pdf.py

from selenium import webdriver
from setup_chromedriver import setup_chromedriver
from pdf_utils import get_pdf_base64_from_html, scroll_to_bottom
import base64
import time
import os
import hashlib
import argparse

def add_url_to_page(driver, url):
    print(f"Adding URL to page: {url}")
    page_title = driver.title
    script = f"""
    let infoDiv = document.createElement('div');
    infoDiv.style.position = 'fixed';
    infoDiv.style.bottom = '0';
    infoDiv.style.left = '0';
    infoDiv.style.width = '100%';
    infoDiv.style.textAlign = 'center';
    infoDiv.style.zIndex = '10000';
    infoDiv.style.fontSize = '12px';
    infoDiv.innerHTML = 'Page Title: {page_title}<br>This PDF file is originally from: <a href="{url}" target="_blank">{url}</a>';
    document.body.appendChild(infoDiv);
    """
    driver.execute_script(script)
    print(f"URL and page title added to page: {url}")

def save_base64_pdf_to_file(pdf_base64, output_pdf_path, force):
    output_tmp_path = output_pdf_path + '.tmp'
    
    # Handle existing files
    if os.path.exists(output_pdf_path) or os.path.exists(output_tmp_path):
        if force:
            print(f"Removing existing files: {output_pdf_path}, {output_tmp_path}")
            if os.path.exists(output_pdf_path):
                os.remove(output_pdf_path)
            if os.path.exists(output_tmp_path):
                os.remove(output_tmp_path)
        else:
            raise FileExistsError(f"File {output_pdf_path} or {output_tmp_path} already exists.")

    try:
        # Decode the base64 encoded PDF data and save it to a temporary file
        with open(output_tmp_path, 'wb') as pdf_file:
            pdf_file.write(base64.b64decode(pdf_base64))
        
        # Rename the temporary file to the final PDF file
        os.rename(output_tmp_path, output_pdf_path)
        
        print(f"PDF successfully generated: {output_pdf_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        if os.path.exists(output_tmp_path):
            os.remove(output_tmp_path)

def generate_pdf_filename(url):
    # Compute the SHA1 hash of the URL and convert it to a hexadecimal filename
    sha1_hash = hashlib.sha1(url.encode()).hexdigest()
    return f"{sha1_hash}.pdf"

def main(urls, force, initial_wait=3):
    driver = setup_chromedriver()
    
    try:
        for url in urls:
            print(f"Processing URL: {url}")
            output_pdf_path = generate_pdf_filename(url)
            driver.get(url)
            print(f"Page loaded: {url}")
            time.sleep(initial_wait)  # Wait for the page to fully load
            add_url_to_page(driver, url)  # Add URL and title to the page
            
            pdf_base64 = get_pdf_base64_from_html(driver, url, initial_wait)
            if pdf_base64:
                save_base64_pdf_to_file(pdf_base64, output_pdf_path, force)
    finally:
        driver.quit()
        print("ChromeDriver session ended.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert multiple web pages to PDFs.')
    parser.add_argument('urls', metavar='URL', type=str, nargs='+', help='URLs of the web pages to convert to PDF')
    parser.add_argument('--force', action='store_true', help='Overwrite existing files if they exist')

    args = parser.parse_args()
    main(args.urls, args.force)
