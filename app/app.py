from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'mlbplayerData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Adib Haques Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlbplayerData')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, mlbplayers=result)


@app.route('/view/<int:mlb_id>', methods=['GET'])
def record_view(mlb_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlbplayerData WHERE id=%s', mlb_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', mlbplayer=result[0])


@app.route('/edit/<int:mlb_id>', methods=['GET'])
def form_edit_get(mlb_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlbplayerData WHERE id=%s', mlb_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', mlbplayer=result[0])


@app.route('/edit/<int:mlb_id>', methods=['POST'])
def form_update_post(mlb_id):
    cursor = mysql.get_db().cursor()
    inputData = (
        request.form.get('Name'), request.form.get('Team'), request.form.get('Position'),
        request.form.get('Height_inches'), request.form.get('Weight_lbs'),
        request.form.get('Age'), mlb_id)
    sql_update_query = """UPDATE mlbplayerData t SET t.Name = %s, t.Team = %s, t.Position = %s, t.Height_inches = 
    %s, t.Weight_lbs = %s, t.Age = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/mlbplayers/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New MLB Player Form')


@app.route('/mlbplayers/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (
        request.form.get('Name'), request.form.get('Team'), request.form.get('Position'),
        request.form.get('Height_inches'), request.form.get('Weight_lbs'),
        request.form.get('Age'))
    sql_insert_query = """INSERT INTO mlbplayerData (Name, Team, Position, Height_inches, Weight_lbs, Age) VALUES (%s, %s,
    %s, %s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:mlb_id>', methods=['POST'])
def form_delete_post(mlb_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM mlbplayerData WHERE id = %s """
    cursor.execute(sql_delete_query, mlb_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


#@app.route('/api/v1/mlb', methods=['GET'])
#def api_browse() -> str:
#    cursor = mysql.get_db().cursor()
#   cursor.execute('SELECT * FROM mlb')
#  result = cursor.fetchall()
# json_result = json.dumps(result);
#    resp = Response(json_result, status=200, mimetype='application/json')
#    return resp


#@app.route('/api/v1/grades/<int:mlb_id>', methods=['GET'])
#def api_retrieve(mlb_id) -> str:
#    cursor = mysql.get_db().cursor()
#    cursor.execute('SELECT * FROM mlb WHERE id=%s', mlb_id)
#    result = cursor.fetchall()
#    json_result = json.dumps(result);
#    resp = Response(json_result, status=200, mimetype='application/json')
#    return resp


#@app.route('/api/v1/mlb/', methods=['POST'])
#def api_add() -> str:
#    resp = Response(status=201, mimetype='application/json')
#    return resp


#@app.route('/api/v1/mlb/<int:mlb_id>', methods=['PUT'])
#def api_edit(mlb_id) -> str:
#    resp = Response(status=201, mimetype='application/json')
#    return resp


#@app.route('/api/grades/<int:mlb_id>', methods=['DELETE'])
#def api_delete(mlb_id) -> str:
#    resp = Response(status=210, mimetype='application/json')
#    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
