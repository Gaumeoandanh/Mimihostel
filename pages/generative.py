import streamlit as st
import google.generativeai as genai
from PIL import Image

model = None
output_text = None
image = None
bytes_data = ''

def get_model():
    """
    Retrieves the Gemini model instance.

    Returns:
        The Gemini model instance.
    """
    global model
    if not model:
        genai.configure(api_key=st.secrets.gemini.api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    return model

# with st.form('generative-ai-form'):
text_input = st.text_input('Enter prompt')

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    with col2:
        image = Image.open(uploaded_file)
        st.image(image)

if st.button('Submit', use_container_width=True):
    if uploaded_file:
        response = get_model().generate_content([text_input, image])
    else :
        response = get_model().generate_text(text_input)

    output_text = response.text

if output_text:
    st.success(output_text)