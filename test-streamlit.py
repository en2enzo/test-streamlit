import streamlit as st


col_1, col_2, col_3 = st.columns(3)
button = col_1.button('真ん中カラムに文字を表示')
button2 = col_1.button('右カラムに文字を表示')
#buttonが押されたら
if button:
    col_2.write('ここは中央カラムです')

if button2:
    col_3.write('ここは右カラムです')
