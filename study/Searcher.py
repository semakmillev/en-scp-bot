# -*- coding: utf-8 -*-

'''
list of abilities

danger: high - low
complexity: simple - hidden
material: metal - wall/brick - wood
colored
size: pixel/small/big_code

'''
import random

from db.code import Code
from study.Team import StudyTeam

num_of_empty_balls = 1000


class Searcher(object):
    def __init__(self, conn, team_name):
        self.conn = conn
        self.steps_2_wait = 0
        # self.team_skills = {}
        self.team = StudyTeam(conn)
        self.team_name = team_name
        self.places = []
        self.team_skills = {}

    def update_team_skills(self):
        self.team_skills = self.team.get_team_skills(self.team_name)

    def fill_places(self, update_scills=True):
        self.update_team_skills() if update_scills else None
        self.places = [None for i in range(0, num_of_empty_balls)]
        sql = '''select *
                  from study_search_code ssc
                 where not exists(select * 
                                    from main.team_code tc 
                                   where team = :team and tc.code = ssc.code )'''
        cur = self.conn.cursor()
        cur.execute(sql, {'team': self.team_name})
        rows = cur.fetchall()
        cur.close()
        print self.team_skills
        for code_info in rows:
            size_arr = [code_info['code'] for i in range(1, (self.team_skills['size'][code_info['size']] - 1) * 5 + 1)]
            self.places.extend(size_arr)
            height_arr = [code_info['code'] for i in
                          range(1, (self.team_skills['height'][code_info['height']] - 1) * 5 + 1)]
            self.places.extend(height_arr)
            material_arr = [code_info['code'] for i in
                            range(1, (self.team_skills['material'][code_info['material']] - 1) * 5 + 1)]
            self.places.extend(material_arr)
            if code_info['colored'] == 1:
                colored_arr = [code_info['code'] for i in range(1, (self.team_skills['colored'] - 1) * 5 + 1)]
                self.places.extend(colored_arr)

    def do_search(self):
        if self.steps_2_wait > 0:
            self.steps_2_wait -= 1
            return None
        i = random.randint(0, len(self.places))
        if self.places[i] is not None:
            code = Code(self.conn)
            code.set_code(self.team_name, self.places[i], 2)
            self.fill_places(False)
            return 'Был найден код! %s' % self.places[i]
        return None
