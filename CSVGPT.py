import streamlit as st
import pandasai
import os

from analyzer import csvgpt
import helpers

import pandas as pd
import numpy as np
from time import sleep
from PIL import Image


def configure_page():
    st.set_page_config(page_title="CSVGPT", page_icon="📊🪄", layout="wide", initial_sidebar_state="auto")

    # CSS styling
    st.markdown(
        """
        <style>
        </style>
        """,
        unsafe_allow_html=True
    )


def configure_sidebar():
    st.sidebar.markdown("# CSVGPT | Open-Source 📊")
    st.sidebar.markdown("## Created by [EmadEldin Osman](https://github.com/Emad-Eldin-G)")
    st.sidebar.markdown("## To contribute, raise an issue on the [GitHub repo](https://github.com/Emad-Eldin-G/CSVGPT/issues)")
    st.sidebar.divider()
    st.sidebar.markdown("""
    ### Powered by:  
    - [Streamlit](https://streamlit.io/)
    - [Pandas](https://pandas.pydata.org/)
    - [NumPy](https://numpy.org/)  
    - [Pandasai](https://pandas-ai.com/)
    """)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)


def display_header():
    st.title("CSVGPT")
    st.subheader("Blaze through datasets like a pro 🚀:H")


def display_help_section():
    open_button = st.toggle("How to use")
    if open_button:
        st.markdown(
            """
            > In 3 simple steps

            1. **Upload your dataset** in a CSV format
            2. **Click Analyze** - Click the Analyze button to start analysis using our **AI**
            3. **Get insights** - Get insights, graphs, and summaries on your dataset in seconds ⚡️
            """)


def upload_dataset():
    st.markdown("## Upload your dataset :file_folder:")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    is_uploaded = False
    if uploaded_file is not None:
        sleep(0.3)
        st.success("Dataset uploaded successfully")
        is_uploaded = True
    return uploaded_file, is_uploaded


def analyze_dataset(is_uploaded, uploaded_file):
    if is_uploaded:
        analyze_button = st.button("Analyze 🔮", disabled=False)
        try:
            read_csv = pd.read_csv(uploaded_file)
            csvgpt_instance = csvgpt(read_csv)
        except Exception as e:
            st.warning("Please upload a valid csv dataset")
            analyze_button = st.button("Analyze 🔮", disabled=True)
    else:
        analyze_button = st.button("Analyze 🔮", disabled=True)
        csvgpt_instance = None

    if analyze_button and is_uploaded:
        with st.spinner('Analyzing dataset... 🕵️‍♂️'):
            sleep(5)
        with st.spinner('Doing our magic... ✨'):
            sleep(5)
        with st.spinner('This might take a while... 🕰️'):
            csvgpt_instance.analyze()

    return csvgpt_instance


def ask_question(is_uploaded, csvgpt_instance):
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message["sender"] == "user":
            user = responses_container.chat_message("user")
            user.write("You")
            user.write(message["content"])
        else:
            bot = responses_container.chat_message("assistant")
            bot.write("Response")
            bot.write(message["content"])

    chat_container = st.container()

    if is_uploaded:
        chat_container.write("### Chat with your Dataset 🤖")
        text_area = chat_container.chat_input("Chat here", disabled=False)
    else:
        chat_container.write("### Chat with your Dataset 🤖")
        text_area = chat_container.chat_input("Chat here", disabled=True)

    responses_container = st.container()

    if text_area:
        with st.spinner('Thinking... 🤔'):
            sleep(2)
            response_from_bot = csvgpt_instance.ask(text_area)

            st.session_state.messages.append({"content": text_area, "sender": "user"})
            st.session_state.messages.append({"content": response_from_bot, "sender": "assistant"})

            bot = chat_container.chat_message("assistant")
            bot.write("Response")
            
            #check if the returned response is an image path
            if ( response_from_bot.endswith('.png') or response_from_bot.endswith('.jpg') or response_from_bot.endswith('.jpeg') ):
                image = Image.open(response_from_bot)
                bot.image(image)
            else:
                bot.write(f"{response_from_bot}")


def main():
    configure_page()
    configure_sidebar()
    display_header()
    display_help_section()

    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)

    uploaded_file, is_uploaded = upload_dataset()
    csvgpt_instance = analyze_dataset(is_uploaded, uploaded_file)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    ask_question(is_uploaded, csvgpt_instance)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pass
