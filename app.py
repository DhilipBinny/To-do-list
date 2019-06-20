from flask import Flask, Response, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
import json
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

postgresdbconnection="" # enter your connection string.

engine = create_engine(sqlconnection)
db = scoped_session(sessionmaker(bind=engine))
print( db.execute("SELECT * FROM todo").fetchall())


@app.route("/")
def index():
    return "hello"

@app.route("/api/v1/task", methods=["GET"])
def getall():
    print("got request")
    tasks_available = db.execute("SELECT * FROM todo").fetchall()

    data = []
    for id,task in tasks_available:
        record_dict = {
            "id" : id,
            "task":task
        }
        data.append(record_dict)

    resp = {
        "status": "success",
        "data": data
    }
    resp_str = json.dumps(resp)
    return Response(resp_str,status=200, content_type="application/json", headers={ 'Access-Control-Allow-Origin': '*' })

@app.route("/api/v1/task", methods=["POST"])
def add():
    
    task = request.get_json(force=True)
    print(task)
    data = task["task"]

    id_return= db.execute ("INSERT INTO todo (task) VALUES (:task) RETURNING id", {"task":data})
    db.commit()
    
    # if len(id_return)!=0:
    #     id = id_retun.fetchone()[0]

    id = id_return.fetchone()[0]
    resp = {
        "status": "Added data success",
        "task": data,
        "id":id
    }
    resp_str = json.dumps(resp)
    print(resp_str)
    return Response(resp_str, status=200, content_type="application/json", headers={ 'Access-Control-Allow-Origin': '*' })

@app.route("/api/v1/task/delete", methods=["DELETE"])
def delete():
    data = request.get_json()
    task_id = data["task_id"]
    print(task_id)

    db.execute("DELETE FROM todo WHERE id=(:id) ", {"id":task_id})
    db.commit()

    resp = {
        "status": "Delete success",
        "id":task_id
    }
    resp_str = json.dumps(resp)
    return Response(resp_str, content_type="application/json",headers={ 'Access-Control-Allow-Origin': '*'})

@app.route("/api/v1/task/delete/all", methods=["DELETE"])
def deleteall():
    # data = request.get_json()
    # task_id = data["task_id"]
    # print(task_id)

    db.execute("DELETE FROM todo")
    db.commit()

    resp = {
        "status": "Delete success",
    }
    resp_str = json.dumps(resp)
    return Response(resp_str, content_type="application/json",headers={ 'Access-Control-Allow-Origin': '*'})


if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    print(port)
    app.run(debug = True, host='0.0.0.0', port = port)
