from flask import Flask, jsonify, g, session, url_for, request, render_template, redirect
import sqlite3

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secretkeyadam'


def connect_db():
    sql = sqlite3.connect('./data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    session['who'] = 'Adam'
    return '<h1>Hello World</h1>'

@app.route('/rest', methods=['GET'], defaults={'entryId':''})
@app.route('/rest/<entryId>', methods=['GET'])
def rest(entryId):
    if 'who' in session:
        sessionName = session['who']
    else:
        sessionName = 'No One'
    return jsonify({'key': entryId, 'key2' : sessionName}, {'test' : [1, 2, 3] })

@app.route('/theform', methods=['GET', 'POST'])
def theform():

    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute('insert into users (name, location) values (?, ?)', [name, location])
        db.commit()

        #return '<h1>Hello {}. You are from {}. You have submitted the form successfully!<h1>'.format(name, location)
        return redirect(url_for('rest', name=name, location=location))

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return '<h1>The ID is {}. The name is {}. The location is {}.</h1>'.format(results[2]['id'], results[2]['name'], results[2]['location'])

if __name__ == '__main__':
    app.run()
