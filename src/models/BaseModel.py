from abc import ABC, abstractmethod

import numpy as np


class RecommendationModelInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def fit(self, *args, **kwargs):
        pass

    @abstractmethod
    def recommend(self, *args, **kwargs):
        pass


class BaseRecommendModel(RecommendationModelInterface):
    def fit(self, interaction_data, top_size=100, *args, **kwargs):
        if 'history' in kwargs:
            self.history = kwargs['history']['item'].str.split(', ').to_dict()
        else:
            self.history = {}

        top = (interaction_data
               .groupby(['source', 'item'])
               .agg({'interaction_type': ['count', 'sum']}))

        self.top_dict = {i: {j: (top
                                 .sort_values(('interaction_type', j), ascending=False)
                                 .loc[i]
                                 .index.values[:top_size]) for j in ['sum', 'count']} for i in ['books', 'kion']}

        ratio = top.groupby(level=0).agg('sum')['interaction_type']

        self.ratio_dict = {i: ratio[i].values/ratio[i].sum() for i in ['sum', 'count']}

    def recommend(self, user, n_to_recommend,
                  top_type='sum', ratio_type='count', use_history=True, user_history=None,
                  *args, **kwargs):

        recommendation = np.random.choice(['books', 'kion'],
                                          size=n_to_recommend,
                                          p=self.ratio_dict[ratio_type]).astype(object)
        if not use_history:
            mask = (recommendation == 'books')
            n_books = sum(mask)
            n_kion = n_to_recommend - n_books
            recommendation[mask] = self.top_dict['books'][top_type][:n_books]
            recommendation[~mask] = self.top_dict['kion'][top_type][:n_kion]
            return recommendation

        if user_history is None:
            user_history = self.history.get(user, [])
        mask = (recommendation == 'books')
        n_books = sum(mask)
        n_kion = n_to_recommend - n_books
        recommendation[mask] = (self.top_dict['books'][top_type][~np.isin(self.top_dict['books'][top_type],
                                                                          user_history)][:n_books])
        recommendation[~mask] = (self.top_dict['kion'][top_type][~np.isin(self.top_dict['kion'][top_type],
                                                                          user_history)][:n_kion])
        return recommendation

