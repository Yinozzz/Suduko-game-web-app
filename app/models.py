from app import db


class User(db.Model):
    """
    User class to declare the structure the user table
    Attributes:
        id: user id
        username: username
        password: password
        user_type: 0 administrator, 1 normal user
        head_pic_url: avatar url
    """
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
            'user_type': self.user_type,
            'head_pic_url': self.head_pic_url
        }
        return data


class GameResult(db.Model):
    """
        Used to save the game records for each user
        Attributes:
            id: game id
            player: user id
            start_time: game started time
            finish_time: game finished time
            time_spent: How many seconds did it take him to finish the game
    """
    __tablename__ = "result"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerId = db.Column(db.Integer, db.ForeignKey("user.id"))
    start_time = db.Column(db.String, nullable=False)
    finish_time = db.Column(db.String, nullable=False)
    time_spent = db.Column(db.Integer, nullable=False)

    player = db.relationship("User", backref="games")

    def __repr__(self):
        return ''.format(self.id)


class GameBank(db.Model):
    """
        Used to save the games
        Attributes:
            id: game id
            game: game data
            uploaderId: ID of the uploader
            upload_time: upload time
            current_game: What day is this game
    """
    __tablename__ = "game_bank"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game = db.Column(db.String, unique=True, nullable=False)
    uploaderId = db.Column(db.Integer, db.ForeignKey("user.id"))
    upload_time = db.Column(db.DateTime)
    current_game = db.Column(db.String, nullable=False)

    uploader = db.relationship("User", backref="upload_games")

    def __repr__(self):
        return ''.format(self.id)


