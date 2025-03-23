import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 크롬 드라이버 경로 (자신의 환경에 맞게 변경하세요)
# 예: '/usr/local/bin/chromedriver'
driver_path = r"C:\Users\MSI\Desktop\chromedriver-win64\chromedriver.exe"
service = ChromeService(executable_path=driver_path)
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # 헤드리스 모드 사용 시 주석 해제
driver = webdriver.Chrome(service=service, options=options)

# 구글 검색 URL
url = (
    "https://www.google.co.kr/maps/place/%EC%9A%A9%ED%99%94%EC%82%AC/data=!3m1!4b1!4m6!3m5!1s0x356527c59a6ca377:0x3bf406f8ef93d386!8m2!3d36.6416246!4d127.4820829!16s%2Fg%2F1tjgy6sl?hl=ko&entry=ttu&g_ep=EgoyMDI1MDIxMi4wIKXMDSoASAFQAw%3D%3D"
)
driver.get(url)

# 페이지 로딩을 위한 대기 설정
wait = WebDriverWait(driver, 10)

try:

    # 장소
    place_selector = "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div:nth-child(1) > h1"
    place_element = driver.find_element(By.CSS_SELECTOR, place_selector)

    # 주소
    address_selector = "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(9) > div:nth-child(3) > div.OyjIsf"
    address_element = driver.find_element(By.CSS_SELECTOR, address_selector)

 # 영업시간 버튼 클릭 (제공된 CSS selector 사용)
    hours_button_selector = "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(9) > div.OqCZI.fontBodyMedium.WVXvdc > div.OMl5r.hH0dDd.jBYmhd > div.MkV9 > div > span.puWIL.hKrmvd.google-symbols.OazX1c"
    hours_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, hours_button_selector)))
    hours_button.click()

    # 영업시간
    hours_selector = "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(9) > div.OqCZI.fontBodyMedium.WVXvdc > div.OMl5r.hH0dDd.jBYmhd > div.MkV9 > div > span.ZDu9vd"
    hours_element = driver.find_element(By.CSS_SELECTOR, hours_selector)

    # 전화번호
    phone_selector = "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(9) > div:nth-child(3) > button > div > div.rogA2c"
    phone_element = driver.find_element(By.CSS_SELECTOR, phone_selector)

    # 정보
    info_selector = "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.y0K5Df > button > div.WeS02d.fontBodyMedium > div > div"
    info_element = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, info_selector)))

except Exception as e:
    print("요소를 찾는 중 오류 발생:", e)
    driver.quit()
    exit()

# 각 요소의 텍스트 추출
place = place_element.text.strip()
# info = info_element.text.strip()
address = address_element.text.strip()
# hours = hours_element.text.strip()
phone = phone_element.text.strip()

driver.quit()

# CSV 파일에 데이터를 추가 (append mode)
csv_file = "google_search_data.csv"
# 파일이 없거나 비어있으면 헤더를 작성할 플래그 설정
write_header = not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0

with open(csv_file, mode="a", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    if write_header:
        writer.writerow(["장소", "정보", "주소", "영업시간", "전화번호"])
    writer.writerow([place,  address, phone])

print("CSV 파일에 데이터 추가 완료:", csv_file)
