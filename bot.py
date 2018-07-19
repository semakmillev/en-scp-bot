# -*- coding: utf-8 -*-
import urllib3
import telepot
import sys
import telepot.api
import time
import datetime

# from apscheduler.scheduler import Scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from kombu import Connection
# from db_bot.bot_training import insert_table_bot_training
# from db_bot.bot_user import *

#from db import create, GameEndException
#from db.code import Code, CodeError
#from db.team import Team, TeamError


reload(sys)
sys.setdefaultencoding('utf8')
headers = urllib3.make_headers(proxy_basic_auth='Golubitskiy_AO:_Qwerty123')


urls = 'http://Golubitskiy_AO:_Qwerty123@hproxy.mmbank.ru:9090'
url = 'http://hproxy.mmbank.ru:9090'
proxy = urllib3.ProxyManager(proxy_url=url, proxy_headers=headers)

telepot.api._pools = {'default': urllib3.ProxyManager(proxy_url=url,
                                                      num_pools=3,
                                                      maxsize=10,
                                                      retries=False,
                                                      timeout=30,
                                                      proxy_headers=headers), }
telepot.api._onetime_pool_spec = (
    urllib3.ProxyManager, dict(proxy_url=url, num_pools=1, maxsize=1, retries=False, timeout=30, proxy_headers=headers))

def init_bot(bot_uid):
    bot = telepot.Bot(bot_uid)
    return bot

