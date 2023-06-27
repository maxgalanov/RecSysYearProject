import streamlit as st
import requests


def train_model():
    url = "http://backend:8000/train-model"
    response = requests.post(url)
    if response.status_code == 200:
        st.success("Модель успешно обучена и сохранена!")
    else:
        st.error("Ошибка при обучении модели")


def train_new_model():
    st.title("Получить новые рекомендации")
    if st.button("Обучить модель"):
        st.text("Обучение модели началось...")
        train_model()
    return
