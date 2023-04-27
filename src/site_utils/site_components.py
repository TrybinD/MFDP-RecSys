from abc import ABC, abstractmethod

import streamlit as st
from streamlit_option_menu import option_menu


class Sidebar:
    def __init__(self, pages_names: list, icon: object):
        with st.sidebar:
            st.image(icon, width=200)
            st.title('LifeStyle')
            self.page = option_menu('Выберите лист', pages_names, menu_icon="table")


class Page(ABC):

    @abstractmethod
    def render(self, data_dict: dict, **kwargs):
        ''' data_dict: dict - Словарь со всеми таблицами, которые нужны для
        отображения информации о рекомендованном item'''
        pass


def create_item_card(item, data_dict):
    '''Возвращает контейнер-карточку item'''

    item_type = item[0]
    item_type_data = data_dict[item_type]

    container = st.container()

    with container:
        if item_type == 'b':
            render_books_card(item, item_type_data)

        elif item_type == 'f':
            render_film_series_card(item, item_type_data, 'film')

        elif item_type == 's':
            render_film_series_card(item, item_type_data, 'serial')

        elif item_type == 'h':
            render_habr_post(item, item_type_data)

    return container


def render_books_card(item, data):

    content = data.query('ISBN == @item')

    st.caption('book')
    st.markdown(f"**{content['Book-Title'].item()}**")
    st.write(content['Book-Author'].item())
    st.write(content['Year-Of-Publication'].item())
    st.image(content['Image-URL-M'].item())


def render_film_series_card(item, data, domain):

    content = data.query('item_id == @item')

    st.caption(domain)
    st.markdown(f"**{content['title'].item()}**")
    st.write(int(content['release_year'].item()))
    st.write(content['genres'].item())
    st.write(content['countries'].item())
    st.write(f'{int(content["age_rating"].item())}+')
    st.write(content['directors'].item())


def render_habr_post(item, data):

    content = data.query('id == @item')

    st.caption('habr')
    st.markdown(f"**{content['title'].item()}**")
    st.write(content['tags'].item())
    st.write(content['url'].item())

