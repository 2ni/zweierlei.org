from flask_redis import FlaskRedis
from redis import StrictRedis

class DecodedRedis(StrictRedis):
    """
    Decode output to always get strings from redis
    instead of bytes (which can't be handled by jsonify)

    see https://github.com/tferreira/Flask-Redis/blob/master/index.py
    """
    @classmethod
    def from_url(cls, url, db=None, **kwargs):
        kwargs['decode_responses'] = True
        return StrictRedis.from_url(url, db, **kwargs)

db = FlaskRedis.from_custom_provider(DecodedRedis)

from flask_jwt_extended import JWTManager
jwt = JWTManager()
