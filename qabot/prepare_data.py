import os
import json
import pickle
import nmslib
import sqlite3
import numpy as np


db_stored = r'D:\Archive\Voibot\qabot\data\qaset.db'
questions_stored = r'D:\Archive\Voibot\qabot\data\question.pickle'
answers_stored = r'D:\Archive\Voibot\qabot\data\answer.pickle'
features_stored = r'D:\Archive\Voibot\qabot\data\feature.npy'
index_stored = r'D:\Archive\Voibot\qabot\data\feature_index'


# 将问题，答案，特征分别存储为单独的文件
def dump_db(db_stored, questions_stored, answers_stored, features_stored):
    questions = []
    answers = []
    features = []
    conn = sqlite3.connect(db_stored)
    cursor = conn.cursor()
    qafs = cursor.execute('select question, answer, feature from qaset')
    for qaf in qafs:
        questions.append(qaf[0])
        answers.append(qaf[1])
        features.append(json.loads(qaf[2]))
    conn.close()
    with open(questions_stored, 'wb') as question_file:
        pickle.dump(questions, question_file)
    with open(answers_stored, 'wb') as answer_file:
        pickle.dump(answers, answer_file)
    features = np.array(features)
    np.save(features_stored, features)


# 建立相似度索引并保存
def build_index(features, index_stored):
    index = nmslib.init(method='hnsw', space='cosinesimil')
    index.addDataPointBatch(features)
    index_params = {
        'indexThreadQty': 10,
        'M': 100,
        'efConstruction': 2000,
        'post': 2
    }
    index.createIndex(index_params, print_progress=True)
    # index.saveIndex('feature_index', save_data=True)
    index.saveIndex(index_stored, save_data=True)


if __name__ == "__main__":
    dump_db(db_stored, questions_stored, answers_stored, features_stored)

    features = np.load(features_stored)
    build_index(features, index_stored)
