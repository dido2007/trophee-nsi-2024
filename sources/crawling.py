import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import re
from collections import Counter
import json
from unidecode import unidecode
import sys
import os
import time


# Agrandissement de la taille des champs CSV (Nous avons trop de données à stocker permet d'eviter les erreurs de type "field larger than field limit")
csv.field_size_limit(sys.maxsize)

# Liste des mots à ignorer (Ce sont des mots recurents et non pertinents pour la recherche)
stop_words = {"a","abord","absolument","afin","ah","ai","aie","aient","aies","ailleurs","ainsi","ait","allaient","allo","allons","allô","alors","anterieur","anterieure","anterieures","apres","après","as","assez","attendu","au","aucun","aucune","aucuns","aujourd","aujourd'hui","aupres","auquel","aura","aurai","auraient","aurais","aurait","auras","aurez","auriez","aurions","aurons","auront","aussi","autant","autre","autrefois","autrement","autres","autrui","aux","auxquelles","auxquels","avaient","avais","avait","avant","avec","avez","aviez","avions","avoir","avons","ayant","ayez","ayons","b","bah","bas","basee","bat","beau","beaucoup","bien","bigre","bon","boum","bravo","brrr","c","car","ce","ceci","cela","celle","celle-ci","celle-là","celles","celles-ci","celles-là","celui","celui-ci","celui-là","celà","cent","cependant","certain","certaine","certaines","certains","certes","ces","cet","cette","ceux","ceux-ci","ceux-là","chacun","chacune","chaque","cher","chers","chez","chiche","chut","chère","chères","ci","cinq","cinquantaine","cinquante","cinquantième","cinquième","clac","clic","combien","comme","comment","comparable","comparables","compris","concernant","contre","couic","crac","d","da","dans","de","debout","dedans","dehors","deja","delà","depuis","dernier","derniere","derriere","derrière","des","desormais","desquelles","desquels","dessous","dessus","deux","deuxième","deuxièmement","devant","devers","devra","devrait","different","differentes","differents","différent","différente","différentes","différents","dire","directe","directement","dit","dite","dits","divers","diverse","diverses","dix","dix-huit","dix-neuf","dix-sept","dixième","doit","doivent","donc","dont","dos","douze","douzième","dring","droite","du","duquel","durant","dès","début","désormais","e","effet","egale","egalement","egales","eh","elle","elle-même","elles","elles-mêmes","en","encore","enfin","entre","envers","environ","es","essai","est","et","etant","etc","etre","eu","eue","eues","euh","eurent","eus","eusse","eussent","eusses","eussiez","eussions","eut","eux","eux-mêmes","exactement","excepté","extenso","exterieur","eûmes","eût","eûtes","f","fais","faisaient","faisant","fait","faites","façon","feront","fi","flac","floc","fois","font","force","furent","fus","fusse","fussent","fusses","fussiez","fussions","fut","fûmes","fût","fûtes","g","gens","h","ha","haut","hein","hem","hep","hi","ho","holà","hop","hormis","hors","hou","houp","hue","hui","huit","huitième","hum","hurrah","hé","hélas","i","ici","il","ils","importe","j","je","jusqu","jusque","juste","k","l","la","laisser","laquelle","las","le","lequel","les","lesquelles","lesquels","leur","leurs","longtemps","lors","lorsque","lui","lui-meme","lui-même","là","lès","m","ma","maint","maintenant","mais","malgre","malgré","maximale","me","meme","memes","merci","mes","mien","mienne","miennes","miens","mille","mince","mine","minimale","moi","moi-meme","moi-même","moindres","moins","mon","mot","moyennant","multiple","multiples","même","mêmes","n","na","naturel","naturelle","naturelles","ne","neanmoins","necessaire","necessairement","neuf","neuvième","ni","nombreuses","nombreux","nommés","non","nos","notamment","notre","nous","nous-mêmes","nouveau","nouveaux","nul","néanmoins","nôtre","nôtres","o","oh","ohé","ollé","olé","on","ont","onze","onzième","ore","ou","ouf","ouias","oust","ouste","outre","ouvert","ouverte","ouverts","o|","où","p","paf","pan","par","parce","parfois","parle","parlent","parler","parmi","parole","parseme","partant","particulier","particulière","particulièrement","pas","passé","pendant","pense","permet","personne","personnes","peu","peut","peuvent","peux","pff","pfft","pfut","pif","pire","pièce","plein","plouf","plupart","plus","plusieurs","plutôt","possessif","possessifs","possible","possibles","pouah","pour","pourquoi","pourrais","pourrait","pouvait","prealable","precisement","premier","première","premièrement","pres","probable","probante","procedant","proche","près","psitt","pu","puis","puisque","pur","pure","q","qu","quand","quant","quant-à-soi","quanta","quarante","quatorze","quatre","quatre-vingt","quatrième","quatrièmement","que","quel","quelconque","quelle","quelles","quelqu'un","quelque","quelques","quels","qui","quiconque","quinze","quoi","quoique","r","rare","rarement","rares","relative","relativement","remarquable","rend","rendre","restant","reste","restent","restrictif","retour","revoici","revoilà","rien","s","sa","sacrebleu","sait","sans","sapristi","sauf","se","sein","seize","selon","semblable","semblaient","semble","semblent","sent","sept","septième","sera","serai","seraient","serais","serait","seras","serez","seriez","serions","serons","seront","ses","seul","seule","seulement","si","sien","sienne","siennes","siens","sinon","six","sixième","soi","soi-même","soient","sois","soit","soixante","sommes","son","sont","sous","souvent","soyez","soyons","specifique","specifiques","speculatif","stop","strictement","subtiles","suffisant","suffisante","suffit","suis","suit","suivant","suivante","suivantes","suivants","suivre","sujet","superpose","sur","surtout","t","ta","tac","tandis","tant","tardive","te","tel","telle","tellement","telles","tels","tenant","tend","tenir","tente","tes","tic","tien","tienne","tiennes","tiens","toc","toi","toi-même","ton","touchant","toujours","tous","tout","toute","toutefois","toutes","treize","trente","tres","trois","troisième","troisièmement","trop","très","tsoin","tsouin","tu","té","u","un","une","unes","uniformement","unique","uniques","uns","v","va","vais","valeur","vas","vers","via","vif","vifs","vingt","vivat","vive","vives","vlan","voici","voie","voient","voilà","voire","vont","vos","votre","vous","vous-mêmes","vu","vé","vôtre","vôtres","w","x","y","z","zut","à","â","ça","ès","étaient","étais","était","étant","état","étiez","étions","été","étée","étées","étés","êtes","être","ô"}

"""
Cette fonction permet de normaliser un texte en supprimant les mots inutiles et en convertissant le texte en minuscules.
C'est une etape importante pour le traitement des données.
"""
def normalize_text(text):
    words = re.findall(r'\w+', unidecode(text.lower()))
    words = [word[:-1] if word.endswith('s') else word for word in words]
    return [word for word in words if word not in stop_words]

"""
Cette fonction permet de créer un crawler qui va parcourir les pages web à partir d'une URL de départ.
Tout d'abord on efface les fichiers CSV s'ils existent déjà puis on appelle crawl_url() pour chaque URL pas visitée.
Le crawler s'arrête après un certain temps défini par le timer. (A titre d'exemple, le timer est fixé à 25 secondes)
"""
def create_crawler(starting_url, timer):
    if os.path.exists('./clientwebpages.csv') and os.path.exists('./clientkeywords.csv'):
        os.remove('./clientwebpages.csv')
        os.remove('./clientkeywords.csv')

    urls_to_crawl = [starting_url]
    visited_urls = set()  

    with open('./clientwebpages.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Title", "Description"])

    with open('./clientkeywords.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["mot-clé", "données"])
        writer.writeheader()

    start_time = time.time()

    while urls_to_crawl  :

        if time.time() - start_time > timer:
            print("Time limit reached.")
            with open('clientkeywords.csv', 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                data = []
                for i, j in list(reader):
                    try:
                        if j.strip():
                            data_dict = json.loads(j)
                            data.append([i, data_dict])
                        else:
                            print(f"Ligne vide ou mal formée détectée: {j}")
                    except json.JSONDecodeError as e:
                        print(f"Erreur lors du décodage JSON pour la ligne '{j}': {e}")
                        continue  
                for i in data:
                    print(i, end='\n')
                return data
            
        current_url = urls_to_crawl.pop(0)
        if current_url not in visited_urls:
            print(f"Crawling: {current_url}")
            visited_urls.add(current_url)
            crawl_url(current_url, urls_to_crawl, visited_urls)

"""
Cette fonction permet de crawler une URL donnée.
Recupère le contenu de la page grace à BeautifulSoup4, extrait les mots clés et les stocke dans un fichier CSV.
Elle extrait également les liens de la page pour les ajouter à la liste des URLs à crawler.
Cette fonction appelle 2 fonctions: process_content() et update_keywords_csv() qui permettent respectivement de 
traiter le contenu de la page et de mettre à jour le fichier CSV des mots clés.
"""
def crawl_url(url, urls_to_crawl, visited_urls):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        process_content(soup, url)

        text = soup.get_text()
        words = normalize_text(text)
        update_keywords_csv(url, words)

        links = [a.get('href') for a in soup.find_all('a', href=True)]
        for link in links:
            absolute_link = urljoin(url, link)
            if absolute_link not in visited_urls:
                urls_to_crawl.append(absolute_link)

    except requests.RequestException as e:
        print(f"Error fetching page: {url}, due to {e}")

"""
Cette fonction permet de traiter le contenu de la page.
Elle extrait le titre et la description grace a BeautifulSoup4 de la page et les stocke dans un fichier CSV.
"""
def process_content(soup, url):
    title = soup.find('title').text if soup.find('title') else ""
    
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag.get('content', '') if description_tag else ""

    with open('./clientwebpages.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([url, title, description])

"""
Cette fonction permet de mettre à jour le fichier CSV des mots clés.
Elle stocke les mots clés et leur fréquence d'apparition dans le fichier "clientkeywords.csv".
"""
def update_keywords_csv(url, words):
    word_counts = Counter(words)
    total_words = sum(word_counts.values())
    keywords_data = {word: count / total_words for word, count in word_counts.items()}

    try:
        with open('./clientkeywords.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            existing_keywords = {row["mot-clé"]: json.loads(row["données"]) for row in reader}
    except FileNotFoundError:
        existing_keywords = {}

    for word, frequency in keywords_data.items():
        if word in existing_keywords:
            if url not in existing_keywords[word]:
                existing_keywords[word][url] = frequency
            else:
                existing_keywords[word][url] = max(frequency, existing_keywords[word][url])
        else:
            existing_keywords[word] = {url: frequency}

    with open('./clientkeywords.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["mot-clé", "données"])
        writer.writeheader()
        for keyword, data in existing_keywords.items():
            writer.writerow({"mot-clé": keyword, "données": json.dumps(data)})

