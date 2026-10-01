from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)         # 최대 100자 상품명
    description = models.TextField(blank=True)      # 상품 설명 (폼 입력을 비워둘 수 있음)
    price = models.PositiveIntegerField()           # 0 이상 상품 가격
    stock = models.PositiveIntegerField()           # 0 이상 재고
    available = models.BooleanField(default=True)   # 판매 가능 여부
    created_at = models.DateTimeField(auto_now_add=True)    # 최초 생성 시간 자동 저장 필드
    updated_at = models.DateTimeField(auto_now=True)        # 수정시마다 시간 자동 저장 필드

    # 객체를 출력시 제목문자열 출
    def __str__(self):
        return self.name

# Product와 Discount를 1:1로 연결해서 사용하는 할인 정보 모델
class Discount(models.Model):
    # 해당 Product 데이터 삭제시 자동 삭제되는 할인정보 필
    product = models.OneToOneField(Product, on_delete=models.CASCADE,related_name='discount')
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2,help_text='Discount precentage: 예) 10% => 0.1'
    )   # 할인율 저장 필드 (소수점 2자리, 최대 5자리)
    start_date = models.DateTimeField() # 할인 시작시간
    end_date = models.DateTimeField()   # 할인 종료시간

    # 객체를 출력시 할인율과 상품명 문자열 출력
    def __str__(self):
        return f"{self.discount_percentage}% off for {self.product.name}"

# Product와 Review 1:N로 연결하는 리뷰 모델
# Product : Review 참조(related_name값을 이용해서 접근)
class Review(models.Model):
    # 해당 Product 데이터 삭제시 자동 삭제되는 리뷰 필드
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name='reviews')
    user_id = models.PositiveIntegerField(blank=True, null=True)    # 사용자 id : 폼 공란, db상에 null 허용
    rating = models.PositiveIntegerField(default=1, help_text='평점은 1~5') # 평점필드
    comment = models.TextField(blank=True)  # 폼 공란 허용되는 리뷰 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 리뷰 작성 시간

    # 객체를 출력시 사용자 정보와 제품명 문자열 출력
    def __str__(self):
        return f"{self.user_id}가 {self.product.name}에 남긴 리"

# Product와 Category를 N:M으로 연결하는 카테고리 모델
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # 여러 상품과 여러 카테고리를 연결하는 필드
    products = models.ManyToManyField(Product,related_name='categories')

     # 객체를 출력시 상품명 문자열 출력
    def __str__(self):
        return self.name    