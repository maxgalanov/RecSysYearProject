import streamlit as st
import requests
import pandas as pd


# Функция для получения или создания словаря состояния сеанса
def get_session_state():
    if "session_state" not in st.session_state:
        st.session_state["session_state"] = {}
    return st.session_state["session_state"]


def recommend_songs(num):
    session_state = get_session_state()
    if "df" not in session_state:
        url = f"http://127.0.0.1:8000/recommend/{num}"
        res = requests.get(url)
        try:
            ans = res.json()
        except requests.exceptions.JSONDecodeError:
            return pd.DataFrame()
        data = []
        for item in ans:
            song_id = item[0]
            author = item[1]
            song = item[2]
            rating = item[3]
            data.append([str(int(song_id)), author, song, rating])

        df = pd.DataFrame(data, columns=["song_id", "artist", "song", "rating"])
        return df
    else:
        df = session_state["df"]
        return df


def get_feedback(feedback):
    url = "http://127.0.0.1:8000/get_feedback"
    response = requests.post(url, json=feedback)
    if response.status_code == 200:
        st.success("Оценки пользователя успешно добавлены")
    else:
        st.error("Ошибка при добавлении оценок пользователя")


def rec_song():
    session_state = get_session_state()
    if "user_ratings" not in session_state:
        session_state["user_ratings"] = {}

    st.title("Введите id пользователя")
    title = st.text_input("id")
    if st.button("Ok"):
        assert title.lstrip("-+").isdigit(), "Id должен быть целым числом"
        session_state["num"] = int(title)
        assert session_state["num"] >= 0, "Id должен быть неотрицательным"
        session_state["df"] = recommend_songs(session_state["num"])

    if "df" in session_state:
        if "feedback" not in session_state:
            if session_state["df"]['rating'].any() == 0:
                st.dataframe(session_state["df"][['artist', 'song']])
            elif session_state["df"].empty:
                st.error("Такого пользователя не существует.")
                st.session_state["session_state"] = {}
                return
            session_state["feedback"] = {}
            session_state["feedback"]["user_id"] = session_state["num"]
        for index, row in session_state["df"].iterrows():
            song_id = row["song_id"]
            author = row["artist"]
            song = row["song"]
            if row["rating"] == 0:
                rating = st.slider(f"Оцените песню '{song}' от '{author}'", 1, 9)
                session_state["user_ratings"][song_id] = rating
            else:
                st.dataframe(session_state["df"][['artist', 'song', 'rating']])
                st.success("Все рекомендации уже оценены. Новые скоро появятся :)")
                # requests.post("http://127.0.0.1:8000/train-model")
                break
        session_state["feedback"]["ratings"] = session_state["user_ratings"]

        if session_state["feedback"]["ratings"]:
            if st.button("Добавить оценки пользователя"):
                get_feedback(session_state["feedback"])
                st.session_state["session_state"] = {}
        else:
            st.session_state["session_state"] = {}
    return
