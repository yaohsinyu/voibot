import json
import requests


url = 'http://10.1.163.22:8885/answer'
headers = {'Content-Type': 'application/json'}
question = '你知道灯泡是谁发明的吗'
data = {
    'question': question
    }
r = requests.post(url=url, headers=headers, data=json.dumps(data))
result = json.loads(r.text)
print(result['answer'])
