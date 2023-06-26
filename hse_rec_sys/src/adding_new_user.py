import streamlit as st
import requests


# Функция для получения или создания словаря состояния сеанса
def get_session_state():
    if "session_state" not in st.session_state:
        st.session_state["session_state"] = {}
    return st.session_state["session_state"]


# Функция для получения любимых жанров
def get_genres():
    response = requests.get("http://127.0.0.1:8000/genres")
    if response.status_code == 200:
        genres = response.json()
        return genres
    else:
        st.error("Ошибка при получении жанров")


# Функция для получения популярных песен по выбранному жанру
def get_popular_songs(genre):
    session_state = get_session_state()
    if genre not in session_state:
        response = requests.get(f"http://127.0.0.1:8000/popular-songs/{genre}")
        if response.status_code == 200:
            songs = response.json()
            session_state[genre] = songs
        else:
            st.error("Ошибка при получении популярных песен")
    else:
        songs = session_state[genre]
    return songs


# Функция для добавления нового пользователя
def add_new_user(user_ratings):
    response = requests.post("http://127.0.0.1:8000/add-user", json=user_ratings)
    if response.status_code == 200:
        new_user_id = response.json()  # Получаем new_user_id из ответа
        st.success(f"Новый пользователь успешно добавлен. ID: {new_user_id}")
    else:
        st.error("Ошибка при добавлении нового пользователя")


# Функция для страницы добавления нового пользователя
def add_user():
    session_state = get_session_state()
    if "user_ratings" not in session_state:
        session_state["user_ratings"] = {}

    st.title("Добавить нового пользователя")

    genres = get_genres()
    selected_genres = st.multiselect("Выберите любимые жанры", genres)

    for genre in selected_genres:
        st.subheader(f"Популярные песни в жанре: {genre}")
        songs = get_popular_songs(genre)
        for song_id, song_title in songs:
            rating = st.slider(f"Оцените песню '{song_title}'", 1, 9)
            session_state["user_ratings"][song_id] = rating

    if st.button("Добавить пользователя"):
        add_new_user(session_state["user_ratings"])
