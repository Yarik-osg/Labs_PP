from datetime import datetime
from gevent.pywsgi import WSGIServer
from flask import Flask
from flask_migrate import Manager, Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/lab_6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    count_of_messages = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(70), nullable=False)

    def __init__(self, name, email, count_of_messages, password):
        self.name = name
        self.email = email
        self.count_of_messages = count_of_messages
        self.password = password


class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    count_of_users = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(70), nullable=False)

    def __init__(self, name, count_of_users, description):
        self.name = name
        self.count_of_users = count_of_users
        self.description = description


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    id_note = db.Column(db.Integer, db.ForeignKey(Note.id, ondelete="cascade"), unique=True)
    description = db.Column(db.String(70), nullable=False)

    def __init__(self, name, id_note, description):
        self.name = name
        self.id_note = id_note
        self.description = description


class History(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    id_note = db.Column(db.Integer, db.ForeignKey(Note.id, ondelete="cascade"), unique=True)
    id_users = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="cascade"), unique=True)
    description = db.Column(db.String(70), nullable=False)
    time_of_edit = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, name, id_note, id_users, description, time_of_edit):
        self.name = name
        self.id_note = id_note
        self.id_users = id_users
        self.description = description
        self.time_of_edit = time_of_edit


@app.route("/api/v1/hello-world-/<num_of_variant>")
def hello_world(num_of_variant):
    # user = User("Yaroslav", "exp@smth.com", 22, 22)
    user = User("Yaroslav", "exp@smth.com",2,22)
    note = Note("Game", 1, "For boys")
    d1 = datetime(2017, 3, 5, 12, 30, 10)

    tag = Tag("cooking", 4, "in the kitchen")
    history = History("changes", 4, 1, "new user", d1)
    #db.session.add(user)
    #db.session.add(note)
    #db.session.add(tag)
    db.session.add(history)
    db.session.commit()
    return 'Hello, World! {' + num_of_variant + '}'


app.debug = True
http_server = WSGIServer(('127.0.0.1', 8081), app)
http_server.serve_forever()
