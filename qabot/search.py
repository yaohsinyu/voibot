import os
import time
import json
import pickle
import nmslib
import requests
import numpy as np


questions_stored = r'D:\Archive\Voibot\qabot\data\question.pickle'
answers_stored = r'D:\Archive\Voibot\qabot\data\answer.pickle'
features_stored = r'D:\Archive\Voibot\qabot\data\feature.npy'
index_stored = r'D:\Archive\Voibot\qabot\data\feature_index'

# 加载问题和答案
with open(questions_stored, 'rb') as question_file:
    questions = pickle.load(question_file)
with open(answers_stored, 'rb') as answer_file:
    answers = pickle.load(answer_file)
features = np.load(features_stored)

# 加载索引
index = nmslib.init(method='hnsw', space='cosinesimil')
index.loadIndex(index_stored, load_data=True)


def get_ques_vec(question):
    url = 'http://10.1.163.22:5000/encode'
    headers = {'Content-Type': 'application/json'}
    qas = [question]
    data = {
        'id': 123,
        'texts': qas
        }
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    result = json.loads(r.text)
    qvector = result['result']
    return qvector


def get_answer(question):
    qvector = get_ques_vec(question)
    ids, distance = index.knnQuery(qvector, k=3)
    return answers[ids[0]]


if __name__ == "__main__":
    while True:
        question = input('Question: ')
        qvector = get_ques_vec(question)
        ids, distance = index.knnQuery(qvector, k=3)
        print(questions[ids[0]], distance[0])
        print(questions[ids[1]], distance[1])
        print(questions[ids[2]], distance[2])
