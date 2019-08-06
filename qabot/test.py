import json
import requests


url = 'http://10.1.163.22:8885/answer'
headers = {'Content-Type': 'application/json'}
question = '生命在于运动这句话是谁说的'
data = {
    'question': question
    }
r = requests.post(url=url, headers=headers, data=json.dumps(data))
result = json.loads(r.text)
print(result['answer'])
simi = float(result['similarity'])
print(simi)
