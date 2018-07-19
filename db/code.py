# -*- coding: utf-8 -*-
import sqlite3

from db import create, GameEndException

sql_action = '''
  select a.action_type, t.zone 
    from action_code a,
         team_condition_code t
   where a._code = t._code
    and datetime(datetime('now'), "+3 hours") < datetime(datetime(code_date), "+"||a.duration||" minutes")
    order by action_type
'''


class CodeError(Exception):
    def __init__(self, msg):
        self.msg = msg


team_chat = {}
'''
Зоны:
1. Общая
2. Можно находиться только по двое, связанные 3х метровой верёвкой.
3. Можно находиться строго без средств связи
4. Запрещено касаться земли
5. Любой игрок обязан иметь не более, 
    чем в метре по горизонтали (т.е. можно лезть вверх без) пятилитровку воды

Коды:
1. Блокировка всех кодов на 3 минуты STOP x 3 
2. Блокировка всех кодов на 2 минуты STOP x4
3. Пожар в выбранной зоне - игроки обязаны иметь не более чем в метре по горизонтали огнетушитель x3
4. Тишина на зону - игроки не имеют права разговаривать на глазах у агентов.
Ни шёпотом, ни на ушко. Агенты имеют право провоцировать команды! Примечание: При словах агента "это не игра!"
 человек может говорить с агентом и с тем, с кем агент разрешит. Сделано для безопасности. x3
5. Буст на локу - стоимость кодов на всей локе увеличивается в два раза на 3 минуты x3 
6. Буст на зону - стоимость кодов на зоне увеличивается в два раза x2
7. Снятие любых ограничений и профитов на 5 минут по всей локе x2
8. Снятие любых ограничений и профитов на 3 минуты в выбранной зоне x5
9. Нерф на локу - стоимость кодов уменьшается в 2 раза по всей локе на 5 минут.
10. Нерф на зону - стомость кодов уменьшается в 2 раза в выбранной зоне на 5 минут x2
11. Бан на перемещения. На глазах агента запрещено перемещаться по зоне в течение 2х минут. 
Двигаться можно, одна нога (опорная) должна всегда стоять на месте x3
'''


class Code:
    def __init__(self, conn):
        self.conn = conn

    def set_code(self, team, code, task_id):
        # val = self.get_code_value(code)
        try:
            sql = 'insert into main.team_code(code, task, team, code_date) ' \
                  'values (:code, :task, :team, current_timestamp)'
            cur = self.conn.cursor()
            cur.execute(sql, {"code": code, "team": team, "task": task_id})
            self.conn.commit()
            cur.close()
            if self.check_team_score(team):
                raise GameEndException()
        except Exception as ex:
            raise CodeError("Код уже введён!")

    def check_code_exists(self, code, task_id):
        sql = '''select * from main.code where task = :task_id and code = :code'''
        cur = self.conn.cursor()
        cur.execute(sql, {"code": code, "task_id": task_id})
        cur.close()
        raise CodeError("Код неверен!") if len(cur.fetchall()) == 0 else None
