from pathlib import Path
import pickle

import streamlit as st
import pandas as pd

model_path = Path('src/models')


def show_results(recommends, data_books, data_kion, N_cards_per_row = 4):

    for n_row, r in enumerate(recommends):
        i = n_row % N_cards_per_row
        if i == 0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")

        if r[0] == 'b':
            isbn = r[1:]
            content = data_books.query('ISBN == @isbn')
            if len(content) == 0:
                continue
            with cols[n_row % N_cards_per_row]:
                st.caption('book')
                st.markdown(f"**{content['Book-Title'].item()}**")
                st.image(content['Image-URL-M'].item())


                st.button('Добавить в избранное', key='b'+content['ISBN'].item())

        elif r[0] == 'k':
            item_id = int(r[1:])
            content = data_kion.query('item_id == @item_id')
            if len(content) == 0:
                continue
            with cols[n_row % N_cards_per_row]:
                st.caption(f'{content["content_type"].item()}')
                st.markdown(f"**{content['title'].item()}**")

                st.button('Добавить в избранное', key='k' + str(content['item_id'].item()))


with open(model_path/'base_model.pickle', 'rb') as f:
    model = pickle.load(f)

def new_recommendation(*args):
    data_books, data_kion = args

    for i, flag in st.session_state.items():
        if type(flag) is bool:
            if flag:
                st.session_state['favorites'].append(i)

    st.title('New recommendation')

    recommendations = model.recommend('', 20, top_type='count',
                                      user_history=st.session_state['favorites'])

    show_results(recommendations, data_books, data_kion)