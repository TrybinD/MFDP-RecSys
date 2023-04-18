import numpy as np
from scipy.stats import dirichlet

from .BaseModel import RecommendationModelInterface


class PopularDomainRecommender(RecommendationModelInterface):
    '''
     Модель рекомендации домена на основе популярности того или иного домена в данных по взаимодействию
     '''
    def fit(self, interaction_data, *args, **kwargs):  # TODO: Типизация DataFrame
        ''' interaction_data должен иметь столбцы 'source' '''

        self.ratio = interaction_data.source.value_counts(normalize=True).to_dict()

    def recommend(self, user_history, n_to_recommend, *args, **kwargs):
        return np.random.choice(list(self.ratio.keys()),
                                p=list(self.ratio.values()),
                                size=(n_to_recommend,)).astype('<U20')


class AdaptiveDomainRecommender(RecommendationModelInterface):
    def __init__(self, domains: list,
                 prior_alpha=None):
        super().__init__()
        self.domains = domains
        self.prior_alpha = prior_alpha if not None else [1 for _ in domains]

    def fit(self, interaction_data, *args, **kwargs):
        pass

    def recommend(self, user_history, n_to_recommend, mode='bayesian', *args, **kwargs):
        posterior_alpha = self.prior_alpha.copy()
        for i, domain in enumerate(self.domains):
            for item in user_history:
                if item[0] == domain[0]:  # Код домена и его названия начинаются с одной буквы
                    posterior_alpha[i] += 1

        if mode == 'bayesian':
            p = dirichlet(posterior_alpha).rvs()[0]
        elif mode == 'frequency':
            p = np.array(posterior_alpha)/sum(posterior_alpha)

        return np.random.choice(self.domains,
                                p=p,
                                size=(n_to_recommend,)).astype('<U20')
