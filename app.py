from flask import Flask, request, jsonify, render_template
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

app = Flask(__name__)

nltk.download('punkt')
nltk.download('stopwords')
with open('listofprofanitywords.txt') as f:
    profanity_list = [word.strip().strip('"') for line in f for word in line.split(',')]


def detect_profanity(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text.lower())

    for word in word_tokens:
        if word not in stop_words and word in profanity_list:
            return True

    return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check():
    text = request.json['text']
    is_profane = detect_profanity(text)
    return jsonify({'is_profane': is_profane})
