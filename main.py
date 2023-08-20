import os

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

from dotenv import load_dotenv, find_dotenv

import AppConstants
from PromptTemplates import system_template_string, human_template_string

_ = load_dotenv(find_dotenv())

st.title(AppConstants.icon + AppConstants.seperator + AppConstants.app_title)


def generate_response(input_text):
    llm = ChatOpenAI(model_name=AppConstants.CHAT_MODEL_GPT_3_5, temperature=AppConstants.ZERO_TEMPERATURE, openai_api_key=openai_api_key)
    x = llm(input_text)
    st.info(x.content)


if __name__ == '__main__':
    # Using object notation
    language = st.sidebar.selectbox(
        "Which language would you prefer?",
        ('English', 'Hindi')
    )

    # Using object notation
    role = st.sidebar.selectbox(
        "Which role you play in society?",
        ('Human', 'Student', 'Teacher', 'Doctor', 'Engineer', 'Son', 'Daughter', 'Wife', 'Husband')
    )

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template_string)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template_string)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    with st.form('my_form'):
        text = st.text_area('Just ask:')
        submitted = st.form_submit_button('Guide me')
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
        if submitted and openai_api_key.startswith('sk-'):
            customer_messages = chat_prompt.format_prompt(
                language=language,
                role=role, text=text).to_messages()
            generate_response(customer_messages)
