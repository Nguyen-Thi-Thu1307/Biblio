import flask_sqlalchemy # type: ignore
from authlib.integrations.flask_client import OAuth

db = flask_sqlalchemy.SQLAlchemy()
oauth = OAuth()
