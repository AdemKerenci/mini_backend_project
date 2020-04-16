from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Channel(Base):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)


class Performer(Base):
    __tablename__ = "performer"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)


class Song(Base):
    __tablename__ = "song"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    performer_id = Column(Integer, ForeignKey("performer.id"), nullable=False)
    performer = relationship("Performer")


class Play(Base):
    __tablename__ = "play"

    id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey("song.id"), nullable=False)
    song = relationship("Song")
    channel_id = Column(Integer, ForeignKey("channel.id"), nullable=False)
    channel = relationship("Channel")
    start_t = Column(TIMESTAMP, nullable=False)
    end_t = Column(TIMESTAMP, nullable=False)
