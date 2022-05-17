from app import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.Integer, nullable=False)
    head_pic_url = db.Column(db.String(256))

    def __repr__(self):
        return ''.format(self.username)

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'user_type': self.user_type
        }
        return data

class GameResult(db.Model):
    __tablename__ = "result"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerId = db.Column(db.Integer, db.ForeignKey("user.id"))
    start_time = db.Column(db.String, nullable=False)
    finish_time = db.Column(db.String, nullable=False)
    time_spent = db.Column(db.String, nullable=False)

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



