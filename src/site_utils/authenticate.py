from pathlib import Path
import yaml
from yaml.loader import SafeLoader

import streamlit as st


class Authenticate:
    """
    This class will create login, logout, register user widgets.
    """
    def __init__(self, user_data_path: Path):
        self.user_data_path = user_data_path

        if 'user' not in st.session_state:
            st.session_state['user'] = None
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'favorites' not in st.session_state:
            st.session_state['favorites'] = []

    def login(self):

        login_form = st.form('Login')

        login_form.subheader('Вход')
        user = login_form.text_input('Username')
        password = login_form.text_input('Password', type='password')

        if login_form.form_submit_button('Login'):
            self._check_credentials(user, password)

        return (st.session_state['user'],
                st.session_state['authentication_status'],
                st.session_state['favorites'])

    def _check_credentials(self, user, password):
        """
        Checks the validity of the entered credentials.
        """

        with open(str(self.user_data_path)) as file:
            user_data = yaml.load(file, Loader=SafeLoader)

        if user in user_data:
            if str(user_data[user]['password']) == password:
                st.session_state['user'] = user
                st.session_state['authentication_status'] = True
                st.session_state['favorites'] = user_data[user]['favorites'].split(', ')
                st.experimental_rerun()
            else:
                st.session_state['authentication_status'] = False
                st.warning(f'Неверный пароль')
        else:
            st.warning(f'Такого пользователя нет')

    def register_user(self):
        """
        Creates a password reset widget.
        """
        with open(str(self.user_data_path)) as file:
            user_data = yaml.load(file, Loader=SafeLoader)

        register_user_form = st.form('Register user')
        register_user_form.subheader('Регистрация')
        new_user = register_user_form.text_input('Name')
        new_password = register_user_form.text_input('Password', type='password')
        new_password_repeat = register_user_form.text_input('Repeat password', type='password')

        if register_user_form.form_submit_button('Register'):
            if new_user and new_password:
                if new_user not in user_data:
                    if new_password == new_password_repeat:
                        self._register_credentials(new_user, new_password)

                        st.session_state['user'] = new_user
                        st.session_state['authentication_status'] = True
                        st.session_state['favorites'] = ''

                        st.experimental_rerun()

    def _register_credentials(self, new_user, new_password):
        new_user_data = {new_user: {'password': new_password,
                                    'favorites': ''}}
        with open(str(self.user_data_path), 'a') as file:
            yaml.dump(new_user_data, file, default_flow_style=False)
