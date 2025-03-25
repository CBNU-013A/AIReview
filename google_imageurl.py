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
    "https://www.google.co.kr/maps/place/%EC%9A%A9%ED%99%94%EC%82%AC/data=!3m1!4b1!4m6!3m5!1s0x356527c59a6ca377:0x3bf406f8ef93d386!8m2!3d36.6416246!4d127.4820829!16s%2Fg%2F1tjgy6sl?hl=ko&entry=ttu&g_ep=EgoyMDI1MDMxOS4yIKXMDSoASAFQAw%3D%3D"
)
driver.get(url)

# 페이지 로딩을 위한 대기 설정
wait = WebDriverWait(driver, 10)

try:
    # 이미지 요소 찾기
    image_css_selector = "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.ZKCDEc > div.RZ66Rb.FgCUCc > button > img"
    image_element = driver.find_element(By.CSS_SELECTOR, image_css_selector)
    image_url = image_element.get_attribute("src")
    print("이미지 URL:", image_url)

    # 장소 이름 요소 찾기
    place_name_css_selector = "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div:nth-child(1) > h1"
    place_name_element = driver.find_element(
        By.CSS_SELECTOR, place_name_css_selector)
    place_name = place_name_element.text.strip()
    print("장소 이름:", place_name)

    # CSV 파일에 연속 추가 저장 (헤더는 처음 생성 시에만 작성)
    file_exists = False
    try:
        with open("image_data.csv", "r", encoding="utf-8") as file:
            file_exists = True
    except FileNotFoundError:
        pass

    with open("image_data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Place Name", "Image URL"])
        writer.writerow([place_name, image_url])
        print("CSV 파일에 추가 저장 완료: image_data.csv")
except Exception as e:
    print("오류 발생:", e)

# 브라우저 종료
driver.quit()


print("CSV 파일에 데이터 추가 완료:")
