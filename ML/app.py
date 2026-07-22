import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# ---------- 한글 폰트 설정 ----------
plt.rcParams['axes.unicode_minus'] = False
try:
    matplotlib.rcParams['font.family'] = 'NanumGothic'
except Exception:
    pass

st.set_page_config(page_title="진료비 데이터 분석 대시보드", layout="wide")

# ---------- 데이터 로드 ----------
DATA_PATH = "data/insurance.csv"  # 이 스크립트와 같은 폴더에 insurance.csv를 두세요
df = pd.read_csv(DATA_PATH)

st.title("📊 진료비(charges) 데이터 탐색적 분석 대시보드")
st.caption(f"데이터 파일: {DATA_PATH}  |  총 {len(df)}행")

required_cols = {'age', 'bmi', 'children', 'charges', 'smoker', 'sex'}
missing = required_cols - set(df.columns)
if missing:
    st.error(f"다음 컬럼이 데이터에 없습니다: {missing}")
    st.stop()

# ---------- 상관관계 계산을 위한 인코딩 ----------
df_corr = df.copy()
if not pd.api.types.is_numeric_dtype(df_corr['smoker']):
    df_corr['smoker'] = df_corr['smoker'].astype(str).map({'yes': 1, 'no': 0})
if not pd.api.types.is_numeric_dtype(df_corr['sex']):
    df_corr['sex'] = df_corr['sex'].astype(str).map({'male': 1, 'female': 0})

# ---------- 사이드바 필터 ----------
st.sidebar.header("🔍 필터")

age_min, age_max = int(df['age'].min()), int(df['age'].max())
age_range = st.sidebar.slider("나이 범위", age_min, age_max, (age_min, age_max))

bmi_min, bmi_max = float(df['bmi'].min()), float(df['bmi'].max())
bmi_range = st.sidebar.slider("BMI 범위", bmi_min, bmi_max, (bmi_min, bmi_max))

smoker_options = df['smoker'].unique().tolist()
smoker_sel = st.sidebar.multiselect("흡연 여부", smoker_options, default=smoker_options)

children_options = sorted(df['children'].unique().tolist())
children_sel = st.sidebar.multiselect("자녀 수", children_options, default=children_options)

filtered_df = df[
    (df['age'].between(*age_range)) &
    (df['bmi'].between(*bmi_range)) &
    (df['smoker'].isin(smoker_sel)) &
    (df['children'].isin(children_sel))
]

filtered_corr = df_corr.loc[filtered_df.index]

st.sidebar.markdown(f"**선택된 행 수:** {len(filtered_df)} / {len(df)}")

if filtered_df.empty:
    st.warning("선택한 조건에 해당하는 데이터가 없습니다. 필터를 조정해주세요.")
    st.stop()

# ---------- 요약 지표 ----------
col1, col2, col3, col4 = st.columns(4)
col1.metric("평균 진료비", f"${filtered_df['charges'].mean():,.0f}")
col2.metric("중앙값 진료비", f"${filtered_df['charges'].median():,.0f}")
col3.metric("평균 BMI", f"{filtered_df['bmi'].mean():.1f}")
col4.metric("평균 나이", f"{filtered_df['age'].mean():.1f}")

st.divider()

# ---------- 탭 구성 ----------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["📈 상관관계 & 분포", "🔬 산점도 분석", "📋 데이터 미리보기",
     "🧪 파생변수 추가", "📊 모델 비교 분석표", "🔮 진료비 예측"]
)

with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("상관관계 히트맵")
        corr_cols = ['age', 'bmi', 'children', 'charges', 'smoker', 'sex']
        corr = filtered_corr[corr_cols].corr()
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax, square=True)
        st.pyplot(fig)

    with c2:
        st.subheader("흡연 유무별 진료비")
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.boxplot(data=filtered_df, x='smoker', y='charges', hue='smoker', legend=False, ax=ax)
        st.pyplot(fig)

    st.subheader("자녀 수별 진료비")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=filtered_df, x='children', y='charges', hue='children', legend=False, ax=ax, palette='Set3')
    st.pyplot(fig)

with tab2:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("나이별 진료비")
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.scatterplot(data=filtered_df, x='age', y='charges', hue='smoker', alpha=0.6, ax=ax)
        st.pyplot(fig)

    with c2:
        st.subheader("BMI별 진료비")
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.scatterplot(data=filtered_df, x='bmi', y='charges', hue='smoker', alpha=0.6, ax=ax)
        st.pyplot(fig)

with tab3:
    st.subheader("필터링된 원본 데이터")
    st.dataframe(filtered_df, use_container_width=True)
    st.download_button(
        "필터링된 데이터 CSV 다운로드",
        filtered_df.to_csv(index=False).encode('utf-8-sig'),
        file_name="filtered_data.csv",
        mime="text/csv"
    )

with tab4:
    st.subheader("🧪 파생변수(상호작용 변수) 만들기")
    st.caption("여기서 켠 파생변수는 '🤖 진료비 예측 모델' 탭에 자동으로 반영되어 학습에 사용됩니다.")

    obese_threshold = st.number_input(
        "비만 판정 기준 BMI", min_value=20.0, max_value=40.0,
        value=st.session_state.get('fe_obese_threshold', 30.0), step=0.5
    )
    st.session_state['fe_obese_threshold'] = obese_threshold

    fc1, fc2 = st.columns(2)
    with fc1:
        fe_smoker_bmi = st.checkbox(
            "흡연 × BMI (smoker_bmi)",
            value=st.session_state.get('fe_smoker_bmi', True)
        )
        fe_smoker_age = st.checkbox(
            "흡연 × 나이 (smoker_age)",
            value=st.session_state.get('fe_smoker_age', True)
        )
    with fc2:
        fe_bmi_obese = st.checkbox(
            f"비만 여부, BMI ≥ {obese_threshold:.1f} (bmi_obese)",
            value=st.session_state.get('fe_bmi_obese', True)
        )
        fe_smoker_obese = st.checkbox(
            "흡연 × 비만 (smoker_obese)",
            value=st.session_state.get('fe_smoker_obese', True),
            disabled=not fe_bmi_obese,
            help="비만 여부(bmi_obese)를 먼저 켜야 사용할 수 있습니다."
        )

    st.session_state['fe_smoker_bmi'] = fe_smoker_bmi
    st.session_state['fe_smoker_age'] = fe_smoker_age
    st.session_state['fe_bmi_obese'] = fe_bmi_obese
    st.session_state['fe_smoker_obese'] = fe_smoker_obese and fe_bmi_obese

    # ---------- 미리보기용 파생변수 계산 ----------
    preview_df = filtered_df.copy()
    smoker_num_preview = (preview_df['smoker'].astype(str).str.strip().str.lower() == 'yes').astype(int)

    if fe_bmi_obese:
        preview_df['bmi_obese'] = (preview_df['bmi'] >= obese_threshold).astype(int)
    if fe_smoker_bmi:
        preview_df['smoker_bmi'] = smoker_num_preview * preview_df['bmi']
    if fe_smoker_age:
        preview_df['smoker_age'] = smoker_num_preview * preview_df['age']
    if fe_smoker_obese and fe_bmi_obese:
        preview_df['smoker_obese'] = smoker_num_preview * preview_df['bmi_obese']

    new_cols = [c for c in ['smoker_bmi', 'smoker_age', 'bmi_obese', 'smoker_obese']
                if c in preview_df.columns]

    st.divider()

    if not new_cols:
        st.info("위에서 최소 하나 이상의 파생변수를 켜주세요.")
    else:
        st.markdown("#### 👀 미리보기 (상위 20행)")
        st.dataframe(
            preview_df[['age', 'bmi', 'smoker', 'charges'] + new_cols].head(20),
            use_container_width=True
        )

        st.markdown("#### 📊 파생변수와 진료비(charges)의 상관계수")
        corr_vals = preview_df[new_cols + ['charges']].corr()['charges'].drop('charges')
        corr_vals = corr_vals.sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(6, max(2, len(corr_vals) * 0.7)))
        colors = ['crimson' if v < 0 else 'steelblue' for v in corr_vals]
        ax.barh(corr_vals.index, corr_vals.values, color=colors)
        ax.set_xlabel("charges와의 상관계수")
        st.pyplot(fig)

        st.caption(
            "값이 1에 가까울수록 해당 파생변수가 커질 때 진료비도 함께 커지는 경향이 강하다는 뜻입니다."
        )

    st.info(
        "ℹ️ 이 탭은 탐색용입니다. '🔮 진료비 예측' 탭은 노트북에서 저장한 모델을 그대로 불러와 사용하며, "
        "이미 4가지 파생변수(smoker_bmi, smoker_age, bmi_obese, smoker_obese)가 고정 반영되어 있습니다."
    )


with tab5:
    st.subheader("📊 모델 비교 분석표")
    st.caption(
        "아래 결과는 실시간으로 재학습한 것이 아니라, "
        "주피터 노트북에서 실제로 학습·평가한 결과를 그대로 옮긴 정적(static) 표입니다."
    )

    st.markdown("#### 1) 기본 파라미터 vs 튜닝 후 (Train/Test 성능)")
    comparison_data = {
        'Model': [
            'LinearRegression', 'RandomForest', 'XGBoost',
            'LinearRegression (튜닝)', 'RandomForest (튜닝)', 'XGBoost (튜닝)'
        ],
        'Train R²': [0.8620, 0.9744, 0.9903, 0.8620, 0.8737, 0.8801],
        'Test R²': [0.8820, 0.8354, 0.8164, 0.8820, 0.8756, 0.8795],
        'Test MAE': [2290, 2850, 3132, 2290, 2501, 2398],
        'Test RMSE': [4173, 4927, 5204, 4173, 4284, 4217],
    }
    comparison_df = pd.DataFrame(comparison_data)

    def _highlight_best(row):
        is_best = row['Model'] == 'LinearRegression (튜닝)'
        return ['background-color: #d4edda' if is_best else '' for _ in row]

    st.dataframe(
        comparison_df.style.apply(_highlight_best, axis=1).format({
            'Train R²': '{:.4f}', 'Test R²': '{:.4f}',
            'Test MAE': '${:,.0f}', 'Test RMSE': '${:,.0f}'
        }),
        use_container_width=True, hide_index=True
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    x_pos = np.arange(len(comparison_df))
    colors = ['#2e7d32' if m == 'LinearRegression (튜닝)' else '#4c78a8' for m in comparison_df['Model']]
    ax.bar(x_pos, comparison_df['Test R²'], color=colors)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(comparison_df['Model'], rotation=30, ha='right')
    ax.set_ylabel('Test R²')
    ax.set_ylim(0.7, 0.95)
    ax.set_title('모델별 Test R² 비교')
    st.pyplot(fig)

    st.success(
        "🏆 **최종 선택 모델: LinearRegression (튜닝)** — Test R² 0.8820으로 가장 높고, "
        "Train/Test 차이가 거의 없어 과적합도 적으며, 구조가 단순해 해석과 배포가 쉽습니다. "
        "'🔮 진료비 예측' 탭에서 이 모델(저장된 파일)만 불러와 사용합니다."
    )

    st.markdown("#### 2) 5-Fold 교차검증 (기본 파라미터, 전체 데이터 기준)")
    cv_data = {
        'Model': ['LinearRegression', 'RandomForest', 'XGBoost'],
        'CV R² 평균': [0.8607, 0.8263, 0.8052],
        'CV R² 표준편차': [0.0324, 0.0328, 0.0305],
    }
    st.dataframe(pd.DataFrame(cv_data), use_container_width=True, hide_index=True)
    st.caption(
        "교차검증에서도 LinearRegression이 가장 안정적으로 높은 R²를 보였습니다. "
        "트리 기반 모델(RF/XGBoost)은 Train R²는 매우 높지만 Test R²가 상대적으로 낮아 "
        "과적합 경향이 있는 것으로 보입니다 (원본 노트북 파생변수: smoker_bmi, smoker_age, "
        "bmi_obese, smoker_obese 기준)."
    )

    st.markdown("#### 3) 최적 하이퍼파라미터 (GridSearchCV 결과)")
    st.write("**LinearRegression**: `{'fit_intercept': True}` (Best CV R²: 0.8617)")
    st.write("**RandomForest**: `{'max_depth': 5, 'min_samples_leaf': 5, 'n_estimators': 300}` (Best CV R²: 0.8569)")
    st.write("**XGBoost**: `{'colsample_bytree': 0.8, 'learning_rate': 0.05, 'max_depth': 3, "
             "'n_estimators': 100, 'reg_lambda': 1, 'subsample': 0.8}` (Best CV R²: 0.8600)")

with tab6:
    st.subheader("🔮 진료비 예측 (저장된 모델 사용)")

    MODEL_PATH = "models/best_model.joblib"

    if not os.path.exists(MODEL_PATH):
        st.error(
            f"'{MODEL_PATH}' 파일을 찾을 수 없습니다. "
            "노트북에서 학습한 모델을 joblib으로 저장한 뒤, app.py와 같은 폴더에 넣어주세요."
        )
        st.code(
            "import joblib\n"
            "bundle = {\n"
            "    'model': lr_model,          # 학습된 LinearRegression\n"
            "    'scaler': scaler,           # MinMaxScaler (age, bmi 학습에 사용)\n"
            "    'scale_features': ['age', 'bmi'],\n"
            "    'feature_order': X.columns.tolist(),\n"
            "    'obese_threshold': 30,\n"
            "}\n"
            "joblib.dump(bundle, 'best_model.joblib')",
            language="python"
        )
        st.stop()

    bundle = joblib.load(MODEL_PATH)
    model = bundle['model']
    scaler = bundle['scaler']
    scale_features = bundle['scale_features']       # ['age', 'bmi']
    feature_order = bundle['feature_order']
    obese_threshold = bundle.get('obese_threshold', 30)



    st.divider()
    st.markdown("### 새 고객 정보 입력")

    p1, p2, p3 = st.columns(3)
    with p1:
        input_age = st.number_input("나이", min_value=18, max_value=100, value=35)
        input_children = st.number_input("자녀 수", min_value=0, max_value=10, value=0)
    with p2:
        input_bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=28.0, step=0.1)
        input_sex = st.selectbox("성별", ["male", "female"])
    with p3:
        input_smoker = st.selectbox("흡연 여부", ["no", "yes"])

    if st.button("💰 예상 진료비 계산하기", type="primary"):
        smoker_num = 1 if input_smoker == "yes" else 0
        sex_num = 1 if input_sex == "male" else 0
        bmi_obese = 1 if input_bmi >= obese_threshold else 0

        row = {
            'age': input_age,
            'sex': sex_num,
            'bmi': input_bmi,
            'children': input_children,
            'smoker': smoker_num,
            'smoker_bmi': smoker_num * input_bmi,
            'smoker_age': smoker_num * input_age,
            'bmi_obese': bmi_obese,
            'smoker_obese': smoker_num * bmi_obese,
        }
        input_row = pd.DataFrame([row])[feature_order]
        input_row[scale_features] = scaler.transform(input_row[scale_features])

        prediction = model.predict(input_row)[0]
        st.success(f"### 예상 진료비: **${prediction:,.0f}**")

        if input_smoker == "yes":
            st.caption("⚠️ 흡연자는 비흡연자보다 평균적으로 훨씬 높은 진료비가 예측됩니다.")

    st.divider()
    st.markdown("### 📈 저장된 모델의 실제값 vs 예측값 (테스트셋 재현)")

    # ---------- 노트북과 동일한 절차로 X, y 재구성 ----------
    df_repro = df.copy()
    if not pd.api.types.is_numeric_dtype(df_repro['sex']):
        df_repro['sex'] = df_repro['sex'].map({'male': 1, 'female': 0})
    if not pd.api.types.is_numeric_dtype(df_repro['smoker']):
        df_repro['smoker'] = df_repro['smoker'].map({'yes': 1, 'no': 0})
    if 'region' in df_repro.columns:
        df_repro = df_repro.drop(columns=['region'])

    X_repro = df_repro.drop(columns=['charges'])
    y_repro = df_repro['charges']
    X_repro['smoker_bmi'] = X_repro['smoker'] * X_repro['bmi']
    X_repro['smoker_age'] = X_repro['smoker'] * X_repro['age']
    X_repro['bmi_obese'] = (X_repro['bmi'] >= obese_threshold).astype(int)
    X_repro['smoker_obese'] = X_repro['smoker'] * X_repro['bmi_obese']
    X_repro = X_repro[feature_order]

    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
        X_repro, y_repro, test_size=0.2, random_state=42, stratify=X_repro['smoker']
    )
    X_test_r = X_test_r.copy()
    X_test_r[scale_features] = scaler.transform(X_test_r[scale_features])

    y_pred_r = model.predict(X_test_r)

    r2_r = r2_score(y_test_r, y_pred_r)
    mae_r = mean_absolute_error(y_test_r, y_pred_r)
    rmse_r = np.sqrt(mean_squared_error(y_test_r, y_pred_r))

    rc1, rc2, rc3 = st.columns(3)
    rc1.metric("R²", f"{r2_r:.4f}")
    rc2.metric("MAE", f"${mae_r:,.0f}")
    rc3.metric("RMSE", f"${rmse_r:,.0f}")

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(y_test_r, y_pred_r, alpha=0.5)
    max_val = max(y_test_r.max(), y_pred_r.max())
    ax.plot([0, max_val], [0, max_val], 'r--', label='y = x (완벽 예측선)')
    ax.set_xlabel('실제값 (Actual charges)')
    ax.set_ylabel('예측값 (Predicted charges)')
    ax.set_title(f"{bundle.get('model_name', 'LinearRegression')}: 실제값 vs 예측값")
    ax.legend()
    st.pyplot(fig)