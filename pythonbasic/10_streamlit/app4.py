import streamlit as st
import pandas as pd

# 제품 재고 데이터 생성
inventory = {
    "제품명": ["노트북", "모니터", "키보드"],
    "재고량": [25, 50, 100]
}
df = pd.DataFrame(inventory)

# 편집 가능한 테이블 생성
edited_df = st.data_editor(df, num_rows="dynamic")

st.write("수정된 데이터:", edited_df)