import pandas as pd
import streamlit as st

#This class manages the analysis of the dataset
#It uses the pandas library to read the dataset and analyze it
#It also uses the snowflake arctic LLM model to generate insights, and know what parts
#of the dataset to analyze

class csvgpt:
    def __init__(self, dataset) -> None:
        self.__dataset = dataset

    def analyze(self):
        #Firstly get basic statisitcs of the dataset
        st.markdown("> Basic statistics of the dataset")
        pd_data_describe = self.__dataset.describe()
        data_row_count = len(self.__dataset)
        data_column_count = len(self.__dataset.columns)
        number_of_missing_values = self.__dataset.isnull().sum().sum()

        pd_df = pd.DataFrame({
            "Number of rows": [data_row_count],
            "Number of columns": [data_column_count],
            "Number of missing values": [number_of_missing_values]
        })

        st.table(pd_df)

