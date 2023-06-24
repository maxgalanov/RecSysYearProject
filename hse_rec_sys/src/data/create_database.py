from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./music.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class SongFeatures(Base):
    __tablename__ = "song_features"

    song_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    release = Column(String)
    artist_name = Column(String)
    year = Column(Integer)
    genre = Column(String)
    artist_country = Column(String)
    artist_city = Column(String)

class UserSongInteraction(Base):
    __tablename__ = "user_song_interaction"
    
    user_id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, primary_key=True, index=True)
    play_count = Column(Integer)

Base.metadata.create_all(bind=engine)
