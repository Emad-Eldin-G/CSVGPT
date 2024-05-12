import pandas as pd
import streamlit as st
import os
from pandasai import Agent

os.environ["PANDASAI_API_KEY"] = "$2a$10$TYR1DHo20xqhWC2LI8pVze66Mswg4DfbHJwGRmUvXnjXfoIqqnnrS"

#This class manages the analysis of the dataset
#It uses the pandas library to read the dataset and analyze it
#It also uses the snowflake arctic LLM model to generate insights, and know what parts
#of the dataset to analyze

class csvgpt:
    def __init__(self, dataset) -> None:
        self.__dataset = dataset

    def analyze(self):
        self.shape_of_dataset()
        self.max_min_range_mean_mode()

    def shape_of_dataset(self):
        st.markdown("> Shape of data")
        pd_data_describe = self.__dataset.describe()
        data_row_count = len(self.__dataset)
        data_column_count = len(self.__dataset.columns)
        number_of_missing_values = self.__dataset.isnull().sum().sum()
        number_of_not_missing_values = self.__dataset.notnull().sum().sum()
        percentage_of_missing_values = (number_of_missing_values / (number_of_missing_values + number_of_not_missing_values)) * 100

        st.markdown(f"""
            - There are **{data_row_count}** rows in your dataset
            - There are **{data_column_count}** columns in your dataset
            - **{round(percentage_of_missing_values, 2)}%** of the cell values are missing ({number_of_missing_values} missing values)
            
        """)

    def max_min_range_mean_mode(self):
        #Present the max, min, range, mean, and mode in a streamlit table with two columns
        st.markdown("> Max, Min, Range, Mean, Mode")

        df = pd.DataFrame(self.__dataset)
        agent = Agent(df)
        
        max_col_num = agent.chat("""
            If there is any column that can be used, to calculate a max value from, that would be useful for the client to know,
            what columns are these. 
            Please answer in the following way:
            [Col-num-X, Col-num-Y]
            where the values in the array you give as answer are the col number only.
            """)
        
        st.write(max_col_num)