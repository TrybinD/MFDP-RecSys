import streamlit as st

from src.site_utils.site_components import Page, create_item_card, create_time_based_domain_filter


class FavoritesPage(Page):

    def render(self, data_dict: dict, **kwargs):

        st.title('Favorites')

        domains = create_time_based_domain_filter()

        self.show_favorites(st.session_state['favorites'], data_dict, select_only=domains)

    def show_favorites(self, favorites, data_dict, n_cards_per_row=1, select_only=None):

        if select_only is not None:
            favorites = [f for f in favorites if f[0] in select_only]

        for i, item in enumerate(favorites):
            n_col = i % n_cards_per_row

            if n_col == 0:
                st.write("---")
                cols = st.columns(n_cards_per_row)

            with cols[n_col]:
                card = create_item_card(item, data_dict)

                card.button('Удалить из избранного', key=f'drop_item_{item}',
                            on_click=self.drop_favorites, args=(item,))

    @staticmethod
    def drop_favorites(item):
        st.session_state['favorites'].remove(item)
