import os
import json
import sqlite3
import requests


db_stored = os.path.join(os.path.dirname(__file__), 'qaset.db')    # r'D:\Archive\Voibot\qabot\data\qabot\data\qaset.db'
url = 'http://10.1.163.22:5000/encode'
headers = {'Content-Type': 'application/json'}


def generate_all_features(db_stored, begin_id, end_id):
    conn = sqlite3.connect(db_stored)
    cursor = conn.cursor()
    ques_cursor = cursor.execute('select question from qaset where id between ? and ?', (begin_id, end_id))
    questions = []
    for ques in ques_cursor:
        questions.append(ques[0])
    data = {
        'id': 123,
        'texts': questions
        }
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    result = json.loads(r.text)
    qvectors = result['result']
    current_id = begin_id
    while current_id <= end_id:
        cursor.execute('update qaset set feature = ? where id = ?', (json.dumps(qvectors[current_id - begin_id]), current_id))
        current_id += 1
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # begin_id = 1
    # while(begin_id <= 36800):
    #     end_id = begin_id + 99
    #     generate_all_features(db_stored, begin_id, end_id)
    #     print('%d to %d is done.' % (begin_id, end_id))
    #     begin_id = end_id + 1
    begin_id = 36811
    end_id = 36843
    generate_all_features(db_stored, begin_id, end_id)
