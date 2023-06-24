import streamlit as st
import json
import requests
import pandas as pd
import numpy as np

def recommend_songs(num):
    res = requests.get(url=f'http://backend:8000/recommend/{num}')
    ans = res.text
    ans = ans.replace('[', '').replace(']', '')
    x = ans.split(",")
    data = []
    for i in range(len(x)//2):
        author = x[2*i]
        song = x[2*i + 1]
        a = [author, song]
        data.append(a)
    df = pd.DataFrame(data, columns=['Автор', 'Песня'])
    return df

st.title("Введите id пользователя")
title = st.text_input('id')
if st.button('Ok'):
    assert title.lstrip('-+').isdigit(), 'Id должен быть целым числом'
    num = int(title)
    assert num >= 0, 'Id должен быть неотрицательным'
    df = recommend_songs(num)
    st.dataframe(df)


# Функция для получения списка доступных жанров
def get_genres():
    res = requests.get(url='http://backend:8000/genres')
    genres = res.json()
    return genres

# Функция для получения списка популярных песен для указанного жанра
def get_popular_songs(genre):
    res = requests.get(url=f'http://backend:8000/popular-songs/{genre}')
    songs = res.json()
    return songs

st.title("Добавление нового пользователя")

# Шаг 1: Выбор любимых жанров
if 'song_ratings' not in st.session_state:
    genres = get_genres()
    selected_genres = st.multiselect('Выберите любимые жанры', genres)

# Шаг 2: Оценка песен для выбранных жанров
if 'song_ratings' not in st.session_state:
    st.session_state.song_ratings = {}

for genre in selected_genres:
    st.subheader(f"Жанр: {genre}")
    popular_songs = get_popular_songs(genre)
    for song in popular_songs:
        rating = st.slider(f"Оцените песню '{song}'", min_value=1, max_value=9, key=song)
        st.session_state.song_ratings[song] = rating

# Шаг 3: Отправка оценок в базу данных
if st.button('Добавить пользователя'):
    song_ratings = st.session_state.song_ratings
    # Здесь вы можете добавить логику для отправки оценок в базу данных
    # Пример: отправка POST-запроса с данными о пользователе и его оценками
    payload = {
        'user_id': 123,  # Замените на реальный ID пользователя
        'ratings': song_ratings
    }
    res = requests.post(url='http://backend:8000/add-user', json=payload)
    if res.status_code == 200:
        st.success('Пользователь успешно добавлен')
    else:
        st.error('Произошла ошибка при добавлении пользователя')
