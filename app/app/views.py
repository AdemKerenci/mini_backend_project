from flask import Blueprint, request

from .service import Service
from .utils import with_response

base_bp = Blueprint("base", __name__)


@base_bp.route("/add_channel", methods=["POST"])
def add_channel():
    data = request.form
    Service.add_channel(channel_name=data["name"])
    return ("", 204)


@base_bp.route("/add_performer", methods=["POST"])
def add_performer():
    data = request.form
    Service.add_performer(performer_name=data["name"])
    return ("", 204)


@base_bp.route("/add_song", methods=["POST"])
def add_song():
    data = request.form
    Service.add_song(performer_name=data["performer"], song_name=data["title"])
    return ("", 204)


@base_bp.route("/add_play", methods=["POST"])
def add_play():
    data = request.form
    Service.add_play(
        channel_name=data["channel"],
        performer_name=data["performer"],
        song_name=data["title"],
        start=data["start"],
        end=data["end"],
    )
    return ("", 204)


@base_bp.route("/get_song_plays", methods=["GET"])
@with_response
def get_song_plays():
    data = request.args
    return Service.get_song_plays(
        performer_name=data["performer"],
        song_name=data["title"],
        start=data["start"],
        end=data["end"],
    )


@base_bp.route("/get_channel_plays", methods=["GET"])
@with_response
def get_channel_plays():
    data = request.args
    return Service.get_channel_plays(
        channel_name=data["channel"], start=data["start"], end=data["end"]
    )


@base_bp.route("/get_top", methods=["GET"])
@with_response
def get_top():
    data = request.args
    return Service.get_top(
        channels=eval(data["channels"]), start=data["start"], limit=eval(data["limit"])
    )
