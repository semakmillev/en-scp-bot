# -*- coding: utf-8 -*-
from db.code import CodeError
from study.Team import StudyTeam


def study_job(bot , chat_id, searcher):
    #bot.sendMessage(chat_id, "Сообщение!")
    res = searcher.do_search()
    bot.sendMessage(chat_id, res) if res is not None else None


def study_handler(bot, msg, con, team_name):
    team = StudyTeam(con)

    chat_id = msg["chat"]["id"]
    reply_to_message_id = msg['message_id']
    message_text = '%s' % msg['text'].encode("utf-8")
    try:
        return_text = team.set_study_code.put_code(team_name, message_text.upper())
        print return_text
    except CodeError as ex:
        bot.sendMessage(chat_id, ex.msg, reply_to_message_id=reply_to_message_id)
        return