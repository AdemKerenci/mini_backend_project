import datetime
from typing import Dict, List

import dateutil.parser
from sqlalchemy import func

from . import db
from .model import Channel, Performer, Play, Song


class Service:
    @staticmethod
    def _create_or_get(table, create_args):
        """
        This method query the object in given object with given arguments,
        If it exists it will return the object, otherwise it will create, commit and return the object

        Args:
            table: model class object that will be used to query and object creation.
            create_args: arguments that identify an entity as unique in given table.
        Returns:
            Entity from db belongs to given table.
        """
        obj = db.session.query(table).filter_by(**create_args).first()
        if not obj:
            obj = table(**create_args)
            db.session.add(obj)
            db.session.commit()
        return obj

    @staticmethod
    def add_channel(channel_name: str):
        """ Add the channel to the db, if exists just ignores. """
        return Service._create_or_get(Channel, {"name": channel_name})

    @staticmethod
    def add_performer(performer_name: str):
        """ Add the performer to the db, if exists just ignores. """
        return Service._create_or_get(Performer, {"name": performer_name})

    @staticmethod
    def add_song(performer_name: str, song_name: str):
        """ Add the song to the db, if exists just ignores, also trigger adding performer too. """
        performer = Service.add_performer(performer_name)
        performer_id = performer.id
        return Service._create_or_get(
            Song, {"name": song_name, "performer_id": performer_id}
        )

    @staticmethod
    def add_play(
        channel_name: str, performer_name: str, song_name: str, start: str, end: str
    ):
        """ Add the play to the db, if exists just ignores, also trigger adding song too. """
        song = Service.add_song(performer_name, song_name)
        channel = Service.add_channel(channel_name)
        song_id = song.id
        channel_id = channel.id
        return Service._create_or_get(
            Play,
            {
                "song_id": song_id,
                "channel_id": channel_id,
                "start_t": start,
                "end_t": end,
            },
        )

    @staticmethod
    def get_song_plays(
        performer_name: str, song_name: str, start: str, end: str
    ) -> List:
        """ Get channels that the given song is played between specific time period. """
        filters = (
            Song.name == song_name,
            Performer.name == performer_name,
            Play.start_t >= start,
            Play.end_t <= end,
        )
        query_result = (
            db.session.query(Channel.name, Play.start_t, Play.end_t)
            .join(Channel)
            .join(Song)
            .join(Performer)
            .filter(*filters)
            .all()
        )
        result_columns = ["channel", "start", "end"]
        return list(map(lambda res: dict(zip(result_columns, res)), query_result))

    @staticmethod
    def get_channel_plays(channel_name: str, start: str, end: str) -> List:
        """ Get songs that is played in given channel between specific time period. """
        filters = (
            Channel.name == channel_name,
            Play.start_t >= start,
            Play.end_t <= end,
        )
        query_result = (
            db.session.query(Performer.name, Song.name, Play.start_t, Play.end_t)
            .join(Channel)
            .join(Song)
            .join(Performer)
            .filter(*filters)
            .all()
        )
        result_columns = ["performer", "title", "start", "end"]
        return list(map(lambda res: dict(zip(result_columns, res)), query_result))

    @staticmethod
    def get_top(channels: List[str], start: str, limit: int) -> List:
        """ Get the top songs in given channels with additional previous week information. """
        cur_rank = Service._get_current_week_rank(channels, start, limit)
        pre_rank = Service._get_previous_week_rank(channels, start, limit)

        for key, value in pre_rank.items():
            if key in cur_rank:
                cur_rank[key].update(value)
        return list(cur_rank.values())

    @staticmethod
    def _get_current_week_rank(channels: List[str], start: str, limit: int) -> Dict:
        """ Get the top songs in given channels for given week. """
        start_date = dateutil.parser.parse(start)
        filters = (
            Channel.name.in_(channels),
            Play.start_t >= start,
            Play.end_t <= start_date + datetime.timedelta(weeks=1),
        )
        queries = (
            Play.song_id,
            func.max(Song.name),
            func.max(Performer.name),
            func.count(Play.song_id),
        )

        query_result = Service._rank_query(queries, filters, limit)

        result_columns = ["title", "performer", "plays"]
        res_dict = {}
        for rank, values in enumerate(query_result, start=0):
            song_id = values[0]
            res_dict[song_id] = {
                "rank": rank,
                "previous_rank": None,
                "previous_plays": 0,
                **dict(zip(result_columns, values[1:])),
            }
        return res_dict

    @staticmethod
    def _get_previous_week_rank(channels: List[str], start: str, limit: int) -> Dict:
        """ Get the top songs in given channels for previous week. """
        start_date = dateutil.parser.parse(start)
        filters = (
            Channel.name.in_(channels),
            Play.start_t >= start_date - datetime.timedelta(weeks=1),
            Play.end_t <= start,
        )
        queries = (Play.song_id, func.count(Play.song_id))
        query_result = Service._rank_query(queries, filters, limit)

        res_dict = {}
        for pre_rank, values in enumerate(query_result, start=0):
            song_id = values[0]
            res_dict[song_id] = {"previous_rank": pre_rank, "previous_plays": values[1]}

        return res_dict

    def _rank_query(queries: List, filters: List, limit: int):
        """ Runs and returns query to extract rank information from db."""
        return (
            db.session.query(*queries)
            .join(Channel)
            .join(Song)
            .join(Performer)
            .filter(*filters)
            .group_by(Play.song_id)
            .order_by(func.count(Play.song_id).desc())
            .limit(limit)
            .all()
        )
