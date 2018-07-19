# -*- coding: utf-8 -*-
from condition.ConditionCode import ConditionCode
from condition.ConditionTeam import ConditionTeam
from db import GameEndException
from db.code import CodeError


def condition_handler(bot, msg, con, team_name):
    team = ConditionTeam(con)
    code = ConditionCode(con)
    chat_id = msg["chat"]["id"]
    reply_to_message_id = msg['message_id']
    message_text = '%s' % msg['text'].encode("utf-8")
    if message_text == '/theend?':
        try:
            raise GameEndException() if code.check_team_score(team) else None
            score = code.get_team_score(team)
            bot.sendMessage(chat_id, 'Ваша команда набрала пока ещё только %s очков а надо 960' % score)
            return
        except GameEndException as ex:
            bot.sendMessage(chat_id, ex.msg)
            return

    if message_text == '/score':
        score = code.get_team_score(team)
        bot.sendMessage(chat_id, 'Ваша команда набрала %s очков' % score)
        return

    # print msg['chat']['type']
    try:
        return_text, code_type = code.put_code(team_name, message_text.upper())
        print code_type
        if code_type == 'ACTION':
            bot.sendMessage(chat_id="@enscp", text=return_text)
            bot.sendMessage(chat_id, "Код принят! %s" % message_text, reply_to_message_id=reply_to_message_id)
            return
    except CodeError as ex:
        bot.sendMessage(chat_id, ex.msg, reply_to_message_id=reply_to_message_id)
        return