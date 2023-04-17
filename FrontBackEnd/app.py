from flask import Flask, render_template, request, flash, redirect, url_for
import threading
import requests

#query = "http://localhost:8983/solr/pets/select?&mlt.count=1&mlt=true&mlt.fl=color&mlt.mintf=1&hl.fl=*&hl.highlightMultiTerm=false&hl=true&q.op=AND&rows=20&q=..."

app = Flask(__name__)
app.config['SECRET_KEY'] = '19f9ce9bada7c53b1b75260b27fc722ccc587f070c93f67f'
app.config["CACHE_TYPE"] = "null"

retrieved = []
pushed = []

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        query = request.form['query']
        if not query:
            flash('Insert you query!')
        else:
            path = "http://localhost:8983/solr/pets/"
            op = "select?"
            mlt = "&mlt.count=1&mlt=true&mlt.fl=color,feature&mlt.mintf=1"
            hl = "&hl.fl=*&hl.highlightMultiTerm=false&hl=true"
            q = "&q.op=AND&rows=20&q={}".format(query)
            url = path + op + mlt + hl + q
            results, highlighted, suggested = process(url)
            if results == []:
                return render_template('index.html', messages = [{'no_results': 'Whooops... I really do not have that'}])
            retrieved.clear()
            pushed.clear()
            for pet in results:
                retrieved.append({'result': pet, 'highlighted': highlighted[pet.get('id')]})
            thr = threading.Thread(target=handle_suggestion, args=(suggested,), kwargs={})
            thr.start()
    return render_template('index.html', messages = retrieved)

@app.route('/suggest/')
def suggester():
    return render_template('suggest.html', messages = pushed)

def process(url):
    response = requests.get(url)
    suggested = response.json()['moreLikeThis']
    highlighting = response.json()['highlighting']
    response = response.json()['response']
    return (response.get('docs'), highlighting, suggested)

def handle_suggestion(suggested): #filters duplicate items given by moreLikeThis
    check = []
    for val in suggested.values():
        items = val.get('docs')
        if len(items) > 0:
            id = items[0].get('id')
            if id not in check:
                check.append(id)
                pushed.append({'suggest': items[0]})