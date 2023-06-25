import pickle
import datetime
from rankfm.rankfm import RankFM


def train_rankfm_model(interactions_train, item_features_train, sample_weight_train):
    rank_fm = RankFM(
        factors=100,
        loss="warp",
        max_samples=100,
        alpha=0.05,
        sigma=0.1,
        learning_rate=0.1,
        learning_schedule="invscaling",
    )

    rank_fm.fit(
        interactions_train,
        item_features=item_features_train,
        sample_weight=sample_weight_train,
        epochs=100,
        verbose=False,
    )

    now = datetime.datetime.now()

    with open(f"./models/{now.strftime('%d_%m_%y_%H_%M')}_RankFm.pkl", 'wb') as f:
        pickle.dump(rank_fm, f)

    return rank_fm, f"{now.strftime('%d_%m_%y_%H_%M')}_RankFm.pkl"
