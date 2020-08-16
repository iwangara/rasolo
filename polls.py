import random

import emoji
from telegram import Poll
import keyboards
import words
import db

sql = db.DBManager()


def polls_manager(update,context):
    try:
        poll_id = update.poll.id

        if update.poll.is_closed:
            return
        user_id = sql.get_userid_poll_id(poll_id)
        session, level, language = sql.get_user_session_level_language(user_id)
        if session == 'Africa':
            user_id, message_id, session = sql.get_africa_message_id(poll_id)
            context.bot.delete_message(chat_id=user_id, message_id=message_id)
            africa = sql.get_africa_question(level, language.capitalize())

            if africa != False:
                question, answer, answer1, answer2, answer3, answer4 = africa
                pick = [answer1, answer2, answer3, answer4]
                answer = pick[0]

                random.shuffle(pick)
                correct = pick.index(answer)
                payload = context.bot.send_poll(chat_id=user_id, question=question, options=pick,
                                                is_anonymous=True, type=Poll.QUIZ, correct_option_id=correct,
                                                explanation=emoji.emojize(f":fire:Answer: {answer}",
                                                                          use_aliases=True))

                message_id = payload.message_id
                poll_id = payload.poll.id
                correct_id = payload.poll.correct_option_id
                sql.update_user_messageid_answer(user_id, message_id, correct_id)
                sql.update_poll_id(userid=user_id, poll_id=poll_id)
            else:
                context.bot.send_message(chat_id=user_id, text=words.QUE_UNVAILABLE,
                                         reply_markup=keyboards.back_key(language=language))



    except:
        pass

