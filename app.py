import json
from os import abort
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    with open('entities.json') as f:
        entities = json.load(f)
        return render_template("main-all-items.html", entities=entities)


@app.route('/paging/<int:eid>')
def paging(eid: int):
    with open('entities.json') as f:
        entities = json.load(f)
        entities_list = []
        if eid == 1:
            entities_list = entities[:3]
        elif eid == 2:
            entities_list = entities[3:6]
        elif eid == 3:
            entities_list = entities[6:]

    return render_template("paging.html", entities=entities_list)


@app.route('/search')
def search():
    model = request.args.get('model')
    with open('entities.json') as f:
        entities = json.load(f)
        response = []
        if not model:
            response = entities
        else:
            for e in entities:
                if e["model"] == model:
                    response.append(e)
                else:
                    new_model = model.split(" ")
                    for item in new_model:
                        if item in e["model"]:
                            response.append(e)
        return render_template("search_ause.html", entities=response)


@app.route('/card/<int:eid>')
def card(eid: int):
    with open('entities.json') as f:
        entities = json.load(f)
        for ent in entities:
            if ent["id"] == eid:
                return render_template("card_full.html", entity=ent)


@app.route('/card/<int:eid>/<view_form>/')
@app.route('/card/<int:eid>')
def card1(eid: int, view_form: str = ''):
    with open('entities.json') as f:
        entities = json.load(f)
        for e in entities:
            if e["id"] == eid:
                if view_form == 'short':
                    return render_template("card_short.html", entity=e)
                elif not view_form:
                    return render_template("card_full.html", entity=e)
                else:
                    abort(400)


if __name__ == '__main__':
    app.run(debug=True)
