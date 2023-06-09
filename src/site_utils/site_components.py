from abc import ABC, abstractmethod

import streamlit as st
from streamlit_option_menu import option_menu

from src.site_utils.authenticate import Authenticate


class Sidebar:
    def __init__(self, pages_names: list, icon: object, side_bar_name='LifeStyle'):
        with st.sidebar:
            if icon:
                st.image(icon, width=200)
            st.title(side_bar_name)
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


def create_time_based_domain_filter():

    available_time = st.selectbox('Сколько у Вас свободного времени?',
                                  ['Много - можно фильм посмотреть или что-то почитать',
                                   'Не очень много - может на одну серию хватит',
                                   'Еду в метро - хотел бы что-то почитать',
                                   'Буквально 15 минут - хватит на статью'])

    selected_domains = {'Много - можно фильм посмотреть или что-то почитать': ['b', 'f', 's', 'h'],
                        'Не очень много - может на одну серию хватит': ['s', 'b', 'h'],
                        'Еду в метро - хотел бы что-то почитать': ['b', 'h'],
                        'Буквально 15 минут - хватит на статью': ['h']}[available_time]

    selected_domains = additional_choice(preselected=selected_domains)

    return selected_domains


def additional_choice(preselected=()):
    domains = ['b', 'f', 's', 'h']
    if preselected:
        domains_mask = [d in preselected for d in domains]
    else:
        domains_mask = [True for d in domains]

    with st.expander('Дополнительный выбор'):
        cols = st.columns(4)
        for i, (col, domain_name) in enumerate(zip(cols, ['Книги', 'Фильмы', 'Сериалы', 'Статьи'])):
            domains_mask[i] = col.checkbox(domain_name, value=domains_mask[i])

    return [d for d, mask in zip(domains, domains_mask) if mask]


def create_authenticate(user_data_path):
    auth = Authenticate(user_data_path)

    if not st.session_state['authentication_status']:
        auth_sidebar = Sidebar(['Вход', 'Регистрация'], None, 'Вход или Регистрация')

        if auth_sidebar.page == "Вход":
            auth.login()
        elif auth_sidebar.page == "Регистрация":
            auth.register_user()
