from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# import os
# os.environ["JAVA_HOME"] = "C:\Program Files\Eclipse Adoptium\jdk-17.0.8.101-hotspot\bin"

# "C:\Program Files\Eclipse Adoptium\jdk-17.0.8.101-hotspot\bin\" <- Path

# "%JAVA_HOME%\bin\" <- Path <- 시스템 변수
# "C:\Program Files\Eclipse Adoptium\jdk-17.0.8.101-hotspot" <- JAVA_HOME <-시스템 변수

# KoNLPy의 Okt 토크나이저 초기화
okt = Okt()

# 사용자 정의 토크나이저 함수: 텍스트를 형태소 단위로 분리합니다.


def korean_tokenizer(text):
    # 명사만 추출
    nouns = okt.nouns(text)
    # 길이가 1인 명사는 제외 (의미있는 명사만 사용)
    nouns = [noun for noun in nouns if len(noun) > 1]
    return nouns


# 여행지 설명 데이터 예시
destinations = [
    "해변과 산이 어우러진 휴양지, 다양한 해양 스포츠와 맛집이 있음",
    "문화와 역사가 살아있는 도시, 박물관과 전통 시장이 유명함",
    "자연 경관이 뛰어난 산악 지역, 트래킹과 등산이 인기"
]

# 사용자 선호 예시 (예: 해양 스포츠, 휴양, 해변 관련 선호)
user_preference = "해양 스포츠 트래킹"

# TF-IDF 벡터화: tokenizer를 korean_tokenizer로 설정하고, token_pattern은 사용하지 않도록 None으로 지정
vectorizer = TfidfVectorizer(tokenizer=korean_tokenizer, token_pattern=None)
dest_vectors = vectorizer.fit_transform(destinations)
user_vector = vectorizer.transform([user_preference])

# 코사인 유사도 계산
similarities = cosine_similarity(user_vector, dest_vectors).flatten()

# 유사도에 따라 여행지를 정렬하여 추천
sorted_indices = np.argsort(similarities)[::-1]

print("추천 순위:")
for idx in sorted_indices:
    print(f"여행지: {destinations[idx]} - 유사도: {similarities[idx]:.2f}")
