import streamlit as st
import pandas as pd
import numpy as np
from time import sleep
from analyzer import csvgpt
from PIL import Image
import pandasai

#css styling
st.markdown(
    """
    <style>
    </style>
    """
    ,
    unsafe_allow_html=True
)


#Sidebar
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

#Header
title = st.title("CSVGPT")
header = st.subheader("Blaze through datasets like a pro 🚀:H")

#Help section
open_button = st.toggle("How to use")

if open_button:
    st.markdown(
    """
    > In 3 simple steps

    1. **Upload your dataset** in a CSV format
    2. **Click Analyze** - Click the Analyze button to start analysis using our **AI**
    3. **Get insights** - Get insights, graphs, and summaries on your dataset in seconds ⚡️
        
    """)

st.divider()
#Free gap
st.markdown("<br>", unsafe_allow_html=True)

#Upload dataset
st.markdown("## Upload your dataset :file_folder:")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
is_uploaded = False
if uploaded_file is not None:
    sleep(0.3)
    st.success("Dataset uploaded successfully")
    is_uploaded = True


#Analyze button
if is_uploaded:
    analyze_button = st.button("Analyze 🔮", disabled=False)
else:
    analyze_button = st.button("Analyze 🔮", disabled=True)

if analyze_button:
    if is_uploaded:
        try:
            read_csv = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            st.error("Please upload a valid CSV file")
    else:
        st.warning("Please upload a valid csv dataset first")

    if is_uploaded:
        #Analyze dataset
        with st.spinner('Analyzing dataset... 🕵️‍♂️'):
            sleep(5)
        with st.spinner('Doing our magic... ✨'):
            sleep(5)
        with st.spinner('This might take a while... 🕰️'):
            #Instantiate the csvgpt class
            csvgpt_instance = csvgpt(read_csv)
            csvgpt_instance.analyze()
    else:
        #do nothing, the warning message will be sent from the catch error above
        pass

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

#Ask questions about data (Uses Vana and LLMS)
if is_uploaded:
    text_area = st.text_area("Ask CSVGPT a question about your data ✨", disabled=False)
    submit_button = st.button("Ask CSVGPT", disabled=False)
else:
    text_area = st.text_area("Ask CSVGPT a question about your data ✨", disabled=True)
    submit_button = st.button("Ask CSVGPT", disabled=True)


if submit_button:
    if is_uploaded:
        df = pd.read_csv(uploaded_file)
        st.write(df.head())
    else:
        st.warning("Please upload a valid csv dataset first")