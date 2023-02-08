from flask import Flask, request, render_template
import gensim
import pandas as pd
import translate
from translate import Translator
import requests
from gensim.models import KeyedVectors

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        searchedWord = request.form["searchedWord"]
        chosenLanguage = request.form["language"]
        spanishTranslator = Translator(to_lang="Spanish")
        englishTranslator = Translator(to_lang="english")
        frenchTranslator = Translator(to_lang="French")
        model = KeyedVectors.load("./word2vec-amazon-cell-accessories-reviews-short.model", mmap='r')
        searchedWordEng = englishTranslator.translate(searchedWord)
        just_first = [a for a, b in model.wv.most_similar(searchedWord, topn=25)]
        similar_words = []
        for x in just_first:
            try:
                if chosenLanguage == 'Spanish':
                    similarWordsSpan = spanishTranslator.translate(x)
                    similar_words.append(similarWordsSpan)
                elif chosenLanguage == 'French':
                    similarWordsFren = frenchTranslator.translate(x)
                    similar_words.append(similarWordsFren)
            except:
                similar_words.append("Error: Could not generate word")
        return render_template("index.html", searchedWord=searchedWord, language=chosenLanguage, similar_words=similar_words)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
