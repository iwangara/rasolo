import db
import utils
import emoji
import keyboards
from telegram.ext.dispatcher import run_async
speech = utils.Speech()
sql = db.DBManager()

@run_async
def reply_check(update,context):
    bot_id = update.message.reply_to_message.from_user.id

    user = update.message.from_user

    user_answer = update.message.text
    group_id = update.message.chat.id
    chat_type = update.message.chat.type
    session, level, language = sql.get_user_session_level_language(user.id)
    #check if the user is replying in the group and to the bot's message
    if bot_id == context.bot.id:
        # chat message id
        message_id = update.message.reply_to_message.message_id
        session_type = sql.get_session_type(userid=user.id, msgid=message_id)
        if session_type in ['Apollo','Leizi','Odin','Seshat','Tyche','Zamo']:
            qanswer = sql.get_answer_msgid(userid=user.id, msgid=message_id)
            if utils.stripper(text=user_answer) == utils.stripper(text=qanswer):
                context.bot.delete_message(chat_id=user.id, message_id=message_id)
                pl = context.bot.send_message(chat_id=user.id, text=emoji.emojize(":fire:Your Answer is Correct:fire:",
                                                                                  use_aliases=True),reply_markup=keyboards.next_question(language,session,level))
            else:
                context.bot.delete_message(chat_id=user.id, message_id=message_id)
                context.bot.send_message(chat_id=user.id,
                                         text=emoji.emojize(
                                             f":fire:Your Answer is Incorrect, the correct answer was: <b>{qanswer}</b> :fire:",
                                             use_aliases=True), parse_mode='html',reply_markup=keyboards.next_question(language,session,level))

        elif session_type == ['Nuwa','Gaia']:
            qanswer = sql.get_answer_msgid(userid=user.id, msgid=message_id)
            correct_answer = utils.stripper(text=qanswer)
            try:
                file_id = update.message.voice.file_id
                newFile = context.bot.get_file(file_id)
                newFile.download('gaia_{}.ogg'.format(user.id))
                length = update.message.voice.duration
                if length < 10:
                    new = utils.convert_ogg_to_wav(f"gaia_{user.id}.ogg",
                                                   f"gaia_{user.id}.wav")
                    speech.file = new


                    text = speech.to_text(lang=language.capitalize())
                    utils.mr_logger(f"totext: {text},answer {qanswer}")
                    if text == 401:
                        update.message.reply_text(
                            f"Hi {user.first_name}, I did not understand this, please try again.")
                    elif text == 500:
                        update.message.reply_text(
                            f"Sorry {user.first_name}, I got a little light headed, please try again.")
                    elif text.lower() == correct_answer:
                        context.bot.delete_message(chat_id=user.id, message_id=message_id)
                        context.bot.send_message(chat_id=user.id,
                                                      text=emoji.emojize(":fire:Your Answer is Correct:fire:",
                                                                         use_aliases=True),
                                                      reply_markup=keyboards.next_question(language, session, level))
                    elif text.lower() != correct_answer:
                        context.bot.delete_message(chat_id=user.id, message_id=message_id)
                        context.bot.send_message(chat_id=user.id,
                                                 text=emoji.emojize(
                                                     f":fire:Your Answer is Incorrect, the correct answer was: <b>{qanswer}</b> :fire:",
                                                     use_aliases=True), parse_mode='html',
                                                 reply_markup=keyboards.next_question(language, session, level))
            except:
                pass



