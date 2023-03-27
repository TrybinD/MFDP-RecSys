import os
from PIL import Image

import pandas as pd

import streamlit as st
from streamlit_option_menu import option_menu

from new_recommendation import new_recommendation
from favorites import favorites

pages_dict = {'Новые рекомендации': new_recommendation,
              'Избранное': favorites}


icon = Image.open(os.path.join('utils', 'logo.jpeg'))
st.set_page_config(layout="wide", page_title='LifeStyle', page_icon=icon)


@st.cache
def read_data():
    data_books = pd.read_parquet(os.path.join('data', 'books_bd.parquet'))
    data_kion = pd.read_parquet(os.path.join('data', 'kion_bd.parquet'))
    return data_books, data_kion


data_books, data_kion = read_data()


def create_sidebar():
    with st.sidebar:
        st.image(icon, width=200)
        st.title('LifeStyle')
        page = option_menu('Выберите лист', list(pages_dict.keys()), menu_icon="table")
    return page


if 'favorites' not in st.session_state:
    st.session_state['favorites'] = []


if __name__ == '__main__':
    st.markdown("""
                <style>
                       .css-hxt7ib {
                        padding-top: 1rem;
                        padding-left: 1rem;
                        padding-right: 1rem;
                    }
                </style>
                """, unsafe_allow_html=True)

    page = create_sidebar()
    pages_dict[page](data_books, data_kion)