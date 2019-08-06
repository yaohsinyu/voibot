import json
import tornado.web
import tornado.ioloop
import tornado.options
from tornado.escape import json_decode, json_encode

from qabot import search

tornado.options.define('port', default=8885)


class IndexHandle(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, I\'m voibot. Try ask me something.')


class AnswerbotHandle(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, I\'m voibot. Try ask me something.')

    def post(self):
        data = json_decode(self.request.body)
        key = 'question'
        if key in data.keys() and isinstance(data[key], str):
            question = data[key]
            match_qaf = search.match(question)
            result = {
                'question': match_qaf[0],
                'answer': match_qaf[1],
                'similarity': str(match_qaf[2])
            }
            self.write(json.dumps(result, ensure_ascii=False))
        else:
            self.send_error(400)


def make_app():
    return tornado.web.Application(
        [
            (r'/', IndexHandle),
            (r'/answer', AnswerbotHandle)
        ]
        # ,
        # template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        # static_path=os.path.join(os.path.dirname(__file__), 'static'),
    )


if __name__ == '__main__':
    app = make_app()
    app.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()
    # nohup python3 -u start_nlp_server.py > log.log 2>&1 &
