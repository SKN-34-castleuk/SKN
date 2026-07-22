# 흡연 유무와 BMI 수치별 진료비 예측

건강보험 가입자의 인적 정보(나이, 성별, BMI, 자녀 수, 흡연 여부)를 바탕으로
**연간 진료비(charges)를 예측하는 회귀 모델** 프로젝트입니다.

---

## 📊 데이터 출처

- [Kaggle: Medical Cost Personal Datasets](https://www.kaggle.com/datasets/mirichoi0218/insurance/data)
- 총 1,338행, 결측치 없음
- 컬럼: `age`, `sex`, `bmi`, `children`, `smoker`, `region`, `charges`
- `charges`는 누적값이 아니라 **가입자 1인당 해당 연도의 진료비 스냅샷**입니다.

## 목차

1. 데이터 읽기
2. EDA 및 데이터 정제
3. 데이터 시각화
4. 머신러닝 모델 학습을 위한 전처리
5. 모델 학습 및 평가
6. 고도화 (파생변수, 교차검증, 하이퍼파라미터 튜닝)

---

## 🔍 EDA 주요 발견

| 발견 | 내용 |
|---|---|
| 상관관계 | `smoker`가 `charges`와 가장 강한 상관관계 (r ≈ 0.79) |
| 흡연자 비율 | 비흡연자 1,064명(79.5%) vs 흡연자 274명(20.5%) — 특성 불균형 존재 |
| 흡연자 vs 비흡연자 평균 진료비 | 비흡연자 $8,434 vs 흡연자 $32,050 (약 4배 차이) |
| 이상치 | `charges` 상위 이상치(IQR 기준 139건)의 97.8%가 흡연자 → 노이즈가 아닌 **실제 하위 그룹**으로 판단, 제거하지 않고 파생변수로 반영 |

## 🧪 데이터 전처리 및 파생변수

```python
df_corr['sex'] = df_corr['sex'].map({'male': 1, 'female': 0})
df_corr['smoker'] = df_corr['smoker'].map({'yes': 1, 'no': 0})
df_corr = df_corr.drop('region', axis=1)   # 지역 변수 제거

X['smoker_bmi']   = X['smoker'] * X['bmi']            # 흡연 × BMI 상호작용
X['smoker_age']   = X['smoker'] * X['age']             # 흡연 × 나이 상호작용
X['bmi_obese']    = (X['bmi'] >= 30).astype(int)        # 비만 여부(BMI ≥ 30)
X['smoker_obese'] = X['smoker'] * X['bmi_obese']        # 흡연 × 비만 상호작용
```

- **MinMaxScaler**: `age`, `bmi`만 0~1로 스케일링 (train에 fit, test는 transform만)
- **train/test 분할**: `test_size=0.2`, `random_state=42`, **`stratify=smoker`** (흡연자 비율을 train/test에 동일하게 유지)
  - 전체 1,338 → 학습 1,070 / 테스트 268

## 📐 평가 지표

`charges`는 연속값이므로 **회귀 지표**를 사용합니다 (분류의 혼동행렬·Accuracy는 적용 불가).

- **R²**: 모델이 데이터의 분산을 얼마나 설명하는지
- **MAE**: 평균 절대 오차
- **RMSE**: 평균 제곱근 오차 (큰 오차에 더 민감)

---

## 🤖 모델 비교 결과

### 기본 파라미터 vs 튜닝 후

| Model | Train R² | Test R² | Test MAE | Test RMSE |
|---|---|---|---|---|
| LinearRegression | 0.8620 | **0.8820** | **$2,290** | **$4,173** |
| RandomForest | 0.9744 | 0.8354 | $2,850 | $4,927 |
| XGBoost | 0.9903 | 0.8164 | $3,132 | $5,204 |
| **LinearRegression (튜닝)** | 0.8620 | **0.8820** | **$2,290** | **$4,173** |
| **RandomForest (튜닝)** | 0.8737 | 0.8756 | $2,501 | $4,284 |
| **XGBoost (튜닝)** | 0.8801 | 0.8795 | $2,398 | $4,217 |

> 튜닝 전 RandomForest·XGBoost는 Train R² 0.97~0.99인데 Test R²는 0.82 수준으로,
> 전형적인 **과적합** 양상을 보였습니다. 하이퍼파라미터 튜닝 후에는 과적합이 크게 줄고
> 세 모델의 Test R²가 0.876~0.882 사이로 수렴했습니다.

### 5-Fold 교차검증 (기본 파라미터)

| Model | CV R² 평균 | CV R² 표준편차 |
|---|---|---|
| LinearRegression | 0.8607 | 0.0324 |
| RandomForest | 0.8263 | 0.0328 |
| XGBoost | 0.8052 | 0.0305 |

### GridSearchCV 최적 하이퍼파라미터

- **LinearRegression**: `{'fit_intercept': True}` (Best CV R²: 0.8617)
- **RandomForest**: `{'max_depth': 5, 'min_samples_leaf': 5, 'n_estimators': 300}` (Best CV R²: 0.8569)
- **XGBoost**: `{'colsample_bytree': 0.8, 'learning_rate': 0.05, 'max_depth': 3, 'n_estimators': 100, 'reg_lambda': 1, 'subsample': 0.8}` (Best CV R²: 0.8600)

---

## 🏆 최종 모델 선택: XGBoost

성능만 놓고 보면 LinearRegression(Test R² 0.8820)이 근소하게 1위이지만,
**최종적으로는 XGBoost를 채택**했습니다.

> 성능면에선 LinearRegression가 1위이지만, 나중에 데이터가 더 모였을 때를 생각해
> 모델을 XGBoost로 정했다.

즉, 현재 시점의 성능 차이는 미미하지만(0.876~0.882 R²), 데이터가 더 쌓였을 때
**비선형 상호작용을 유연하게 학습할 수 있는 확장성**을 고려한 선택입니다.

| 항목 | 값 |
|---|---|
| 모델 | XGBoost (튜닝) |
| Test R² | 0.8795 |
| Test MAE | $2,398 |
| Test RMSE | $4,217 |
| 파라미터 | `n_estimators=100, max_depth=3, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, reg_lambda=1` |

---

## 💾 모델 저장

```python
import joblib, os

os.makedirs('models', exist_ok=True)

bundle = {
    'model': best_xgb,
    'scaler': scaler,
    'scale_features': numeric_features,     # ['age', 'bmi']
    'feature_order': X.columns.tolist(),
    'obese_threshold': 30,
    'model_name': 'XGBoost',
    'test_r2': 0.8795,
    'test_mae': 2398,
    'test_rmse': 4217,
}
joblib.dump(bundle, 'models/best_model.joblib')
```

---

## 🖥️ Streamlit 대시보드

노트북 분석 결과를 바탕으로 인터랙티브 웹 대시보드(`app.py`)를 함께 제공합니다.

### 폴더 구조

```
project/
├── app.py
├── insurance.csv
└── models/
    └── best_model.joblib
```

### 실행 방법

```bash
pip install streamlit pandas numpy matplotlib seaborn scikit-learn xgboost joblib
streamlit run app.py
```

### 탭 구성

| 탭 | 내용 |
|---|---|
| 📈 상관관계 & 분포 | 히트맵, 흡연/자녀 수별 진료비 박스플롯 |
| 🔬 산점도 분석 | 나이·BMI별 진료비 산점도 (흡연 여부 색상 구분) |
| 📋 데이터 미리보기 | 필터링된 원본 데이터 확인 및 CSV 다운로드 |
| 🧪 파생변수 추가 | 상호작용 변수 탐색용 (미리보기 + 상관계수) — 예측 모델과는 별개 |
| 📊 모델 비교 분석표 | 노트북에서 실제 실행한 정적 결과표 (재학습 없음) |
| 🔮 진료비 예측 | 저장된 `best_model.joblib`을 불러와 신규 고객 진료비 예측 + 테스트셋 재현 성능 확인 |

사이드바에서 나이·BMI·흡연 여부·자녀 수로 데이터를 필터링할 수 있습니다.

---

## 📦 주요 의존성

```
pandas
numpy
matplotlib
seaborn
scikit-learn
xgboost
streamlit
joblib
```

## ⚠️ 참고 사항

- `charges`는 연속값이므로 회귀 지표(R², MAE, RMSE)로만 평가하며, 분류용 지표(혼동행렬, Accuracy 등)는 사용하지 않습니다.
- `smoker` 특성 불균형(79.5% / 20.5%)을 고려해 `train_test_split`에 `stratify` 옵션을 적용했습니다.
- `charges` 이상치는 제거하지 않고, 흡연×비만 상호작용 파생변수로 반영해 모델이 학습하도록 했습니다.