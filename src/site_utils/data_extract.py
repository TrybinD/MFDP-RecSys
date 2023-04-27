import pandas as pd

import streamlit as st


@st.cache_data
def read_data(data_path):
    ''' Принимает на вход путь до данных, необходимых для сайта'''

    return pd.read_parquet(data_path)
