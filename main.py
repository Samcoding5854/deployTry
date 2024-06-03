from Logic.logic import Running
from flask import Flask, jsonify, request
from flask_cors import CORS
import http.server
import socketserver
import webbrowser

app = Flask(__name__)
CORS(app)

@app.route('/hello/World', methods=['GET'])
def home():
    with Running() as bot:
        bot.land_first_page()
        bot.SignIn()
        topics = bot.extract_trending_topics()
        print(jsonify(topics))
    return jsonify(topics)


if __name__ == '__main__':
    app.run(debug=True)