import os
from PIL import Image
from pathlib import Path

import pandas as pd

import streamlit as st
from streamlit_option_menu import option_menu

from src.site_utils.data_extract import read_data
from src.site_utils.site_components import Sidebar

from new_recommendation import NewRecommendationPage
from favorites import FavoritesPage
from search import SearchPage


if __name__ == '__main__':

    # Настраиваем возможные странички
    pages_dict = {'Новые рекомендации': NewRecommendationPage(),
                  'Избранное': FavoritesPage(),
                  'Поиск': SearchPage()}

    # Настраиваем добавленное в избранное - изменится с аутентификацией
    if 'favorites' not in st.session_state:
        st.session_state['favorites'] = []

    # Загружаем изображения
    icon = Image.open(Path('utils/logo.jpeg'))

    # Настраиваем параметры страницы
    st.set_page_config(layout="wide", page_title='LifeStyle', page_icon=icon)
    st.markdown("""
                    <style>
                           .css-hxt7ib {
                            padding-top: 1rem;
                            padding-left: 1rem;
                            padding-right: 1rem;
                        }
                    </style>
                    """, unsafe_allow_html=True)



    # Считываем данные из "БД"
    books_data_path = Path('data/books_bd.parquet')
    books_data = read_data(books_data_path)

    films_data_path = Path('data/films_bd.parquet')
    films_data = read_data(films_data_path)

    series_data_path = str(Path('data/series_bd.parquet'))
    series_data = read_data(series_data_path)

    habr_data_path = str(Path('data/habr_posts.parquet'))
    habr_data = read_data(habr_data_path)

    data_dict = {'b': books_data,
                 'f': films_data,
                 's': series_data,
                 'h': habr_data}


    # Создаем sidebar
    sidebar = Sidebar(list(pages_dict.keys()), icon)

    # Отрисовываем выбранную страничку
    pages_dict[sidebar.page].render(data_dict)
