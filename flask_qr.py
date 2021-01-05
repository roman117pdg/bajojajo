import flask
import os
import qrcode
import logger
import io
import time
import secrets
from threading import Thread 
from server import Server

app = flask.Flask(__name__)
app.debug = False
app.secret_key = os.urandom(24)

app_logger = logger.start_logging("root")
s = Server(app_logger)


token = ""

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.qr_codes = []


users = []
users.append(User(id=1, username='qr', password='qr123'))
users.append(User(id=2, username='admin', password='admin'))

@app.route("/qr")
def qr():
    if 'id' in flask.session:
        for user in users:
            if user.id == flask.session['id']:
                global token
                file = qrcode.make(token)
                img_buf = io.BytesIO()
                file.save(img_buf)
                img_buf.seek(0)
                return flask.send_file(img_buf, mimetype='image/jpeg')
            else:
                return flask.redirect(flask.url_for('login'))
    else:
        return flask.redirect(flask.url_for('login'))


    
@app.route("/login", methods=['GET', 'POST'])
def login():

    if flask.request.method == 'POST':
        flask.session.pop('id', None)

        username = flask.request.form['username']
        password = flask.request.form['password']
        
        for user in users:
            if user.username == username:
                if user.password == password:
                    flask.session['id'] = user.id
                    return flask.redirect(flask.url_for('qr'))
        return flask.redirect(flask.url_for('login'))
    return flask.render_template('login.html')


@app.route("/api", methods=['GET', 'POST'])
def api():
    global s
    if flask.request.method == 'POST':
        data = flask.request.data.decode()
        ip = flask.request.remote_addr
        global token
        if token == data:
            s.add_client(ip)
            return "SUCCESS"
        else:
            return "FAILURE"
    else:
        ip = flask.request.remote_addr
        response = s.get_response(ip)
        return response

def run(app_logger):
    token_thread = Thread(target = token_changing, name="website", args =(app_logger, ), daemon=True)
    token_thread.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=port)


def token_changing(app_logger):
    global token
    while True:
        token = secrets.token_hex(32)
        app_logger.info("Token is set to "+token)
        time.sleep(30)


def get_token():
    global token
    return token


# flask_thread = Thread(target = flask_qr.run, name="flask", args =(app_logger, ), daemon=True)
# app_logger.info("starting flask thread...")
# flask_thread.start()


server_thread = Thread(target = s.run, name="server", daemon=True)
app_logger.info("starting server thread...")
server_thread.start()
app_logger.info("starting flask thread...")
run(app_logger)
