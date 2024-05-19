import pandas as pd
import streamlit as st
from streamlit.errors import StreamlitAPIException
import os
from time import sleep
from pandasai import Agent, SmartDataframe
from pandasai.llm import OpenAI
from pandasai.exceptions import NoCodeFoundError

#This class manages the analysis of the dataset
#It uses the pandas library to read the dataset and analyze it
#It also uses the snowflake arctic LLM model to generate insights, and know what parts
#of the dataset to analyze

class csvgpt:
    def __init__(self, dataset) -> None:
        self.__dataset = dataset
        self.__back_slash = "\\"


    def analyze(self):
        self.__shape_of_dataset()
        self.__LLM_Analysis()


    def __shape_of_dataset(self):
        st.markdown("> Head of data")
        st.write(self.__dataset.head())

        st.markdown("> Tail of data")
        st.write(self.__dataset.tail())
        
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


    def __LLM_Analysis(self):
        os.environ["PANDASAI_API_KEY"] = os.environ.get("PANDASAI_API_KEY")
        llm = OpenAI(api_token=os.environ.get("OPENAI_API_KEY"))

        df = pd.DataFrame(self.__dataset)
        pAI = SmartDataframe(df, config={"verbose": True, "llm": llm})

        llm_analysis_response = pAI.chat("What is the context of this dataset, and what is it trying to find/track based on the context of the dataset? Also format your responsee by adding ** before and after key pieces of information")
        st.markdown(f"### Short summary of the dataset:")
        st.markdown(f"{llm_analysis_response}")

        llm_analysis_response = pAI.chat("What are the columns in the dataset, return the column names comma separated: column_1, column_2, column_3, ...")
        columms_list = llm_analysis_response.split(",")
        st.markdown(f"> The columns in the dataset are:")
        for column in columms_list:
            st.markdown(f"- {column}")

        
        st.markdown("""
                    > AI Analysis of the dataset
                    > Includes: min, max, mean, std, count, and more
        """)
        llm_analysis_response = pAI.chat("Please make a table for the min, max, mean, std, count, and unique values of the dataset")
        try:
            st.table(llm_analysis_response)
        except StreamlitAPIException as e:
            #Raise error to sentry to see what what type of data caused the error
            pass
            try:
                st.write(llm_analysis_response)
            except NoCodeFoundError as e:
                st.markdown(llm_analysis_response)
        except NoCodeFoundError as e:
            st.markdown(llm_analysis_response)

    
    def ask(self, question):
        os.environ["PANDASAI_API_KEY"] = os.environ.get("PANDASAI_API_KEY")
        llm = OpenAI(api_token=os.environ.get("OPENAI_API_KEY"))

        df = pd.DataFrame(self.__dataset)
        pAI = SmartDataframe(df, config={"verbose": True, "llm": llm})

        pAI.chat("I want to ask a question about the dataset")
        llm_analysis_response = pAI.chat(question)
        return llm_analysis_response

