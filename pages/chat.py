import streamlit as st
from google_trans_new import google_translator
from services.chatbot import Chatbot

class ChatModule:
    """
    A class to create a chatbot interface using OpenAI and Google Translate.
    """

    # Set up Google Translate API
    translator = google_translator()
    chatbot = Chatbot()

    # Variables
    chat_message = ""
    send_button = None

    def run(self):
        self._render_ui()
        self._load_behaviours()

    def get_avatar(self, role):
        if role == "assistant":
            return "🐱"
        return None

    def _render_ui(self):
        if st.button("Back"):
            st.switch_page(page='pages/home.py')

        if "chat_histories" in st.session_state:
            st.button("New Chat", on_click=self.new_chat)

        st.title("Chat with me", anchor=False)

        # Display chat messages from history on app rerun
        if "chat_histories" in st.session_state:
            for message in st.session_state.chat_histories:
                with st.chat_message(message["role"], avatar=self.get_avatar(message["role"])):
                    st.markdown(message["content"])
        else:
            st.session_state.chat_histories = []

        # Accept user input
        if prompt := st.chat_input("Type your question here"):
            self.chat_message = prompt
            # Add user message to chat history
            st.session_state.chat_histories.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

        # self.chat_message = st.chat_input("Type your question here")

    def new_chat(self):
        st.session_state.chat_histories = []
        self.chatbot.reset()
        self.chat_message = ""


    def _load_behaviours(self):
        if self.chat_message:
            # Add message to chat box
            # st.session_state.chat_histories.append({"role": "user", "content": self.chat_message})

            # Send message to Chatbots
            # Send message streaming
            stream = self.chatbot.send_message(message=self.chat_message, stream=True)
            response = st.write_stream(stream)
            st.session_state.chat_histories.append({"role": "assistant", "content": response})

            # Send message directly
            # response = self.chatbot.send_message(message=self.chat_message)
            # if response["status"]:
            #     # Append to chat box
            #     st.session_state.chat_histories.append({"role": "assistant", "content": response["reply"]})
            # else:
            #     # Display default error message
            #     st.session_state.chat_histories.append({"role": "assistant", "content": "Ops! Something when wrong."})

            st.rerun()

    # Hàm dịch câu trả lời của bot sang ngôn ngữ người dùng
    def _translate_text(self, text, target_lang):
        translated = self.translator.translate(text, dest=target_lang)
        return translated.text

chat_module = ChatModule()
chat_module.run()
