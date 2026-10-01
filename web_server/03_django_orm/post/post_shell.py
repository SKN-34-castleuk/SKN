# python manage.py shell
# import os; os.system('cls') 화면 정리 (Windows)
from post.models import Post  # Post 모델 import

Post  # Post 모델 클래스 확인
Post.objects  # Post 모델의 매니저 객체 확인
Post.objects.all()  # 전체 Post 조회
queryset = Post.objects.all()  # 전체 조회 결과를 queryset 변수에 저장
str(queryset.query)  # 실행될 SQL 쿼리 문자열 확인

### post 생성 ###
post = Post.objects.create(title='Hello world', content='🍭🍭🍭')  # 객체 생성과 저장을 한 번에 수행
post  # 생성된 객체 확인
post.id  # 생성된 객체의 기본키 확인
post.title  # 제목 필드 값 확인
post.content  # 내용 필드 값 확인
post.created_at  # 생성 시각 확인
post.updated_at  # 수정 시각 확인

post2 = Post(title='배고프다', content='춥고 배고프다ㅠ 🤖🤖')  # 저장 전 Post 객체 생성
post2.save()  # DB에 저장
post2.id  # 저장 후 기본키 확인
post2.title  # 제목 필드 값 확인
post2.content  # 내용 필드 값 확인
post2.created_at  # 생성 시각 확인
post2.updated_at  # 수정 시각 확인

### post 조회 ###
queryset = Post.objects.all()  # 전체 Post 다시 조회
queryset  # 조회 결과 확인

# 쿼리 확인
# 1.queryset.query
queryset.query  # Query 객체 확인
str(queryset.query)  # SQL 문자열로 변환하여 확인

import sqlparse  # SQL 포맷팅 라이브러리 import
print(sqlparse.format(str(queryset.query), reindent=True))  # SQL을 보기 좋게 정렬해서 출력

# 2.connection.queries
from django.db import connection  # 실행된 SQL 목록 확인용 import

connection.queries  # 실행된 모든 쿼리 출력
connection.queries[-1]  # 가장 마지막에 실행된 쿼리 확인

# where 조건검색
# 1. filter   : 조건에 맞는 여러 개의 데이터를 QuerySet 형태로 조회
# 2. get      : 조건에 맞는 단일 데이터를 조회 (0개 또는 여러 개면 오류 발생)
# 3. exclude  : 지정한 조건에 해당하는 데이터를 제외하고 조회

# 특정 조건에 맞는 데이터 필터링
# filer/get 차이
Post.objects.filter(title='배고프다')  # 조건에 맞는 여러 행을 QuerySet으로 반환
Post.objects.get(title='배고프다')  # 조건에 맞는 한 행만 반환, 없거나 여러 개면 오류 발생

# 문자열 필드
Post.objects.filter(title='Hello world')  # title이 정확히 일치하는 데이터 조회
Post.objects.filter(title__startswith='Hello')  # title이 Hello로 시작하는 데이터 조회
Post.objects.filter(title__endswith='!')  # title이 !로 끝나는 데이터 조회
Post.objects.filter(content__contains='🍭')  # content에 🍭가 포함된 데이터 조회
Post.objects.filter(title__icontains='happy')  # 대소문자 구분 없이 happy 포함 데이터 조회
Post.objects.filter(content__isnull=True)  # content가 NULL인 데이터 조회

# 날짜필드 (less then, great than, equal)
Post.objects.filter(created_at__lte='2027-01-01')  # 2027-01-01 이하 날짜 조회
Post.objects.filter(created_at__gt='2026-01-01')  # 2026-01-01 초과 날짜 조회
Post.objects.filter(created_at__gt='2026-03-13 06:00:00')  # 특정 일시 이후 데이터 조회
Post.objects.filter(created_at__year=2026)  # 생성연도가 2026년인 데이터 조회

# 여러 조건 AND
Post.objects.filter(title='Hello world', created_at__year=2026)  # 조건을 AND로 함께 적용
Post.objects.filter(title='Hello world').filter(created_at__year=2026)  # filter 체이닝으로 AND 적용

# 여러 조건 OR (Q 객체를 | 연산자로 연결)
from django.db.models import Q  # 복합 조건식을 위한 Q 객체 import
Post.objects.filter(Q(title__contains='🍭') | Q(content__contains='🍭'))  # OR 조건 검색

# NOT 비교
# - exclude       : 지정한 조건에 해당하는 데이터를 제외하고 조회
# - filter(~Q())  : Q객체에 NOT 연산자를 적용해 조건을 반대로 하여 조회

# 같은 행의 다른 컬럼 비교시 F객체 사용
from django.db.models import F  # 같은 행의 다른 필드 값을 비교할 때 사용하는 F 객체 import
Post.objects.exclude(created_at=F('updated_at'))  # created_at과 updated_at이 같은 행 제외
Post.objects.filter(~Q(created_at=F('updated_at')))  # created_at과 updated_at이 같지 않은 행 조회

# 정렬
Post.objects.all().order_by('created_at')  # 생성일 오름차순 정렬
Post.objects.all().order_by('-created_at')  # 생성일 내림차순 정렬
Post.objects.all().order_by('title', 'id')  # title 우선, 같은 값이면 id 기준 정렬

# 한 행 조회 get
# 주로 pk컬럼 조회에 사용. 0행 또는 n행 반환시 오류
Post.objects.get(id=1)  # id가 1인 객체 1개 조회
Post.objects.get(id=100)  # 없는 id 조회 시 오류 발생
Post.objects.filter(id=1)  # id가 1인 객체를 QuerySet 형태로 조회

# 기존 Post객체와 새롭게 질의후 반환받은 객체와 내용(pk)비교
post = Post.objects.get(id=6)  # id가 6인 객체 조회
# `__eq__` 내부적으로 호출, 재정의 하지않은 `__eq__`는 id함수값을 비교한다.
# Model클라스는 `__eq__` pk비교하도록 오버라이드함.
post == Post.objects.get(id=1)  # pk 기준 동등 비교
Post.objects.get(id=2) is post  # 같은 메모리 객체인지 비교
id(Post.objects.get(id=1)), id(post)  # 각 객체의 메모리 주소값 확인

# values
# - Model.objects.values(*fields)
# - values 메소드는 Django ORM에서 특정 필드만 선택해 쿼리셋을 생성할 때 사용한다.
# - 이를 활용하면 모델 객체 대신 필드 이름과 값으로 구성된 딕셔너리 형태의 쿼리셋을 반환한다.
Post.objects.values('title', 'content')  # title, content만 dict 형태로 조회
Post.objects.values()  # 모든 필드를 key-value 형태로 조회
Post.objects.values('title', 'content').distinct()  # 중복 제거 후 조회

# values + annotate -> group by
from django.db.models.functions import ExtractYear  # 날짜에서 연도 추출 함수 import
from django.db.models import Count  # 개수 집계 함수 import
# 연도별 게시글 수 집계 (created_at에서 연도만 뽑고, 그 연도별로 게시글 개수를 센다)
Post.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count_by_year=Count('year'))


#### post 수정 ####
post = Post.objects.get(id=1)  # 수정할 객체 조회
post.title  # 수정 전 제목 확인
post.title += '123'  # 제목 뒤에 문자열 추가
post.title  # 수정된 제목 확인
post.save()  # 변경사항 저장


#### post 삭제 ####
post = Post.objects.create(title='Hello world123', content='🍭🍭🍭')  # 삭제 테스트용 객체 생성
post.delete()  # 객체 삭제