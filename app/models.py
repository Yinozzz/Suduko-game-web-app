from app import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.Integer)

    def __repr__(self):
        return ''.format(self.username)


class GameResult(db.Model):
    __tablename__ = "result"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerId = db.Column(db.Integer, db.ForeignKey("user.id"))
    start_time = db.Column(db.Integer)
    finish_time = db.Column(db.Integer)
    time_spent = db.Column(db.Integer)

    player = db.relationship("User", backref="games")

    def __repr__(self):
        return ''.format(self.id)


class GameBank(db.Model):
    __tablename__ = "game_bank"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game = db.Column(db.String, unique=True, nullable=False)
    uploaderId = db.Column(db.Integer, db.ForeignKey("user.id"))
    upload_time = db.Column(db.DateTime)

    uploader = db.relationship("User", backref="upload_games")

    def __repr__(self):
        return ''.format(self.id)



