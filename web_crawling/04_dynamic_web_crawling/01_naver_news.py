from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

service = webdriver.chrome.service.Service("chromedriver.exe")
driver = webdriver.Chrome(service = service)

driver.get("https://naver.com")
time.sleep(1)
search_box = driver.find_element(By.ID, 'query')

search_box.send_keys("이번주 날씨")
search_box.send_keys(Keys.RETURN)
time.sleep(1)
news_tab = driver.find_element(By.CSS_SELECTOR, "a.tab[href*='where=news']")    # 뉴스버튼 찾기
news_tab.click()
time.sleep(1)
for _ in range(5):
    body = driver.find_element(By.TAG_NAME,"body")
    body.send_keys(Keys.END)
    time.sleep(1)

news_contents = driver.find_elements(By.CSS_SELECTOR,"span.sds-comps-text-type-headline1")

for news_content in news_contents:
    href_tag = news_content.find_element(By.XPATH, "..")   # XPATH를 이용한 태그 탐색 ( a 태그)

    title = news_content.text    #span태그 제목
    href = href_tag.get_attribute('href')  # a 태그 : 링크 경로

    print(title,"|",href)

driver.quit()        # 드라이버 종료(브라우저 종료)