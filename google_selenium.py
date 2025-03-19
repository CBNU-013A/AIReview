from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Chrome WebDriver 설정
service = Service(r"C:\Users\MSI\Desktop\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# 구글 리뷰 페이지 열기
driver.get("URL")  # 크롤링할 URL

# 페이지 로딩 대기
time.sleep(3)

# 리뷰 버튼을 찾고 클릭하기
try:
    review_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(3) > div > div > button:nth-child(2) > div.LRkQ2 > div.Gpq6kf.fontTitleSmall"))
    )
    review_button.click()
    print("리뷰 버튼을 클릭했습니다.")
except Exception as e:
    print(f"오류 발생: {e}")

# 리뷰가 로딩될 때까지 대기
time.sleep(3)

# 리뷰가 길다면 "자세히 보기" 버튼 클릭
try:
    more_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#ChZDSUhNMG9nS0VJQ0FnSURQaUtpWkNBEAE > span:nth-child(2) > button"))
    )
    more_button.click()
    time.sleep(1)  # '자세히 보기' 클릭 후 잠시 대기
    print("자세히 보기를 클릭하여 리뷰 전체를 봅니다.")
except Exception as e:
    print(f"자세히 보기 버튼이 없습니다: {e}")

# 리뷰 크롤링 시작
reviews = []

# 페이지 끝까지 스크롤을 내려서 리뷰를 수집
while True:
    # 현재 페이지의 리뷰를 추출
    review_elements = driver.find_elements(
        By.CSS_SELECTOR, "span.wiI7pd")  # 모든 리뷰 찾기
    new_reviews = []

    for review_element in review_elements:
        review_text = review_element.text.strip() if review_element.text else ""
        # 줄바꿈 제거 (한 줄로 표현)
        review_text = review_text.replace("\n", " ")
        if review_text and review_text not in reviews:  # 중복된 리뷰를 방지
            new_reviews.append(review_text)

    if new_reviews:
        reviews.extend(new_reviews)
    else:
        print("새로운 리뷰가 더 이상 없습니다. 크롤링 종료.")
        break

    # 지정된 div 클래스만 스크롤
    try:
        review_section = driver.find_element(
            By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight", review_section)
        time.sleep(2)
    except Exception as e:
        print("리뷰 영역을 찾을 수 없습니다:", e)
        break

# 크롤링된 리뷰 출력
print(f"크롤링된 총 리뷰 수: {len(reviews)}")

# CSV 파일로 저장 (각 리뷰를 큰따옴표로 감싸고 한 줄로 저장)
with open("장소소.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerow(["Review"])  # 헤더 작성
    for review in reviews:
        writer.writerow([review])

print("리뷰가 '장소소.csv' 파일에 저장되었습니다.")

# 크롬 드라이버 종료
driver.quit()
