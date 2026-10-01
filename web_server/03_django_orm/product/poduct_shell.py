from product.models import Product, Category, Discount, Review  # 실습에 사용할 모델
from django.db.models import Sum, Avg, Count, Max, Min  # 집계 함수
from datetime import datetime, timedelta  # 날짜 계산
from django.utils import timezone         # Django 서버시간 (Project Settings.py TIME_ZONE 참조)

# 1:N Product-Review
#  - 특정 제품(Product)의 모든 리뷰 가져오기
reviews = Review.objects.filter(product_id=1)  # product id가 1인 리뷰 전제 조회
reviews
for review in reviews:
    print(review.id, review.product, review.user_id, review.rating, review.comment)

# id가 1인 상품 객체로 리뷰 조회
product = Product.objects.get(id=1)
Review.objects.filter(product=product)

product.reviews
product.reviews.all()  # 해당 상품의 전체 리뷰 조회

# 2. 특정 제품(Product)의 평균 평점과 리뷰 개수 가져오기
product = Product.objects.get(id=1)
# 집계함수로 해당 상품 리뷰의 평균 평점 계산
average_rating = product.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
review_count = product.reviews.count()
print(f'product id 1의 평균 평점 : {average_rating}, 리뷰 수 : {review_count}')

# 3. 평점이 높은 리뷰(4점 이상)만 가져오기
high_rating_reviews = product.reviews.filter(rating__gte=4)
for review in high_rating_reviews:
    print(review.id, review.product, review.user_id, review.rating, review.comment)

# 4. 모든 제품의 평균 평점과 리뷰 개수 가져오기
products_with_review_data = Product.objects.annotate(
    avg_rating = Avg('reviews__rating'),
    review_count = Count('reviews')
)
products_with_review_data

for product in products_with_review_data:
    avg_rating = f"{product.avg_rating:.2f}" if product.avg_rating else "0"
    print(f"Product: {product.name}, Average Rating: {avg_rating}, Reviews: {product.review_count}")

# 5. 특정 기간 동안 작성된 리뷰 가져오기
start_date = timezone.now() - timedelta(weeks=1)  # 검색시작시간 1주일전
end_date = timezone.now()  # 검색 종료시간 현재시간
reviews = Review.objects.filter(created_at__range=(start_date, end_date))  # 1주일 내 작성된 리뷰 조회
for review in reviews:
    print(review.id, review.product, review.user_id, review.rating, review.comment)

# 1:1 Product-Discount
# 1. 특정 제품의 할인 정보 가져오기
product_id = 3

try:
    discount = Discount.objects.get(product_id=product_id)
    print(f"Product: {discount.product.name}, Discount: {discount.discount_percentage}%, Start: {discount.start_date}, End: {discount.end_date}")
except Discount.DoesNotExist:
    print(f"Product ID {product_id}의 할인정보가 없습니다.")

# 2. 할인 중인 모든 제품 가져오기
current_date = timezone.now()
current_discounts = Discount.objects.filter(start_date__lte=current_date, end_date__gte=current_date)

for discount in current_discounts:
    print(f"Product: {discount.product.name}, Discount: {discount.discount_percentage}%, Ends on: {discount.end_date}")

# 3. 특정 할인율 이상인 제품 가져오기 (20%)
high_discounts = Discount.objects.filter(discount_percentage__gte=0.2)

for discount in high_discounts:
    print(f"Product: {discount.product.name}, Discount: {discount.discount_percentage}%, Ends on: {discount.end_date}")

# 4. 할인 정보와 함께 모든 제품 가져오기
#  - prefetch_related를 사용해 지연쿼리를 제한하고, 한번의 추가쿼리를 사용해서 데이터를 미리 가져옴 (N+1 문제 해결함)
#  - DB에서 데이터 가져올때 처음 1회 조회하고, 연관 데이터 가져올때 n번의 추가쿼리가 발생하는 문제
products = Product.objects.all()
products_with_discounts = Product.objects.prefetch_related('discount')

for product in products_with_discounts:
    if hasattr(product, 'discount'):
        print(f"Product: {product.name}, Discount: {product.discount.discount_percentage}%, Ends: {product.discount.end_date}")
    else:
        print(f"Product: {product.name}에는 할인 정보가 없습니다.")

# 5. 할인 기간이 지난 제품 가져오기
expired_discounts = Discount.objects.filter(end_date__lt=current_date)  # 종료일이 현재일 이전인 할인 조회

for discount in expired_discounts:
    print(f"Product: {discount.product.name}, Discount: {discount.discount_percentage}%, Ends on: {discount.end_date}")

# N:M Product-Category
# 1. 특정 제품이 속한 모든 카테고리 가져오기
product_id = 9
product = Product.objects.get(id=product_id)
categories = product.categories.all()  # 해당 제품에 연결된 모든 카테고리 조회

print(f"Product: {product.name}에 해당하는 카테고리는? ")
for category in categories:
    print(f"{category.name}")

# 2. 특정 카테고리에 속한 모든 제품 가져오기
category_name = "가전"
try:
    category = Category.objects.get(name = category_name)
    products = category.products.all()

    print(f"Category: {category.name}에 해당하는 제품은? ")
    for product in products:
        print(f"{product.name} (Price: {product.price}, Stock: {product.stock})")
except Category.DoesNotExist:
    print(f"Category {category_name}에 해당하는 제품이 없습니다.")

# 3. 카테고리가 없는 제품 가져오기
products_without_category = Product.objects.filter(categories__isnull=True)

print("카테고리가 없는 제품은?")
for product in products_without_category:
    print(f"{product.name} (Price: {product.price}, Stock: {product.stock})")

# 4. 특정 제품에 새 카테고리 추가하기
new_category_name = 'Seasonal'  # 새로운 카테고리명
new_category, created = Category.objects.get_or_create(name=new_category_name)  # 카테고리가 없으면 생성, 있으면 기존 객체 반환
product.categories.add(new_category)  # 현재 상품에 새로운 카테고리 연결

print(f"추가된 카테고리 : {new_category.name}, 해당 제품은? {product.name}")

# 5. 모든 카테고리와 각 카테고리의 제품 수 출력하기
categories_with_product_count = Category.objects.annotate(product_count=Count('products'))

for category in categories_with_product_count:
    print(f"Category: {category.name}, Number of Products: {category.product_count}")

# 6. 여러 카테고리에 속한 제품 가져오기
# 카테고리가 2개 이상인 상품 조회
multi_category_products = Product.objects.annotate(category_count = Count('categories')).filter(category_count__gt=1)
for product in multi_category_products:
    # 여러 카테고리가 속한 상품 정보 출력
    print(f"카테고리가 다수인 제품은? {product.name} (Categories: {product.categories.count()})")

### N + 1 이슈 대응 ###
# 1. select_related    : ForeignKey, OneToOne처럼 단일 객체 관계를 JOIN으로 함께 조회할 때 사용
# 2. prefetch_related  : ManyToMany, 역참조처럼 여러 객체 관계를 별도 쿼리로 미리 조회할 때 사용

# N + 1 이슈 발생 예시
products = Product.objects.all()  # 상품 목록만 먼저 조회
for product in products:
    if hasattr(product, 'discount'):
        print(f"Product: {product.name}, Discount: {product.discount.discount_percentage}%, Ends: {product.discount.end_date}")  # 반복문마다 discount 추가 조회 발생
    else:
        print(f"Product: {product.name}, No discount available")  # 할인 정보가 없으면 안내 문구 출력

# N + 1 이슈 해결 (select_related) 예시
products_with_discounts = Product.objects.select_related('discount')  # discount를 JOIN으로 함께 조회
for product in products_with_discounts:
    if hasattr(product, 'discount'):
        print(f"Product: {product.name}, Discount: {product.discount.discount_percentage}%, Ends: {product.discount.end_date}")  # 추가 쿼리 없이 할인 정보 사용
    else:
        print(f"Product: {product.name}, No discount available")  # 할인 정보가 없으면 안내 문구 출력

# N + 1 이슈 예시
products = Product.objects.all()  # 상품 목록만 먼저 조회
for product in products:
  print(product.name, product.reviews.all())  # 반복문마다 reviews 조회 쿼리 추가 발생

# N + 1 이슈 해결 (prefetch_related) 예시
products = Product.objects.prefetch_related('reviews')  # reviews를 별도 쿼리로 미리 조회
for product in products:
  print(product.name, product.reviews.all())  # 미리 조회한 리뷰 데이터 사용

# 집계처리
# 1. aggregate : 전체 조회 결과를 하나로 집계해서 딕셔너리 형태로 반환
Product.objects.aggregate(total_count=Count('id'))   # 전체 상품 수 집계
Product.objects.aggregate(total_price=Sum('price'))  # 전체 상품 가격 합계
Product.objects.aggregate(avg_price=Avg('price'))    # 전체 상품 평균 가격 집계
Product.objects.aggregate(max_price=Max('price'))    # 전체 상품 최고 가격
Product.objects.aggregate(min_price=Min('price'))    # 전체 상품 최저 가격

# 2. filter + aggregate : 조건에 맞는 데이터만 먼저 걸러서 집계
Product.objects.filter(categories__name = '가전')  # 가전 카테고리에 해당하는 상품
Product.objects.filter(categories__name = '가전').aggregate(avg_price = Avg('price'))  # 가전 카테고리 상품의 평균 가격

# 3. 연관관계 annotate   : 각 객체별 집계 결과를 계산해서 객체마다 필드처럼 추가
# 외래 키 관계를 따라가며 데이터를 집계
# 상품별 리뷰 개수 (select product.name, count(*) from review group by product_id)
# .values('product') : 어떤 컬럼 기준으로 결과를 나눌지 정함 + .annotate(Count(...)) → 그 기준별 집계 수행
Review.objects.values('product').annotate(review_counts=Count('id'))  # 리뷰 테이블 기준으로 상품별 리뷰 수 집계
# 역방향 조회
Product.objects.values('id').annotate(review_counts=Count('reviews'))  # 상품 테이블 기준으로 연결된 리뷰 수 집계
# 이때 values는 생략할 수 있고, annotate는 집계처리된 필드만 추가된다.
products = Product.objects.annotate(review_counts=Count('reviews'))  # 상품 객체에 review_counts 필드 추가
products_with_review_counts = [(product.name, product.review_counts) for product in products]  # 상품명과 리뷰 수 리스트 정리
print(products_with_review_counts)

# 카테고리별 상품 개수
Category.objects.values('name').annotate(product_count = Count('products'))  # 카테고리별 상품 수 집계
Product.objects.values('categories').annotate(product_count=Count('id'))     # 카테고리 기준으로 상품 수 집계
# values 없이, annotate만 사용해도 연관관계를 따라가면서 집계처리를 할 수 있다.
# 각 카테고리에 상품 수, 평균 가격 추가
categories = Category.objects.annotate(product_count=Count('products'), avg_product_price=Avg('products__price'))
categories_with_info = [(category.name, category.product_count, category.avg_product_price) for category in categories]
print(categories_with_info)  # 카테고리별 상품 수, 평균 가격 출력