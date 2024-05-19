import pandas as pd
import streamlit as st
from streamlit.errors import StreamlitAPIException
import os
from time import sleep
from pandasai import Agent, SmartDataframe
from pandasai.llm import OpenAI
from pandasai.exceptions import NoCodeFoundError

from container_manager import print_to_analyze_button_response, print_to_chat_response

#This class manages the analysis of the dataset
#It uses the pandas library to read the dataset and analyze it
#It also uses the snowflake arctic LLM model to generate insights, and know what parts
#of the dataset to analyze


class csvgpt:
    def __init__(self, dataset) -> None:
        os.environ["PANDASAI_API_KEY"] = os.environ.get("PANDASAI_API_KEY")
        self.llm = OpenAI(api_token=os.environ.get("OPENAI_API_KEY"))
        self.analyze_manager = print_to_analyze_button_response()
        self.chat_manager = print_to_chat_response()
        self.__dataset = dataset
        self.__back_slash = "\\"

    @staticmethod
    def print_reponse_in_yield_delay(response, delay=0.15):
        for i in response:
            yield i
            sleep(delay)

    def analyze(self):
        analyze_manager = print_to_analyze_button_response()
        self.__shape_of_dataset()
        self.__LLM_Analysis()


    def __shape_of_dataset(self):
        self.analyze_manager.markdown("> Head of data")
        self.analyze_manager.write(self.__dataset.head())

        self.analyze_manager.markdown("> Tail of data")
        self.analyze_manager.write(self.__dataset.tail())

        self.analyze_manager.markdown("> Shape of data")
        pd_data_describe = self.__dataset.describe()
        data_row_count = len(self.__dataset)
        data_column_count = len(self.__dataset.columns)
        number_of_missing_values = self.__dataset.isnull().sum().sum()
        number_of_not_missing_values = self.__dataset.notnull().sum().sum()
        percentage_of_missing_values = (number_of_missing_values / (number_of_missing_values + number_of_not_missing_values)) * 100

        self.analyze_manager.markdown(f"""
            - There are **{data_row_count}** rows in your dataset
            - There are **{data_column_count}** columns in your dataset
            - **{round(percentage_of_missing_values, 2)}%** of the cell values are missing ({number_of_missing_values} missing values)
            
        """)


    def __LLM_Analysis(self):
        df = pd.DataFrame(self.__dataset)
        pAI = SmartDataframe(df, config={"verbose": True, "llm": self.llm})

        llm_analysis_response = pAI.chat("What is the context of this dataset, and what is it trying to find/track based on the context of the dataset? Also format your responsee by adding ** before and after key pieces of information")
        self.analyze_manager.markdown(f"### Short summary of the dataset:")
        self.analyze_manager.markdown(f"{llm_analysis_response}")
        
        self.analyze_manager.markdown("""
                    > Statistical Analysis of the dataset  
                    > Includes: min, max, mean, std, count, and more
        """)
        llm_analysis_response = pAI.chat("What are the quantitative columns in the dataset, return the column names comma separated: column_1, column_2, column_3, ...")
        #For each quantitative column, use pd to find the min, max, mean, std, count, and then add it to the dataframe
        pd_df = []
        quantitative_columns = llm_analysis_response.split(",")
        for column in quantitative_columns:
            pd_df.append(self.__dataset[column].describe())
        
        llm_analysis_response = pd.concat(pd_df, axis=1)

        try:
            self.analyze_manager.table(llm_analysis_response)
        except StreamlitAPIException as e:
            #Raise error to sentry to see what what type of data caused the error
            pass
            try:
                self.analyze_manager.write(llm_analysis_response)
            except NoCodeFoundError as e:
                self.analyze_manager.markdown(llm_analysis_response)
        except NoCodeFoundError as e:
            self.analyze_manager.markdown(llm_analysis_response)

    
    def ask(self, question):
        chat_manager = print_to_chat_response()
        df = pd.DataFrame(self.__dataset)
        pAI = SmartDataframe(df, config={"verbose": True, "llm": self.llm})

        pAI.chat("I want to ask a question about the dataset")
        llm_analysis_response = pAI.chat(question)
        
        with chat_manager.chat_message("Assistant"):
            chat_manager.write(self.print_reponse_in_yield_delay(llm_analysis_response))

