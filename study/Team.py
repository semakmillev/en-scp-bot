# -*- coding: utf-8 -*-
from db.code import Code
from db.team import Team


class StudyTeam(Team):
    def __init__(self, conn):
        self.conn = conn

    def set_study_code(self, team, code, searcher):
        code = Code(self.conn)
        code.check_code_exists(code, 2)
        code.set_code(team, code, 2)
        searcher.steps_2_wait += 2
        return "Код принят!"

    def get_team_skills(self, team):
        sql = ''' select material, colored, height, "size"
                   from study_code sc,
                        team_code tc
                  where sc.code = tc.code
                    and tc.team = :team                                                                          
                  '''
        cur = self.conn.cursor()
        print team
        cur.execute(sql, {'team': team})
        rows = cur.fetchall()
        cur.close()
        skill = {
            'size': {0: 1, 1: 1, 2: 1},
            'height': {0: 1, 1: 1, 2: 1},
            'material': {'wood': 1, 'wall': 1, 'iron': 1},
            'colored': 1
        }
        for row in rows:
            skill['size'][row['size']] += 1
            skill['height'][row['height']] += 1
            skill['material'][row['material']] += 1
            skill['colored'] += row['colored']
        return skill

        '''
        size_0 = 2
        size_1 = 1
        size_2 = 4
        height_0 = 1
        height_1 = 2
        height_2 = 0
        material_wall = 1
        material_iron = 3
        material_wood = 0
        colored_1 = 1
        res = {
            'size': {
                0: size_0,
                1: size_1,
                2: size_2
            },
            'height': {
                0: height_0,
                1: height_1,
                2: height_2
            },
            'material': {
                'wood': material_wood,
                'iron': material_iron,
                'wall': material_wall
            },
            'colored':colored_1
        }
        return res
        '''
