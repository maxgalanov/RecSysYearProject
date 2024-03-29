import pickle
import sqlite3
import random
import asyncio
from fastapi import FastAPI
from src.models.rankfm_pred import get_rankfm_pred
from typing import List
from sqlite3 import OperationalError
from src.get_last_rankfm_model import find_latest_rankfm_model
from src.features.build_features import get_data_for_train
from src.models.train_model import train_rankfm_model

latest_model = find_latest_rankfm_model()

with open(f"src/models/{latest_model}", "rb") as f:
    rank_fm = pickle.load(f)

app = FastAPI()


@app.get("/recommend/{user_id}")
async def recommend(user_id: int) -> List[tuple]:
    # Получаем рекомендации для пользователя
    recommendations = get_rankfm_pred(rank_fm, user_id)

    # Проверка, что рекомендации уже получены и оценены
    check_query = f"""
    SELECT 
        nu.song_id
        ,sf.artist_name
        ,sf.title
        ,nu.play_count
    FROM 
        new_users_added nu
        left join
        song_features sf 
        using(song_id)
    WHERE true
        and user_id = {user_id}
        and song_id in ({str(recommendations).strip('[]')})
    """
    # Запрос для получения названий песен и исполнителей
    query = """SELECT song_id, artist_name, title, 0 as play_count
                FROM song_features 
                WHERE song_id IN ({})""".format(
        ",".join(["?"] * len(recommendations))
    )

    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("src/data/music.db")
    cur = conn.cursor()

    # Выполняем запрос и получаем результат
    try:
        check = cur.execute(check_query).fetchall()
    except OperationalError:
        print('Такого пользователя не существует.')
        check = []
    if check:
        result = check
    else:
        result = cur.execute(query, recommendations).fetchall()

    # Закрываем соединение с базой данных
    conn.close()

    # Возвращаем результат в виде списка кортежей ('song_id', 'исполнитель', 'трек', 'оценка')
    return result


@app.get("/genres")
async def get_genres() -> List[str]:
    # Запрос для получения топ-10 жанров
    query = """SELECT genre
                FROM (SELECT genre, count(*) as cnt
                      FROM song_features
                      GROUP BY genre
                      ORDER BY cnt desc)
                LIMIT 10"""

    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("src/data/music.db")
    cur = conn.cursor()

    # Выполняем запрос и получаем результат
    result = cur.execute(query).fetchall()
    genres = [genre[0] for genre in result]

    # Закрываем соединение с базой данных
    conn.close()

    return genres


@app.get("/popular-songs/{genre}")
async def get_popular_songs(genre: str) -> List[tuple]:
    # Запрос для получения топ-15 песен из жанра
    query = f"""SELECT s.song_id, s.title, s.artist_name, sum(play_count) as cnt
                FROM (SELECT song_id, artist_name, title
                      FROM song_features 
                      WHERE genre = '{genre}') s
                      INNER JOIN 
                      user_song_interaction u
                      ON s.song_id = u.song_id
                GROUP BY s.title, s.artist_name
                ORDER BY cnt desc
                LIMIT 15"""

    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("src/data/music.db")
    cur = conn.cursor()

    # Выполняем запрос и получаем результат
    result = cur.execute(query).fetchall()
    songs = [(song[0], song[1] + ", " + song[2]) for song in result]

    # Закрываем соединение с базой данных
    conn.close()
    random_songs = random.sample(songs, 3)
    return random_songs


@app.post("/add-user")
async def add_user(ratings: dict) -> int:
    # Запрос для получения max user_id
    query = """SELECT max(user_id) + 1
                FROM new_users_added"""

    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("src/data/music.db")
    cur = conn.cursor()

    new_user_id = cur.execute(query).fetchall()[0][0]

    for song_id, rating in ratings.items():
        cur.execute(
            f"""INSERT INTO new_users_added 
                                (user_id, song_id, play_count)
                                VALUES (?, ?, ?)""",
            (int(new_user_id), int(song_id), int(rating)),
        )

    # Закрываем соединение с базой данных
    conn.commit()
    conn.close()
    return new_user_id


@app.post("/get_feedback")
async def get_feedback(feedback: dict) -> None:
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("src/data/music.db")
    cur = conn.cursor()
    print(feedback)
    print(type(feedback))
    user_id = feedback["user_id"]

    for song_id, rating in feedback["ratings"].items():
        cur.execute(
            f"""INSERT INTO new_users_added 
                                (user_id, song_id, play_count)
                                VALUES (?, ?, ?)""",
            (int(user_id), int(song_id), int(rating)),
        )

    # Закрываем соединение с базой данных
    conn.commit()
    conn.close()
    return


@app.post("/train-model")
async def train_model() -> str:
    global rank_fm
    # Получаем данные для обучения модели
    interactions_train, sample_weight_train, item_features_train = get_data_for_train()

    # Обучаем модель RankFM и сохраняем в pickle
    print("rankfm training started...")

    loop = asyncio.get_event_loop()
    new_rankfm, name_new_rankfm = await loop.run_in_executor(None, train_rankfm_model, interactions_train,
                                                             item_features_train, sample_weight_train)

    rank_fm = new_rankfm
    print(f"The model has been successfully trained and saved to the file: {name_new_rankfm}")

    return f"The model has been successfully trained and saved to the file: {name_new_rankfm}"
