# -*- coding: utf-8 -*-
import sqlite3
import os


class GameEndException(Exception):
    def __init__(self):
        self.msg = "Вы набрали необходимое количество баллов! Итоговый код - STEP UP!"


def create():
    conn = sqlite3.connect("engine.db")
    conn.row_factory = sqlite3.Row
    conn.text_factory = str
    return conn

def set_admin_message(conn, message_text, time_delay):
    sql = 'insert into main.message_to_send ' \
          'values (:message_text, datetime("now", "localtime", "+"|| :delay ||" minutes"), 0)'
    cur = conn.cursor()
    cur.execute(sql, {"message_text": message_text, "delay": time_delay})
    conn.commit()
    cur.close()
