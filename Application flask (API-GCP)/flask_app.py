from flask import Flask, request
from flask_mail import Mail, Message
from flask_ngrok import run_with_ngrok
from apps import project, environment, local, mail_setting
app = Flask(__name__)
run_with_ngrok(app)
app.config.update(mail_setting)
mail = Mail(app)


@app.route('/Dalayerbrute', methods=['POST', 'GET'])
def Dalayerbrute():
    message = "<h2>You have launched the first script!</h2>" \
              "<h3>The sheet named 'Datalayer brute' has started to update</h3>"
    return message


@app.route('/Objets', methods=['POST', 'GET'])
def Objets():
    message = "<h2>You have launched the second script!</h2>" \
              "<h3>Sheets named 'Objets [Number]' has started to update</h3>"
    return message

@app.route('/', methods=['POST', 'GET'])
def Open():
    message = "<h2>This is the QA automatisation tool</h2>" \
              "<h3>Specify http://127.0.0.1:5000/Dalayerbrute or http://127.0.0.1:5000/Objets to start a script </h3>"
    return message

if __name__ == '__main__':
    app.run()

