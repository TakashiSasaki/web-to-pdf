# Script name: add_url_to_page.py

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
