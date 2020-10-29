from flask import Flask, jsonify, abort, request
import sqlalchemy as s_a
from sqlalchemy.types import Integer, Text, Float
import pandas as pd
import json

# ------------ Assignment 2 - FLASK SETUP ------------

app = Flask(__name__)


@app.route('/flask_app/')
def index():
    return "Hello World"


# ------------ SQL setup - THE DATABASE ------------

SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://root:root@db/db'
engine = s_a.create_engine(SQLALCHEMY_DATABASE_URL)
table = 'week_8_assignment'


def database_panda_get(query):
    result = pd.read_sql(
        query,
        con=engine
    )
    return result


def database_json_get(query):
    conn = engine.connect()
    response = conn.execute(query)
    headers = response.keys()
    db_results = response.fetchall()
    print('Result Length: ' + str(len(db_results)))
    print('Query: ' + query)
    conn.close()

    result = from_db_to_objects(db_results, headers)

    return result


def add_person_to_db(newPerson):
    try:
        query = 'INSERT INTO ' + table + ' ('
        query_values = ' values ('
        for k, v in newPerson.items():
            query += "`{}`".format(k) + ', '
            if isinstance(v, str):
                query_values += "'{}'".format(v) + ', '
            else:
                query_values += str(v) + ', '
        query = query[:-2] + ')' + query_values[:-2] + ')'

        conn = engine.connect()
        response = conn.execute(query)
        conn.close()
        return response.rowcount > 0
    except:
        return False

def delete_person_to_db(query):
    conn = engine.connect()
    response = conn.execute(query)
    conn.close()
    return response.rowcount > 0


def update_person_to_db(person):
    try:
        firstName = person['First Name']
        lastName = person['Last Name']
        query = 'UPDATE ' + table + ' SET '
        for k, v in person.items():
            query += "`{}` = ".format(k)
            if isinstance(v, str):
                query += "'{}'".format(v) + ', '
            else:
                query += str(v) + ', '
        query = query[:-2] + " WHERE `First Name` = '{}' AND `Last Name` = '{}'".format(firstName, lastName)
        print(query)
        conn = engine.connect()
        response = conn.execute(query)
        conn.close()
        return response.rowcount
    except:
        return -1


# ------------ Make Person Objects - SUPPORT METHOD ------------

def from_db_to_objects(data, headers):
    result = []
    for person in list(data):
        personInfo = {}
        for idx in range(0, len(headers)):
            personInfo[headers[idx]] = person[idx]
        result.append(personInfo)
    return result


# ------------ Assignment 3 - THE API ------------

# GET ALL
@app.route('/api/showAll', methods=['GET'])
def showAll():
    query = 'SELECT * FROM ' + table
    result = database_json_get(query)
    return jsonify(result)

# GET ONE
@app.route('/api/employee/<string:firstName>/<string:lastName>', methods=['GET'])
def showOne(firstName, lastName):
    query = "SELECT * FROM " + table + \
        " WHERE `First Name` = '{}' AND `Last Name` = '{}'".format(
            firstName, lastName)
    result = database_json_get(query)
    if len(result) < 1:
        return jsonify({'status': 404, 'msg': 'No person found with given first and last name'})
    return jsonify(result[0])

# ADD ONE
@app.route('/api/employee/add', methods=['POST'])
def addOne():
    if not request.json or not 'First Name' in request.json or not 'Last Name' in request.json:
        abort(400)
    newPerson = request.json
    if add_person_to_db(newPerson):
        firstName = request.json['First Name']
        lastName = request.json['Last Name']
        return jsonify({'status': 200, 'msg': "{} {} was added".format(firstName, lastName)})
    else:
        abort(400)

# DELETE
@app.route('/api/employee/delete', methods=['DELETE'])
def deleteOne():
    if not request.json or not 'First Name' in request.json or not 'Last Name' in request.json:
        abort(400)
    firstName = request.json['First Name']
    lastName = request.json['Last Name']
    query = "DELETE FROM " + table + " WHERE `First Name` = '{}' AND `Last Name` = '{}'".format(firstName, lastName)
    if delete_person_to_db(query):
        return jsonify({'status': 200, 'msg': "{} {} was deleted".format(firstName, lastName)})
    else:
        return jsonify({'status': 404, 'msg': "{} {} was not found".format(firstName, lastName)})

# EDIT
@app.route('/api/employee/update', methods=['PUT'])
def updateOne():
    if not request.json or not 'First Name' in request.json or not 'Last Name' in request.json:
        abort(400)
    person = request.json
    result = update_person_to_db(person)
    if result > 0:
        return jsonify({'status': 200, 'msg': "{} {} was updated".format(request.json['First Name'], request.json['Last Name'])})
    elif result < 0:
        abort(400)
    else:
        return jsonify({'status': 404, 'msg': 'No person found with given first and last name'})

#RUN
if __name__ == '__main__':
    app.run(debug=True)
