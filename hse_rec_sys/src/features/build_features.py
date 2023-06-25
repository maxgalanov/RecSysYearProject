import pandas as pd
import numpy as np
import sqlite3
from sklearn.preprocessing import LabelEncoder, MinMaxScaler


def get_data_for_train():
    query_1 = f"""SELECT *
                    FROM new_users_added
                    """
    query_2 = f"""SELECT *
                    FROM song_features
                    """

    conn = sqlite3.connect("../data/music.db")
    cur = conn.cursor()
    # Выполняем запрос
    train_users = pd.DataFrame(
        cur.execute(query_1).fetchall(), columns=["user_id", "song_id", "play_count"]
    )
    item_features_train = pd.DataFrame(
        cur.execute(query_2).fetchall(),
        columns=[
            "song_id",
            "title",
            "release",
            "artist_name",
            "year",
            "genre",
            "artist_country",
            "artist_city",
        ],
    )

    # Закрываем соединение с базой данных
    conn.close()

    # Датасет с интеракциями user-song
    interactions_train = train_users[["user_id", "song_id"]]
    # Целевая переменная
    sample_weight_train = np.log2(train_users["play_count"] + 1)
    # Датасет с признаками песен
    item_features_train = item_features_train.drop(["title"], axis=1).drop_duplicates()

    # Кодируем признаки
    realese_encoder = LabelEncoder()
    artist_name_encoder = LabelEncoder()
    artist_country_encoder = LabelEncoder()
    artist_city_encoder = LabelEncoder()
    genre_encoder = LabelEncoder()

    item_features_train["release"] = realese_encoder.fit_transform(
        item_features_train["release"]
    )
    item_features_train["artist_name"] = artist_name_encoder.fit_transform(
        item_features_train["artist_name"]
    )
    item_features_train["artist_country"] = artist_country_encoder.fit_transform(
        item_features_train["artist_country"]
    )
    item_features_train["artist_city"] = artist_city_encoder.fit_transform(
        item_features_train["artist_city"]
    )
    item_features_train["genre"] = genre_encoder.fit_transform(
        item_features_train["genre"]
    )

    # Нормируем признаки
    scaler = MinMaxScaler()
    scaled_cols = item_features_train.columns[1:]
    item_features_train[scaled_cols] = scaler.fit_transform(
        item_features_train[scaled_cols]
    )

    return interactions_train, sample_weight_train, item_features_train
