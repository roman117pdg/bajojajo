import flask
import os

app = flask.Flask(__name__)
app.debug = False

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    data = flask.request.data.decode()
    return "\""+data+"\""


def run():
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0',port=port)

run()
