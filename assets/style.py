import streamlit as st

def render_css():
    # CSS tùy chỉnh để tạo kiểu cho nút
    st.markdown("""
        <style>
            .stMain {
                background: #fbeed8;
            }
            .stAppHeader {
                background-color: transparent
            }
            .title {
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px
            }
            .title h1 {
                margin-left: 10px; 
                font-weight: bold; 
                color: #EDACB1;
            }
            .st-key-logo-container .element-container > div {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-content: center;
                text-align: center;
            }
            .st-key-logo-container .element-container > div > div {
                margin: auto;
            }
            .stHeading {
                text-align: center;
            }
            .stFormSubmitButton > button,
            .stButton > button {
                background-color: #EDACB1;  /* Màu hồng pastel */
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px 20px;
                transition: .3s ease
            }
            .stFormSubmitButton > button:hover,
            .stButton > button:hover{
                background-color: #EF6F82;  /* Hồng pastel đậm hơn một chút */
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)