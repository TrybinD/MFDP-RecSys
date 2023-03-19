from abc import ABC, abstractmethod

import pandas as pd
import numpy as np


class RecommendationModelInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def fit(self, interaction_data, *args, **kwargs):
        pass

    @abstractmethod
    def recommend(self, users, n_to_recommend, *args, **kwargs):
        pass


class BaseRecommendModel(RecommendationModelInterface):
    def fit(self, interaction_data, *args, **kwargs):
        if 'history' in kwargs:
            self.history = kwargs['history'].to_dict()['item']
        else:
            self.history = {}

        books_top = (interaction_data.query('sourse == "books"')['item']
                          .value_counts())
        films_top = (interaction_data.query('sourse == "books"')['item']
                          .value_counts())
        kion_top = (interaction_data.query('sourse == "books"')['item']
                          .value_counts())

        self.books_top = books_top.index.values
        self.films_top = films_top.index.values
        self.kion_top = kion_top.index.values

        self.bfk_rate = np.array([books_top.values.sum(), films_top.values.sum(), kion_top.values.sum()])
        self.bfk_rate = self.bfk_rate/self.bfk_rate.sum()

    def recommend_single(self, user, n_to_recommend, *args, **kwargs):
        bfk_counter = [0, 0, 0]
        recommendation = []
        user_history = self.history.get(user, '')
        i = 0
        while i <= n_to_recommend:
            source = np.random.choice(['books', 'films', 'kion'], p=self.bfk_rate)

            if source == 'books':
                rec = self.books_top[bfk_counter[0]]
                if rec not in user_history:
                    recommendation.append(rec)
                    i += 1
                    bfk_counter[0] += 1
            elif source == 'films':
                rec = self.books_top[bfk_counter[1]]
                if rec not in user_history:
                    recommendation.append(rec)
                    i += 1
                    bfk_counter[1] += 1
            elif source == 'kion':
                rec = self.books_top[bfk_counter[2]]
                if rec not in user_history:
                    recommendation.append(rec)
                    i += 1
                    bfk_counter[2] += 1

        return recommendation

    def recommend(self, users, n_to_recommend, *args, **kwargs):
        recommendations = []
        base_recommendations = self.recommend_single('', n_to_recommend)