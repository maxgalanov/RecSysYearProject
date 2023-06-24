import pandas as pd
import pickle
from rankfm.rankfm import RankFM
from src.features.build_features import get_data_for_train


interactions_train, sample_weight_train, item_features_train = get_data_for_train()

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

with open('./models/RankFm_new.pkl', 'wb') as f:
    pickle.dump(rank_fm, f)
