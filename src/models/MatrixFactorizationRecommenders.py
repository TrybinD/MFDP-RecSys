import numpy as np
from scipy import sparse

from implicit.als import AlternatingLeastSquares
from lightfm import LightFM

from .BaseModel import RecommendationModelInterface


class ALSBasedRecommender(RecommendationModelInterface):

    def fit(self, interaction_data, *args, **kwargs):


        self.rows, r_pos = np.unique(interaction_data['user'].values, return_inverse=True)
        self.cols, c_pos = np.unique(interaction_data['item'].values, return_inverse=True)

        sparse_interactions = sparse.csc_matrix((interaction_data['rating'].values.astype(float),
                                                 (r_pos, c_pos)))

        self.model = AlternatingLeastSquares(**kwargs)
        self.model.fit(sparse_interactions.tocsr())

    def recommend(self, user_history, n_to_recommend, *args, **kwargs):
        book_id = np.where(np.isin(self.cols, user_history))[0]

        # Будем считать, что добавление в избранное == поставил 10 баллов книге
        sp_row = sparse.coo_matrix(([10 for _ in book_id], ([0 for _ in book_id], book_id)),
                                   shape=(1, len(self.cols)))
        recs = self.model.recommend(0, sp_row.tocsr(), recalculate_user=True, N=n_to_recommend)[0]

        recs = self.cols[recs]

        return recs


class LightFMBasedRecommender(RecommendationModelInterface):

    def fit(self, interaction_data, loss='warp', epochs=20, verbose=True, *args, **kwargs):


        self.rows, r_pos = np.unique(interaction_data['user'].values, return_inverse=True)
        self.cols, c_pos = np.unique(interaction_data['item'].values, return_inverse=True)

        self.sparse_interactions = sparse.csc_matrix((interaction_data['rating'].values.astype(float),
                                                 (r_pos, c_pos)), shape=(len(self.rows)+1,
                                                                         len(self.cols)))

        self.model = LightFM(loss=loss, **kwargs)
        self.model.fit(self.sparse_interactions.tocsr(), epochs=epochs, verbose=verbose, **kwargs)

    def recommend(self, user_history, n_to_recommend, epochs=10, verbose=True, *args, **kwargs):
        book_id = np.where(np.isin(self.cols, user_history))[0]

        # Будем считать, что добавление в избранное == поставил 10 баллов книге
        sp_row = sparse.coo_matrix(([10 for _ in book_id], ([0 for _ in book_id], book_id)),
                                   shape=(1, len(self.cols)))

        self.sparse_interactions[-1] = sp_row

        self.model.fit_partial(self.sparse_interactions, epochs=epochs, verbose=verbose)

        recs = self.model.predict([len(self.rows)],
                                  [i for i in range(len(self.cols))]).argsort()[-20:][::-1]

        recs = self.cols[recs]

        return recs
