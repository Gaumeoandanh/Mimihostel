import streamlit as st

def render_css():
    # CSS tùy chỉnh để tạo kiểu cho nút
    st.markdown("""
        <style>
            .stMain {
                # background: #A888B5;
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
                color: #EFB6C8;
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
                background-color: #EFB6C8;  /* Màu hồng pastel */
                border: none;
                color: white;
                font-size: 16px;
                border-radius: .5rem;
                padding: .5rem 1rem;
                transition: .3s ease
            }
            .stFormSubmitButton > button:hover,
            .stFormSubmitButton > button:focus,
            .stFormSubmitButton > button:active,
            .stButton > button:hover,
            .stButton > button:focus,
            .stButton > button:active {
                background-color: #EF6F82;  /* Hồng pastel đậm hơn một chút */
                color: white !important;  
            }
            .stAlert .stAlertContainer.st-g9 {
                /* Màu thông báo error */
                background-color: rgb(238, 128, 128);
            }
            .stAlert .stAlertContainer.st-gm {
                /* Màu thông báo warning */
                # background-color: rgb(149, 144, 109);
            }
            .stAlert .stAlertContainer..st-j5 {
                /* Màu thông báo success */
              background-color: rgb(70, 255, 129);
            }
            [data-baseweb="input"],
            [data-baseweb="select"] > div,
            [data-testid="stNumberInputContainer"],
            [data-baseweb="textarea"] {
                # background-color: white; /* Màu nền trắng -- Already config in .streamlit/config.toml */
                # color: black; /* Màu chữ đen - Already config in .streamlit/config.toml */
                border: 1px solid #ccc !important; /* Viền nhẹ */
                # padding: .375rem; /* Tăng kích thước padding */
                border-radius: .5rem; /* Bo tròn góc */
            }
        </style>
    """, unsafe_allow_html=True)