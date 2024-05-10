
import streamlit as st
import pandas as pd
import numpy as np
from time import sleep
from analyzer import csvgpt

#css hack through markdown
#animated gradient background
#make all text grey
st.markdown(
    """
    <style>
    </style>
    """
    ,
    unsafe_allow_html=True
)

#Header
title = st.title("CSVGPT:H")
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


#Free gap
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


#Analyze button
if st.button("Analyze 🔮"):
    if is_uploaded:
        try:
            df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            st.error("Please upload a valid CSV file")
    else:
        st.warning("Please upload a valid csv dataset first")
    
    #Analyze dataset
    with st.spinner('Analyzing dataset... 🕵️‍♂️'):
        sleep(5)
    with st.spinner('Doing our magic... ✨'):
        sleep(5)
    with st.spinner('This might take a while... 🕰️'):
        #Instantiate the csvgpt class
        csvgpt_instance = csvgpt(df)
        csvgpt_instance.analyze()



#Ask questions about data (Uses Vana and LLMS)
if is_uploaded:
    text_area = st.text_area("Ask CSVGPT a question about your data ✨", disabled=False)
else:
    text_area = st.text_area("Ask CSVGPT a question about your data ✨", disabled=True)


if st.button("Ask CSVGPT"):
    if is_uploaded:
        df = pd.read_csv(uploaded_file)
        st.write(df.head())
    else:
        st.warning("Please upload a valid csv dataset first")