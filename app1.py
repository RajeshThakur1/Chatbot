#Import the Library
from newspaper import Article
import random
import string
import nltk
from flask import Flask,render_template,request, jsonify
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
#download the puntk package
nltk.download('punkt',quiet=True)
#Get the Articles
article = Article('https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521')
article.download()
article.parse()
article.nlp()
corpus = article.text
#print the article text
#print(corpus)
#tockanization
text = corpus
sentence_list = nltk.sent_tokenize(text)


# A function to return a random greeting response to a user greeting
def greeting_response(text):
    text = text.lower()

    # Bots greeting response
    bot_greetings = ['howdy', 'hi', 'hello', 'hey', 'hola']

    # user Greeting
    user_greeting = ['hi', 'hello', 'hey', 'greetings', 'wassup', 'hola']

    for word in text.split():
        if word in user_greeting:
            return random.choice(bot_greetings)


def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))
    x = list_var

    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                # Swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    return list_index


# Create the bot response
def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similerity_score = cosine_similarity(cm[-1], cm)
    similerity_score_list = similerity_score.flatten()
    index = index_sort(similerity_score_list)

    index = index[1:]
    response_flag = 0

    j = 0
    for i in range(len(index)):
        if similerity_score_list[index[i]] > 0.0:
            bot_response = bot_response + ' ' + sentence_list[index[i]]
            response_flag = 1
            j = j + 1
        if j > 2:
            break

    if response_flag == 0:
        bot_response = bot_response + ' ' + "I apologize, I don't understand"

    sentence_list.remove(user_input)
    return bot_response


# start the chat

@app.route('/', methods=['GET', 'POST']) # To render Homepage
def home_page():
    return render_template('index.html')

@app.route('/math', methods=['POST'])  # This will be called from UI
def get_answer():
    if (request.method == 'POST'):

        user_input = request.form['text']
        user_input = user_input.lower()
        exit_list = ['exit', 'see you later', 'bye', 'quit', 'break']

        while (True):
            # user_input = input()
            if user_input.lower() in exit_list:
                return render_template('results.html', result="Doc Bot: Chat with you later !")
                break
            else:
                if greeting_response(user_input) != None:
                    return render_template('results.html', result='Doc Bot: ' + greeting_response(user_input))
                else:
                    return render_template('results.html', result='Doc Bot:' + bot_response(user_input))

if __name__ == '__main__':
    app.run(port=8000, debug=True)

















