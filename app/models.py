import flask_sqlalchemy
db = flask_sqlalchemy.SQLAlchemy()


class Games(db.Model):
    __tablename__ = 'Games'
    game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    players = db.Column(db.String, nullable=False)
    game_columns = db.Column(db.Integer, nullable=False)
    game_rows = db.Column(db.Integer, nullable=False)
    game_state = db.Column(db.String, nullable=False)
    winner = db.Column(db.String, db.ForeignKey('Players.player_name'))


class Players(db.Model):
    __tablename__ = 'Players'
    player_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_name = db.Column(db.String, unique=True, nullable=False)


class Moves(db.Model):
    __tablename__ = 'Moves'
    move_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    move_number = db.Column(db.Integer, nullable=False)
    move_column = db.Column(db.Integer, nullable=False)
    move_row = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('Games.game_id'))
    player_id = db.Column(db.String, db.ForeignKey('Players.player_name'))
