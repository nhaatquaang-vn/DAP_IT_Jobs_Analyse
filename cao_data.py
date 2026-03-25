from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
from bs4 import BeautifulSoup
import time
import pandas as pd

def setup_driver():
    chrome_options = Options()
    # Quan trọng: Thêm User-Agent để giả làm người dùng thật
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    # Tùy chọn: Chạy ẩn danh để tránh cache cũ
    chrome_options.add_argument("--incognito")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_itviec(job_keyword):
    driver = setup_driver()
    url = f"https://itviec.com/{job_keyword}"
    
    try:
        driver.get(url)
        time.sleep(5) # Đợi trang tải xong lần đầu

        # --- BƯỚC CUỘN TRANG (AUTO-SCROLL) ---
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(3): # Cuộn 3 lần để lấy thêm job (tùy chỉnh số lần)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3) # Đợi dữ liệu mới load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height: break
            last_height = new_height

        # --- PHÂN TÍCH HTML ---
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Tìm tất cả các thẻ chứa thông tin job (cần kiểm tra Class thực tế trên web)
        job_cards = soup.find_all('div', class_='job-card') 

        data = []
        for card in job_cards:
            title = card.find('h3').text.strip() if card.find('h3') else "N/A"
            company = card.find('div', class_='company-name').text.strip() if card.find('div', class_='company-name') else "N/A"
            # Lấy các thẻ kỹ năng (Tags)
            tags = [tag.text.strip() for tag in card.find_all('div', class_='tag')]
            
            data.append({
                'Title': title,
                'Company': company,
                'Skills': ", ".join(tags)
            })

        return pd.DataFrame(data)

    finally:
        driver.quit()

# Thực hiện cào thử cho vị trí 'python'
df_jobs = scrape_itviec("python")
print(f"Thu thập được {len(df_jobs)} công việc!")
print(df_jobs.head())