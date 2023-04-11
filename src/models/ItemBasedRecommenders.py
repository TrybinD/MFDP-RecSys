import numpy as np
from scipy import sparse
from sklearn.preprocessing import normalize

from BaseModel import RecommendationModelInterface


class CosineDistanceRecommender(RecommendationModelInterface):

    def fit(self, interaction_data, *args, **kwargs):
        self.rows, r_pos = np.unique(interaction_data['user'].values, return_inverse=True)
        self.cols, c_pos = np.unique(interaction_data['item'].values, return_inverse=True)

        sparse_interactions = sparse.csc_matrix((interaction_data['rating'].values.astype(float), (r_pos, c_pos)))

        Pui = normalize(sparse_interactions, norm='l2', axis=1)

        self.simularity = Pui.T * Pui

    def recommend(self, user_history, n_to_recommend, mode='probabilistic', *args, **kwargs):
        book_id = np.where(np.isin(self.cols, user_history))[0]
        a = np.array(self.simularity[book_id].sum(axis=0))
        if mode == 'probabilistic':
            recs = np.random.choice(self.cols, p=(a[0]/a.sum()),
                                    size=(n_to_recommend+len(book_id)),
                                    replace=False)[::-1]
        elif mode == 'deterministic':
            recs = a.argsort()[0][-(n_to_recommend+len(book_id)):]
            recs = self.cols[recs]
        recs = recs[~np.isin(recs, user_history)][-n_to_recommend:]
        return recs[::-1]

