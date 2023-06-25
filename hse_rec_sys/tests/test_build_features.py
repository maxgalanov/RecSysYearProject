import numpy as np
from sklearn.preprocessing import MinMaxScaler
from hse_rec_sys.src.features.build_features import get_data_for_train


def test_get_data_for_train():
    interactions_train, sample_weight_train, item_features_train = get_data_for_train()

    # Проверяем, что получены не пустые DataFrame
    assert not interactions_train.empty
    assert not item_features_train.empty

    # Проверяем, что все необходимые столбцы присутствуют
    required_interactions_columns = ["user_id", "song_id"]
    required_item_features_columns = [
        "song_id",
        "release",
        "artist_name",
        "artist_country",
        "artist_city",
        "year",
        "genre",
    ]

    assert set(required_interactions_columns).issubset(interactions_train.columns)
    assert set(required_item_features_columns).issubset(item_features_train.columns)

    # Проверяем, что все значения в столбце 'play_count' больше или равны нулю
    assert (sample_weight_train >= 0).all()


def test_get_data_for_train_encoding_normalization():
    interactions_train, sample_weight_train, item_features_train = get_data_for_train()

    # Проверяем, что значения в столбце 'release' были успешно закодированы
    assert len(item_features_train["release"].unique()) == len(item_features_train)

    # Проверяем, что значения в остальных закодированных столбцах были успешно преобразованы в числовой формат
    for column in ["artist_name", "artist_country", "artist_city", "genre"]:
        assert item_features_train[column].dtype == np.int64

    # Проверяем, что значения в нормализованных столбцах находятся в диапазоне от 0 до 1
    scaler = MinMaxScaler()
    scaled_cols = item_features_train.columns[1:]
    scaled_features = scaler.fit_transform(item_features_train[scaled_cols])

    assert (scaled_features >= 0).all() and (scaled_features <= 1).all()
