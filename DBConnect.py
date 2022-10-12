import mysql.connector
import json
import os
from dotenv import dotenv_values

env_var = dotenv_values('.env')


def getHashTags():

    cnx = mysql.connector.connect(
        host=env_var.get('HOST'),
        database=env_var.get('DATABASE'),
        user=env_var.get('USER'),
        password=env_var.get('PASSWORD'),
        port=int(env_var.get('PORT'))
    )
    container = os.environ.get('ContainerName') 
    cursor = cnx.cursor()
    getQuery = 'select * from tasks where container_id = "{0}"'.format(container)
    cursor.execute(getQuery)
    results=cursor.fetchall()
    workflows = {}
    for result in results:
        id = result[4]
        workflows[id] = {}
        query = ""
        try:
            query = json.loads(result[len(result)-2])['Query']
            workflows[id]["query"] = query
            workflows[id]["pointer"] = 0
            strQuery = 'select container_id from tasks e where workflow_id = "{0}" order by e.order'.format(id)
            cursor.execute(strQuery)
            out=cursor.fetchall()
            for row in out:
                if "steps" not in workflows[id]:
                    workflows[id]["steps"] = []
                workflows[id]["steps"].append(row[0])
            
        except Exception:
            print("Processing Query Exception",Exception)
    try:
        cursor.close()
        cnx.close()
    except Exception:
        print("DBClose Exception",Exception)
    return workflows

