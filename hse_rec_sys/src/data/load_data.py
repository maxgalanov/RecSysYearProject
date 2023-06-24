import pandas as pd
from sqlalchemy.orm import Session

from create_database import SongFeatures, UserSongInteraction, SessionLocal


def load_song_features_data(session: Session):
    df = pd.read_csv("item_features_rankfm.csv")
    for index, row in df.iterrows():
        song = SongFeatures(
            song_id=row["song_id"],
            title=row["title"],
            release=row["release"],
            artist_name=row["artist_name"],
            year=row["year"],
            genre=row["genre"],
            artist_country=row["artist_country"],
            artist_city=row["artist_city"],
        )
        session.add(song)
    session.commit()


def load_user_song_interaction_data(session: Session):
    df = pd.read_csv("user_song_interaction_2.csv")
    for index, row in df.iterrows():
        interaction = UserSongInteraction(
            user_id=row["user_id"],
            song_id=row["song_id"],
            play_count=row["play_count"],
        )
        session.add(interaction)
    session.commit()


if __name__ == "__main__":
    session = SessionLocal()
    load_user_song_interaction_data(session)
    load_song_features_data(session)
