# coding=utf-8
import os
import json
import time
import datetime
import requests
import asrtts
from recorder import RPAudio


def askrobot(text='你好', mode='knowledge'):
    if mode == 'knowledge':
        url = 'http://10.1.163.22:8885/answer'
        headers = {'Content-Type': 'application/json'}
        question = text
        data = {
            'question': question
            }
        try:
            r = requests.post(url=url, headers=headers, data=json.dumps(data))
            result = json.loads(r.text)
            similarity = float(result['similarity'])
            if similarity < 0.1:
                reply = result['answer']
            else:
                reply = '我不清楚。'
        except Exception as e:
            reply = '我好像出了点问题哦。'
    else:
        reply = text
    return reply


def get_nowtime_str():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")


def chaton():
    # voicefolder = 'voice'
    voicefolder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'voice')
    rpaudio = RPAudio(debug=False)
    rpaudio.open()
    rpaudio.start_record(voicefolder)

    bot_title = 'Robot: '
    you_title = '我: '

    bot_say = '你好，很高兴认识你。'
    print(bot_say)
    filename = os.path.join(voicefolder, 'r_' + get_nowtime_str() + '.wav')
    if asrtts.text2audio(bot_say, filename):
        rpaudio.playing(filename=filename)

    over = False
    while not over:
        voice = rpaudio.get_one_voice()
        if voice is None:
            time.sleep(0.2)
            continue
        try:
            asr_status, you_say_text = asrtts.audio2text(voice)
        except Exception as e:
            asr_status = False
            print('可能网络问题，语音识别出错。')

        if asr_status and you_say_text:
            try:
                print(you_title + you_say_text)
            except Exception as e:
                pass

            if you_say_text in '再见拜拜':
                over = True
                bot_say_text = '好的，拜拜'
            else:
                over = False
                mode = 'knowledge'
                bot_say_text = askrobot(you_say_text, mode)

            try:
                print(bot_title + bot_say_text)
            except Exception as e:
                pass

            bot_say_file = os.path.join(voicefolder, 'r_' + get_nowtime_str() + '.wav')
            try:
                tts_status = asrtts.text2audio(bot_say_text, bot_say_file)
            except Exception as e:
                tts_status = False
                print('可能网络问题，语音合成出错。')
            if tts_status:
                rpaudio.start_play(filename=bot_say_file)

    rpaudio.play_wait()
    rpaudio.stop_record()
    rpaudio.close()


if __name__ == '__main__':
    chaton()
