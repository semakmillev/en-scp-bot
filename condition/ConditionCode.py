# -*- coding: utf-8 -*-
import sqlite3

from db import create, GameEndException, set_admin_message
from db.code import Code, CodeError

sql_action = '''
  select a.action_type, t.zone 
    from action_code a,
         team_condition_code t
   where a._code = t._code
    and datetime(datetime('now'), "+3 hours") < datetime(datetime(code_date), "+"||a.duration||" minutes")
    order by action_type
'''



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
1. Блокировка всех кодов на 3 минуты x 3 
2. Блокировка всех кодов на 2 минуты x4
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


class ConditionCode(Code):
    def __init__(self, conn):
        super(ConditionCode, self).__init__(conn)

    def get_code_info(self, code):
        cur = self.conn.cursor()
        sql = '''select * from action_code where "_code" = :code'''
        cur.execute(sql, {"code": code})
        rows = cur.fetchall()
        if len(rows) == 0:
            sql = '''select * from simple_code where "_code"= :code'''
            cur.execute(sql, {"code": code})
            simple_rows = cur.fetchall()
            if len(simple_rows) == 0:
                raise CodeError("Код неверен!")
            else:
                return "SIMPLE", self.get_code_value(code), simple_rows[0]["zone"], None, None, 0
        else:
            return "ACTION", None, None, rows[0]["action_text"], rows[0]["action_type"], rows[0]["duration"]

    def put_code(self, team, code):
        splited_code = code.split(':')
        engine_code = splited_code[0]
        super(Code, self).check_code_exists(engine_code, 1)
        code_type, val, zone, return_text, action_type, duration = self.get_code_info(engine_code)
        if action_type is not None:
            if action_type.find('ZONE'):
                if len(splited_code) == 1:
                    raise CodeError("Данный код существует, однако вы не указали зону его действия. "
                                    "Чтобы активировать его вбейте *КОД*:*№ Зоны*")
                else:
                    zone = int(splited_code[1])
                    self.set_code(team, engine_code, zone, val, time_delay=1)
                    set_admin_message(return_text + "Событие началось!" % zone, code_type, 1)
                    set_admin_message(return_text + "Cобытие закроется через минуту!" % zone, code_type, int(duration))
                    set_admin_message(return_text + "Cобытие закончилось!" % zone, code_type, int(duration) + 1)
                    # self.set_code_zone(team, engine_code, int(splited_code[1]))
                    return return_text + " Старт через минуту!" % zone, code_type
            else:
                self.set_code(team, engine_code, None, val, time_delay=1)
                set_admin_message(return_text + "Cобытие закроется через минуту!" %  code_type, int(duration) - 1)
                set_admin_message(return_text + "Cобытие закончилось!" % code_type, int(duration))
                # self.set_code_zone(team, engine_code, int(splited_code[1]))
                return return_text + " Событие началось!" %  code_type

        return return_text, code_type

    def set_code_zone(self, team, code, zone):
        raise Exception("Сюда идти не надо!")
        sql = '''select * from main.team_code where "_code"=:code and team = :team'''
        cur = self.conn.cursor()
        cur.execute(sql, {"code": code, "team": team})
        row = cur.fetchall()[0]
        zone = int(row["zone"])
        raise CodeError("Коду уже задана зона, и он наверняка действует") if zone != -1 else None
        sql = '''update main.team_code set zone=:zone where _code=:code and team=:team '''
        cur.execute(sql, {"code": code, "team": team, "zone": zone})
        self.conn.commit()
        cur.close()

    def set_code(self, team, code, zone=-1, val=None, time_delay=0):
        super(ConditionCode, self).set_code(team, code, 2)
        try:

            sql = 'insert into main.team_code("_code", team, code_date, zone, code_value) ' \
                  'values (:code, :team, datetime("now", "localtime", "+"|| :delay ||" minutes"), :zone, :code_value)'
            cur = self.conn.cursor()
            cur.execute(sql, {"code": code, "team": team, "zone": zone, "code_value": val, ":delay": time_delay})
            self.conn.commit()
            cur.close()
            if self.check_team_score(team):
                raise GameEndException()
        except Exception as ex:
            raise CodeError("Код уже введён!")

    def get_code_value(self, code):
        value = 32
        sql = '''select * from simple_code where "_code" = :code'''
        cur = self.conn.cursor()
        cur.execute(sql, {"code": code})
        code_zone = int(cur.fetchall()[0]["zone"])
        cur.execute(sql_action)
        rows = cur.fetchall()
        if len(rows) == 0:
            return 0
        for row in rows:
            if row["action_type"] == "IGNORE":
                return 32
            if row["action_type"] == "IGNORE_ZONE" and code_zone == row["zone"]:
                return 32
            if row["action_type"] == "STOP":
                raise CodeError("В данный момент запрещено вводить коды с локации!")
            if row["action_type"] == "BUST":
                value *= 2
            if row["action_type"] == "BUST_ZONE" and row["zone"] == code_zone:
                value *= 2
            if row["action_type"] == "DOWN":
                value /= 2
            if row["action_type"] == "DOWN_ZONE" and row["zone"] == code_zone:
                value /= 2
        return value

