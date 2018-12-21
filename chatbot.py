# -*- coding: utf-8 -*-
import json
import urllib.request

import screen
import crawl_naver as cn

from urllib import parse
from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

import multiprocessing as mp
from threading import Thread

app = Flask(__name__)

slack_token = 'xoxb-504131970294-508903605702-OFjUTWEZBiskwMByJEQw5LGh'
slack_client_id = '504131970294.507699781189'
slack_client_secret = '42417226469148766e22973c18d785d2'
slack_verification = 'H0pxKZ8jdR2btltQkjiJbat5'
sc = SlackClient(slack_token)

# threading function
def processing_event(queue):
   while True:
       # 큐가 비어있지 않은 경우 로직 실행
       if not queue.empty():
           slack_event = queue.get()

           # Your Processing Code Block gose to here
           channel = slack_event["event"]["channel"]
           text = slack_event["event"]["text"]

           # 챗봇 크롤링 프로세스 로직 함수
           keywords = _crawl_nstore(text)

           # 아래에 슬랙 클라이언트 api를 호출하세요
           sc.api_call(
               "chat.postMessage",
               channel=channel,
               text=keywords
           )

# 크롤링 함수 구현하기
pre_command = ''
INTRO = "안녕하세요 NAVER N스토어 챗봇입니다.\n무엇을 도와드릴까요?\nex)silee야, 요즘 인기있는 이북 알려줘\n제목으로 검색하려면 '검색 : 컨텐츠 제목 / 장르' 의 양식으로 이야기해주세요!"
URL = 'https://nstore.naver.com/'


def _crawl_nstore(user_input):
    user_input = user_input[13:]

    contents_type = cn.ts.get_content_type(user_input)
    display_type = cn.ts.get_display_type(user_input)
    print('ct : ' + contents_type + ' dt' + display_type)

    print(user_input)
    if user_input == '' or user_input == 'silee야' or user_input == '시리야':
        return INTRO
    elif (display_type == 'find'):
        display_text = cn.crawl_by_title(user_input, contents_type)
        display_text.append('\n' + INTRO)
    elif (display_type == 'recom'):
        display_text = cn.get_random_one()
    elif (display_type == 'none' or contents_type == 'all'):
        return screen.recommand(contents_type)
    elif (display_type == 'new'):
        display_text = cn.crawl_news(user_input, contents_type)
        display_text.append('\n' + INTRO)
    elif (display_type == 'top'):
        display_text = cn.crawl_top10(user_input, contents_type)
        display_text.append('\n' + INTRO)


    print(display_text)

    return u'\n'.join(display_text)

# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):

   if event_type == "app_mention":
       event_queue.put(slack_event)
       return make_response("App mention message has been sent", 200, )



@app.route("/listening", methods=["GET", "POST"])
def hears():
   slack_event = json.loads(request.data)

   if "challenge" in slack_event:
       return make_response(slack_event["challenge"], 200, {"content_type":
                                                                "application/json"
                                                            })

   if slack_verification != slack_event.get("token"):
       message = "Invalid Slack verification token: %s" % (slack_event["token"])
       make_response(message, 403, {"X-Slack-No-Retry": 1})

   if "event" in slack_event:
       event_type = slack_event["event"]["type"]
       return _event_handler(event_type, slack_event)

   # If our bot hears things that are not events we've subscribed to,
   # send a quirky but helpful error response
   return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                        you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
   return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
   event_queue = mp.Queue()

   p = Thread(target=processing_event, args=(event_queue,))
   p.start()
   print("subprocess started")

   app.run('0.0.0.0', port=8080)
   p.join()