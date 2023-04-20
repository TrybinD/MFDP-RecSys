import numpy as np
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import CountVectorizer

from .BaseModel import RecommendationModelInterface


class TagsBasedRecommender(RecommendationModelInterface):

    def fit(self, content_data, *args, **kwargs):
        ''' В content_data должны быть столбцы item и tags'''

        self.items = content_data.item.values

        vectorizer = CountVectorizer(tokenizer=lambda x: x.split(','))
        posts_tag_matrix = vectorizer.fit_transform(content_data['tags'])

        posts_tag_matrix = normalize(posts_tag_matrix, norm='l2', axis=1)

        self.simularity = posts_tag_matrix * posts_tag_matrix.T

    def recommend(self, user_history, n_to_recommend, mode='probabilistic', *args, **kwargs):
        posts_id = np.where(np.isin(self.items, user_history))[0]
        a = np.array(self.simularity[posts_id].sum(axis=0))
        if mode == 'probabilistic':
            recs = np.random.choice(self.items, p=(a[0]/a.sum()),
                                    size=(n_to_recommend+len(posts_id)),
                                    replace=False)[::-1]
        elif mode == 'deterministic':
            recs = a.argsort()[0][-(n_to_recommend+len(posts_id)):]
            recs = self.items[recs]
        recs = recs[~np.isin(recs, user_history)][-n_to_recommend:]
        return recs[::-1]