import streamlit as st

from src.site_utils.site_components import Page, create_item_card


class FavoritesPage(Page):

    def render(self, data_dict: dict, **kwargs):

        st.title('Favorites')

        self.show_favorites(st.session_state['favorites'], data_dict)

    @staticmethod
    def show_favorites(favorites, data_dict, n_cards_per_row=1):

        for i, item in enumerate(favorites):
            n_col = i % n_cards_per_row

            if n_col == 0:
                st.write("---")
                cols = st.columns(n_cards_per_row)

            with cols[n_col]:
                card = create_item_card(item, data_dict)
