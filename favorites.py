import streamlit as st


def favorites(*args, N_cards_per_row = 1):
    data_books, data_kion = args
    st.title('Favorites')

    for n_row, r in enumerate(st.session_state['favorites']):
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


        elif r[0] == 'k':
            item_id = int(r[1:])
            content = data_kion.query('item_id == @item_id')
            if len(content) == 0:
                continue
            with cols[n_row % N_cards_per_row]:
                st.caption(f'{content["content_type"].item()}')
                st.markdown(f"**{content['title'].item()}**")

