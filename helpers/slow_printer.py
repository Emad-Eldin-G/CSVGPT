from time import sleep
import streamlit as st


#Use yield to print the text slowly
def slow_printer(text):
    for word in text.split():
        yield word + " "
        sleep(0.05)
