import streamlit as st
from openai import OpenAI

class Chatbot:
    """
    Chatbot class to interact with OpenAI's GPT-3 model.
    """

    # Set your OpenAI API key
    openai_client: OpenAI

    # Initialize the chatbot with a predefined set of initial prompts and an empty chat history
    chat_histories = []
    initial_prompts = []

    def __init__(self):
        self.openai_client = OpenAI(
            api_key=st.secrets.openapi.api_key,  # this is also the default, it can be omitted
        )

        self._training_bot()

    # Chatting with bots
    def send_message(self, message, stream=False):
        try:
            messages = self.initial_prompts
            messages.append({"role": "user", "content": message })

            # Gửi yêu cầu đến OpenAI API để lấy phản hồi
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=stream,
            )
            if stream:
                return response

            # Lấy phản hồi từ API và hiển thị
            bot_reply = response.choices[0].message.content

            # Lưu lại chat history
            self.chat_histories.append({"role": "user", "content": message })
            self.chat_histories.append({"role": "assistant", "content": bot_reply })

            return {
                "status": True,
                "reply": bot_reply,
            }
        except Exception as e:
            return {
                "status": False,
                "error": f"Error occurred: {e}",
            }

    def reset(self):
        self._training_bot()
        self.chat_histories = []

    # Training
    def _training_bot(self):
        # Add training prompts here to help the chatbot understand the context and provide appropriate responses.
        if True or "initial_prompts" not in st.session_state:
            self.initial_prompts = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant of Mimi hotel for cat with an IQ of 120."
                },
                {
                    "role": "system",
                    "content": """
                    You are a friendly and smart assistant at a cat hotel named Mimi with an IQ of 120 . 
                    This hotel provides boarding and premium care services for cats while their owners are away. 
                    Respond in a friendly, concise, and helpful manner. 
                    If asked about services, provide a brief explanation and its price:
                    Accommodation Packages:
                    Standard Room: A private, comfortable space with a cozy bed, scratching post, and daily meals.Price: 20,000 KRW per night.
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
                    The guest can book a room on this web by clicking the booking button on the homepage.
                    """
                },
                {
                    "role": "user",
                    "content": "What is your address?"
                },
                {
                    "role": "assistant",
                    "content": "Our address: 서울특별시 광진구 능동로 209."
                },
                {
                    "role": "user",
                    "content": "Asking about menu or services"
                },
                {
                    "role": "assistant",
                    "content": "We have Accommodation Packages and another services such as Grooming, Health checking or Training while accomodating. If you want to view our menu, please click the menu button at the top :D "
                },
                {
                    "role": "user",
                    "content": "Can you give me your contact?"
                },
                {
                    "role": "assistant",
                    "content": "Our phone number is: 010-8040-1314 and our email: cathotelm@gmail.com"
                },
                {
                    "role": "user",
                    "content": "How can I book a room for cat?"
                },
                {
                    "role": "assistant",
                    "content": "You can book a room on this web by clicking the booking button on the homepage :D"
                }
            ]
            st.session_state.initial_prompts = self.initial_prompts
        else:
            self.initial_prompts = st.session_state.initial_prompts
