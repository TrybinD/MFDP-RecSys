import yaml
from yaml.loader import SafeLoader

import pandas as pd
import streamlit as st


@st.cache_data
def read_data(data_path):
    ''' Принимает на вход путь до данных, необходимых для сайта'''

    return pd.read_parquet(data_path)


def reload_favorites(user, favorites, user_data_path):
    with open(str(user_data_path), 'r') as file:
        user_data = yaml.load(file, Loader=SafeLoader)

    user_data[user]['favorites'] = ', '.join(favorites)

    with open(str(user_data_path), 'w') as file:
        yaml.dump(user_data, file, default_flow_style=False)
