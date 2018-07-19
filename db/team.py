# -*- coding: utf-8 -*-
import sqlite3

from db import create


class TeamError(Exception):
    def __init__(self, msg):
        self.msg = msg


class Team(object):
    def __init__(self, conn):
        self.conn = conn

    def get_team_by_chat(self, chat_id):
        sql = "select * from main.team_chat where chat_id = :chat_id"
        cur = self.conn.cursor()
        cur.execute(sql, {"chat_id": chat_id})
        rows = cur.fetchall()
        cur.close()
        return None if len(rows) == 0 else rows[0]['chat_id']

    def set_team_task_id(self, team, task_id):
        sql = "update main.team set task_id = :task_id where TEAM_NAME = :team_name"
        cur = self.conn.cursor()
        cur.execute(sql, {"team_name": team, "task_id": task_id})
        self.conn.commit()
        cur.close()

    def get_team_task_id(self, team):
        sql = "select * from main.team where TEAM_NAME = :team_name"
        cur = self.conn.cursor()
        cur.execute(sql, {"team_name": team})
        rows = cur.fetchall()
        cur.close()
        return None if len(rows) == 0 else rows[0]['team_task']

    def set_team_2_chat(self, chat_id, team):
        sql = "insert into main.team_chat(chat_id, team_code) values(:chat_id, :team_code)"
        cur = self.conn.cursor()
        cur.execute(sql, {"chat_id": chat_id, "team_code": team})
        self.conn.commit()

    def register_chat_to_team(self, chat_id, pwd):
        sql = "select * from main.team where TEAM_PWD = :pwd"
        cur = self.conn.cursor()
        cur.execute(sql, {"pwd": pwd})
        rows = cur.fetchall()
        cur.close()
        if len(rows) == 0:
            raise TeamError("Неверный командный токен!")
        else:
            team = rows[0]["TEAM_NAME"]
            self.set_team_2_chat(chat_id, team)
            return team
