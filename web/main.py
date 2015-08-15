
from __future__ import unicode_literals
import json
from flask import Flask, request, abort, render_template
from hazm import Normalizer
from InformationSearcher import InformationSearcher

app = Flask(__name__)
normalizer = Normalizer()
information_searcher = InformationSearcher('../resources/index/')


@app.route('/search', methods=['POST'])
def search():
	if 'argument1' not in request.form or 'argument2' not in request.form or 'relation' not in request.form:
		abort(400)

	query = map(normalizer.normalize, (request.form['argument1'], request.form['argument2'], request.form['relation']))
	results = information_searcher.search(*query)
	return json.dumps({
		'htmls': [information.html() for information in results['informations']],
		'hits': results['hits'],
	}, ensure_ascii=False)


@app.route('/')
def main():
	return render_template('index.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
