import json
import sqlite3
import requests


db_stored = r'D:\Archive\Voibot\qabot\data\qaset.db'
url = 'http://10.1.163.22:5000/encode'
headers = {'Content-Type': 'application/json'}


def add_qaf(db_stored, question, answer, chat_type='百科', created_by='姚'):
    data = {
        'id': 123,
        'texts': [question]
        }
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    result = json.loads(r.text)
    qvector = json.dumps(result['result'][0])
    conn = sqlite3.connect(db_stored)
    cursor = conn.cursor()
    cursor.execute('insert into qaset (question, answer, chat_type, created_by, feature) values (?, ?, ?, ?, ?)', (question, answer, chat_type, created_by, qvector))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    question = input('question:')
    answer = input('answer:')
    add_qaf(db_stored, question, answer)
