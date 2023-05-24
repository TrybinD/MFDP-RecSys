from abc import ABC, abstractmethod

import numpy as np


class RecommendationModelInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def fit(self, interaction_data, *args, **kwargs):
        pass

    @abstractmethod
    def recommend(self, user_history, n_to_recommend, *args, **kwargs):
        pass


class TopRecommender(RecommendationModelInterface):

    def fit(self, interaction_data, n_to_save=100, metric='count', *args, **kwargs):
        self. top_dict = (interaction_data
                          .groupby('item')
                          .agg({'rating': metric})
                          .sort_values('rating')
                          .iloc[-n_to_save:]
                          .to_dict()['rating'])

    def recommend(self, user_history, n_to_recommend, mode='probabilistic', *args, **kwargs):
        if mode == 'probabilistic':
            ratings = np.array(list(self.top_dict.values()))
            recs = np.random.choice(list(self.top_dict),
                                    p=ratings/ratings.sum(),
                                    size=(n_to_recommend+len(user_history)),
                                    replace=False)
        elif mode == 'deterministic':
            recs = np.array(sorted(self.top_dict,
                                   key=self.top_dict.get)[-(n_to_recommend+len(user_history)):])

        recs = recs[~np.isin(recs, user_history)][-n_to_recommend:]
        return recs[::-1]