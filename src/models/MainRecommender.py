from BaseModel import RecommendationModelInterface
from typing import Dict


class RecommendModel(RecommendationModelInterface):
    def __init__(self, domain_recommender: RecommendationModelInterface,
                 atom_models_dict: Dict[str, RecommendationModelInterface]):
        '''
        domain_recommender - Модель, которая выбирает из какого домена тянуть рекомендацию
        на основе предпочтений пользователя

        atom_models_dict - словарь вида {'rec_type': RecModel}, где rec_type - название домена,
        RecModel - атомарная модель рекомендации по этому домену

        '''

        super().__init__()
        self.domain_recommender = domain_recommender
        self.atom_models_dict = atom_models_dict

    def fit(self):
        pass

    def recommend(self, user_history, n_to_recommend, *args, **kwargs):

        recommendation = self.domain_recommender.recommend(user_history, n_to_recommend)

        for rec_type, rec_model in self.atom_models_dict.items():
            mask = (recommendation == rec_type)
            n_in_mask = sum(mask)
            recommendation[mask] = rec_model.recommend(user_history, n_in_mask)

        return recommendation
