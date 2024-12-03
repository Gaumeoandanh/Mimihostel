import streamlit as st
import os
from openai import OpenAI
from langdetect import detect
from googletrans import Translator
from dotenv import load_dotenv

# Load environment variables from .env file (located in the same directory)
load_dotenv()

# Set your OpenAI API key
client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),  # this is also the default, it can be omitted
)

# CSS tùy chỉnh để tạo kiểu cho nút
st.markdown("""
    <style>
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
        color: black;
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

# Hiển thị input và nút gửi
with st.container():
    # Title for the web app
    st.title("Welcome to Mimi Hostel")

    # Hiển thị logo và tên
    st.markdown("""
        <div class="title">
            Am <h1>MiMi</h1> Bot
        </div>
    """, unsafe_allow_html=True)
    with st.container(key="logo-container"):
        st.image("cat.png", width=200)
        st.write("How may I help you!")


    with st.form("my_form", border=False):
        user_input = st.text_input(
            label="Chat with me:",
            placeholder="Type your question here...",
            key="user_input",
            help="Enter your message here."
        )
        send_button = st.form_submit_button(label="Send")


# Xử lý lịch sử hội thoại
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant of Mimi hostel for cat."}]

# Hàm dịch câu trả lời của bot sang ngôn ngữ người dùng
def translate_text(text, target_lang):
    translator = Translator()
    translated = translator.translate(text, dest=target_lang)
    return translated.text

# Xử lý khi người dùng nhấn nút "Send"
if send_button:
    if user_input:
        # Thêm câu hỏi của người dùng vào lịch sử hội thoại
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            # Nếu là lần đầu tiên trò chuyện, thiết lập hướng dẫn cho bot (system message)
            if len(st.session_state.messages) == 2:  # Sau khi người dùng gửi câu hỏi đầu tiên
                # Thêm tin nhắn hệ thống chỉ một lần để hướng dẫn bot
                st.session_state.messages.insert(0, {
                    "role": "system",
                    "content": """
                    You are a friendly assistant at a cat hotel named Mimi. 
                    This hotel provides boarding and premium care services for cats while their owners are away. 
                    Respond in a friendly, concise, and helpful manner. 
                    If asked about services, provide a brief explanation and its price:
                    Accommodation Packages:Standard Room: A private, comfortable space with a cozy bed, scratching post, and daily meals.Price: 20,000 KRW per night.
                    Deluxe Room:Spacious private room with extra toys, a climbing tower, and a premium bed.Price: 35,000 KRW per night
                    VIP Suite:Luxurious suite with panoramic window views, personalized toys, daily grooming, and premium meals.Price: 60,000 KRW per night.
                    Additional Services: Grooming:Includes brushing, nail trimming, and basic cleaning.Price: 15,000 KRW per session.
                    Health Check-Up:Performed by a professional vet to ensure your cat’s well-being.Price: 30,000 KRW per session.
                    Playtime with Staff:One-on-one play sessions with our trained staff.Price: 10,000 KRW per session (30 minutes)
                    Daily Photo Updates:Receive photos and updates of your cat during their stay.Price: 5,000 KRW per day.
                    Food Options: Basic Meals:High-quality cat food provided daily.Included in room price.
                    Premium Meals:Specially curated meals with fresh ingredients.Price: 10,000 KRW per day.
                    Custom Meal Plan:Tailored meals based on your cat’s specific dietary needs.Price: 15,000 KRW per day.
                    Promotions: Opening Special: Enjoy 10% off for stays longer than 5 nights (valid until MM/DD/YYYY). 
                    Membership Program: Get 1 free night after every 10-night stay.
                    Grooming Package Deal:Book 3 grooming sessions and get the 4th one free.
                    """
                })
                #(huấn luyện)
                st.session_state.messages.append({
                    "role": "user",
                    "content": "What is your address?"
                })
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Our address: 서울특별시 광진구 능동로 209."
                })
                #(huấn luyện)
                st.session_state.messages.append({
                    "role": "user",
                    "content": "Can you give me your contact?"
                })
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Our phone number is: 010-8040-1314 and our email: mimihostel@gmail.com"
                })


            # Gửi yêu cầu đến OpenAI API để lấy phản hồi
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            # Lấy phản hồi từ API và hiển thị
            bot_reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

            # Hiển thị phản hồi từ bot
            st.markdown(f"**Bot:** {bot_reply}")

        except Exception as e:
            st.error(f"Error occurred: {e}")
    else:
        st.warning("Please enter a message before sending.")



