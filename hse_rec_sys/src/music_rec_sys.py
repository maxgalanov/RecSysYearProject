import streamlit as st
import requests
from rec_songs_for_user import rec_song
from adding_new_user import add_user
from train_new_model import train_new_model

def main():
    pages = {
        "Рекомендации для пользователя": rec_song,
        "Добавить нового пользователя": add_user,
        "Получить новые рекомендации": train_new_model
    }

    st.sidebar.title('Навигация')
    selection = st.sidebar.radio("Перейти к:", list(pages.keys()))

    page = pages[selection]
    page()


if __name__ == '__main__':
    main()
