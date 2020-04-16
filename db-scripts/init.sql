CREATE TABLE channel(
    id SERIAL PRIMARY KEY,
    name VARCHAR (255) UNIQUE NOT NULL
);

CREATE INDEX idx_channel_name
ON Channel(name);


CREATE TABLE performer(
    id SERIAL PRIMARY KEY,
    name VARCHAR (255) UNIQUE NOT NULL
);

CREATE INDEX idx_performer_name
ON Performer(name);


CREATE TABLE song(
    id SERIAL PRIMARY KEY,
    name VARCHAR (255) NOT NULL,
    performer_id INTEGER REFERENCES Performer(id) NOT NULL
);

CREATE INDEX idx_song_name
ON Song(name, performer_id);


CREATE TABLE play(
    id SERIAL PRIMARY KEY,
    song_id INTEGER REFERENCES Performer(id) NOT NULL,
    channel_id INTEGER REFERENCES Channel(id) NOT NULL,
    start_t TIMESTAMP,
    end_t TIMESTAMP
);

CREATE INDEX idx_play_name
ON Play(song_id, channel_id, start_t, end_t);