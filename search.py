import streamlit as st

from src.site_utils.site_components import Page, create_item_card


class SearchPage(Page):

    def render(self, data_dict: dict, **kwargs):

        self.update_favorites()

        st.title('Search')

        text_to_search = st.text_input('Введите название или автора')


        if text_to_search:
            finds = self.search_in_data(text_to_search, data_dict)


            self.show_finds(finds, data_dict)

    @staticmethod
    def search_in_data(text_to_search, data_dict):

        finds = []


        # Поиск в Книгах по названию
        finds.extend(
            (data_dict['b'][data_dict['b']['Book-Title']
                .str.lower()
                .str.contains(text_to_search.lower())])['ISBN'].values
        )
        # Поиск в Книгах по автору
        finds.extend(
            (data_dict['b'][data_dict['b']['Book-Author']
                .str.lower()
                .str.contains(text_to_search.lower())])['ISBN'].values
        )


        # Поиск в фильмах по названию
        finds.extend(
            (data_dict['f'][data_dict['f']['title']
                .str.lower()
                .str.contains(text_to_search.lower())])['item_id'].values
        )

        # Поиск в фильмах по автору
        finds.extend(
            (data_dict['f'][data_dict['f']['directors'].fillna('-')
                .str.lower()
                .str.contains(text_to_search.lower())])['item_id'].values
        )


        # Поиск в сериалах по названию
        finds.extend(
            (data_dict['s'][data_dict['s']['title']
                .str.lower()
                .str.contains(text_to_search.lower())])['item_id'].values
        )

        # Поиск в сериалах по автору
        finds.extend(
            (data_dict['s'][data_dict['s']['directors'].fillna('-')
                .str.lower()
                .str.contains(text_to_search.lower())])['item_id'].values
        )

        # Поиск в статьях по названию
        finds.extend(
            (data_dict['h'][data_dict['h']['title']
                .str.lower()
                .str.contains(text_to_search.lower())])['id'].values
        )

        return finds


    @staticmethod
    def show_finds(finds, data_dict, n_cards_per_row=2):

        for i, item in enumerate(finds):
            n_col = i % n_cards_per_row

            if n_col == 0:
                st.write("---")
                cols = st.columns(n_cards_per_row)

            with cols[n_col]:
                card = create_item_card(item, data_dict)

                card.button('Добавить в избранное', key=f'add_item_{item}')

    @staticmethod
    def update_favorites():
        for i, flag in st.session_state.items():
            if i.startswith('add_item_'):  # Ключи кнопок для добавления должны начинаться с add_item_
                if flag:
                    st.session_state['favorites'].append(i[9:])
