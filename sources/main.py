# GENESIS by @H&H

from flask import Flask, render_template, request, jsonify

from search import search_keywords

from crawling import create_crawler

app = Flask(__name__)

""" 
Cette route affiche la page HTML index.html
"""
@app.route('/')
def index():
    message = "Hello from Flask!"
    return render_template('index.html', message=message)

"""
Cette route est appelée pour déclencher votre propre crawler avec votre propre URL en appellant la fonction create_crawler.
Elle renvoie les données extraites par le crawler.
"""
@app.route('/crawler', methods=['POST'])
def handle_crawler_submission():
    url = request.form.get('url')
    print(url)
    data = create_crawler(url,25)
    print(data)
    
    return jsonify({"data": data, 'ok': True})

"""
Cette route est appelée pour déclencher le search engine avec un mot clé donné sur les données extraites par votre crawler en appellant la fonction search_keywords (Sur vos données).
Elle renvoie les résultats de la recherche (les 5 premiers résultats les plus pertinents).
"""
@app.route('/keywordingClient', methods=['POST'])
def handle_form_submissionClient():
    keyword = request.form.get('crawler-key')
    results = search_keywords(keyword,'./clientkeywords.csv','./clientwebpages.csv')
    if len(results) == 0:
        print("No results found")
        return jsonify({"error": "No results found"})
    return jsonify(results)

"""
Cette route est appelée pour déclencher le search engine avec un mot clé donné sur les données extraites par notre crawler en appellant la fonction search_keywords (Sur nos données).
Elle renvoie les résultats de la recherche (les 5 premiers résultats les plus pertinents).
"""
@app.route('/keywording', methods=['POST'])
def handle_form_submission():
    keyword = request.form.get('key')
    results = search_keywords(keyword,'./data/keywords.csv','./data/webpages.csv')
    if len(results) == 0:
        return jsonify({"error": "No results found"})
    return jsonify(results)

# Lancement de l'application
if __name__ == '__main__':
    app.run()
