from pathlib import Path
import pickle

import streamlit as st
import pandas as pd

from src.site_utils.site_components import Page, create_item_card, create_time_based_domain_filter
from src.models.MainRecommender import RecommendModel
from src.models.ContentBasedRecommenders import TagsBasedRecommender
from src.models.DomainRecommender import AdaptiveDomainRecommender


class NewRecommendationPage(Page):
    def __init__(self):
        # Загружаем модели для рекомендации фильмов, книг и сериалов
        models_path = Path('src/models/models_storage')

        with open(models_path / 'books_model_1.pickle', 'rb') as f:
            books_model = pickle.load(f)

        with open(models_path / 'films_model_1.pickle', 'rb') as f:
            films_model = pickle.load(f)

        with open(models_path / 'series_model.pickle', 'rb') as f:
            series_model = pickle.load(f)

        # Обучаем модель рекомендации статей
        posts_model = TagsBasedRecommender()
        posts_model.fit(pd.read_parquet(Path('data/habr_posts.parquet')).rename({'id': 'item'}, axis=1))

        # Инициализируем модель для доменов
        domain_model = AdaptiveDomainRecommender(['b', 'f', 's', 'h'])

        # Собираем полную модель
        self.model = RecommendModel(domain_model,
                                    {'b': books_model,
                                     'f': films_model,
                                     's': series_model,
                                     'h': posts_model})

    def render(self, data_dict: dict, **kwargs):

        self.update_favorites()

        st.title('New recommendation')

        domains = create_time_based_domain_filter()

        recommendations = self.model.recommend(st.session_state['favorites'], 20,
                                               select_only=domains)

        self.show_results(recommendations, data_dict)

    @staticmethod
    def update_favorites():
        for i, flag in st.session_state.items():
            if i.startswith('add_item_'):  # Ключи кнопок для добавления должны начинаться с add_item_
                if flag:
                    if st.session_state['favorites']:
                        st.session_state['favorites'].append(i[9:])
                    else:
                        st.session_state['favorites'] = [i[9:]]

    @staticmethod
    def show_results(recommends, data_dict, n_cards_per_row=3):

        for i, item in enumerate(recommends):

            n_col = i%n_cards_per_row

            if n_col == 0:
                st.write("---")
                cols = st.columns(n_cards_per_row)

            with cols[n_col]:
                card = create_item_card(item, data_dict)

                card.button('Добавить в избранное', key=f'add_item_{item}')
