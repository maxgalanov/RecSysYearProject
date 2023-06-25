import streamlit as st
import requests
import pandas as pd


def recommend_songs(num):
    url = f'http://127.0.0.1:8000/recommend/{num}'
    res = requests.get(url)
    ans = res.json()

    data = []
    for item in ans:
        song_id = item[0]
        author = item[1]
        song = item[2]
        data.append([str(int(song_id)), author, song])

    df = pd.DataFrame(data, columns=['song_id', 'artist', 'song'])
    return df


def rec_song():
    st.title("Введите id пользователя")
    title = st.text_input('id')
    if st.button('Ok'):
        assert title.lstrip('-+').isdigit(), 'Id должен быть целым числом'
        num = int(title)
        assert num >= 0, 'Id должен быть неотрицательным'
        df = recommend_songs(num)
        st.dataframe(df)
    return
