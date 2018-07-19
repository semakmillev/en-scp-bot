# -*- coding: utf-8 -*-
import sqlite3

from db import create
from db.team import Team


class ConditionTeam(Team):
    def __init__(self, conn):
        super(ConditionTeam, self).__init__(conn)


    def get_team_score(self, team):
        sql = '''select sum(code_value) score from team_condition_code where team = :team'''
        cur = self.conn.cursor()
        cur.execute(sql, {'team': team})
        score = cur.fetchall()[0]['score']
        cur.close()
        return score

    def check_team_score(self, team):
        score = self.get_team_score(team)
        return score > 640




