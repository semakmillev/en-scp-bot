# -*- coding: utf-8 -*-
import configparser
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from bot import init_bot
from db import create
from db.team import Team, TeamError
from run_bot import scheduler
config = configparser.ConfigParser()
config.read('bot.conf')
admin_bot_uid = config['admin_uid']
bot = init_bot(admin_bot_uid)



def send_message():
    try:
        db = create()
        cur = db.cursor()
        sql = '''select * from main.message_to_send where time_to_send <= datetime('now', 'localtime') and status = 0'''
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print 'sending %s' % row['message_text']
            bot.sendMessage(chat_id="@enscp", text=row['message_text'])
        sql_update = '''update main.message_to_send 
                           set status = 1 
                         where time_to_send <= datetime('now', 'localtime') and status = 0'''
        cur.execute(sql_update)
        cur.close()
        db.commit()
        db.close()
    except Exception as ex:
        print ex.message


scheduler.start()
scheduler.add_job(
    func=lambda: send_message(),
    trigger=IntervalTrigger(seconds=3),
    id='admin_bot',
    name='Send admin msg',
    replace_existing=True)

while True:
    pass