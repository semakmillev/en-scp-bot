# -*- coding: utf-8 -*-
import configparser
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from bot import init_bot
from db import create
from db.team import Team, TeamError
from study import study_job
from study.Searcher import Searcher


config = configparser.ConfigParser()
config.read('bot.conf')

bot_uid = ''
bot = init_bot(bot_uid)
scheduler = BackgroundScheduler()

def handle(msg):
    team = Team()
    con = create()
    reply_to_message_id = msg['message_id']
    chat_id = msg["chat"]["id"]
    team_name = team.get_team_by_chat(chat_id)
    message_text = '%s' % msg['text'].encode("utf-8")
    print message_text
    if message_text == '/ping':
        bot.sendMessage(chat_id, "I'm alive!", reply_to_message_id=reply_to_message_id)
        return
    if team_name is None:
        try:
            team_name = team.register_chat_to_team(chat_id, str(message_text).upper())
            bot.sendMessage(chat_id, "Вы зарегистрировались в команду %s" % team_name)
            return
        except TeamError as ex:
            bot.sendMessage(chat_id, ex.msg)
            return
    print team
    task_id = team.get_team_task_id(team_name)
    if task_id == 1:
        if message_text == '/pleasestartstudy':
            team.set_team_task_id(team_name,2)
            #scheduler.start()
            searcher = Searcher(con, team_name)
            task_id = task_id + 1
            scheduler.add_job(
                func=lambda: study_job(chat_id, searcher),
                trigger=IntervalTrigger(seconds=10),
                id='db_info',
                name='Fill db info',
                replace_existing=True)
