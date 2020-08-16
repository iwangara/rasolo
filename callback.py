import random

from telegram import Poll

import db
import words
import emoji
import utils
import keyboards
from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.dispatcher import run_async

sql = db.DBManager()

@run_async
def cbh(update, context):
    query = update.callback_query
    text = str(query.data)
    user = query.from_user
    session, level, language = sql.get_user_session_level_language(user.id)
    print(text)
    # print(update)
    if text.startswith("play"):
        context.bot.edit_message_text(text=emoji.emojize(":hourglass_flowing_sand:Generating questions please wait.:hourglass_flowing_sand:",use_aliases=True),
                                      inline_message_id=query.inline_message_id)
        game = text.split("+")[1]
        level = text.split("+")[2]
        sql.update_level(user.id, level)
        if game == 'Apollo':
            apollo = sql.get_apollo_question(level, language.capitalize())
            print(apollo)
            if apollo != False:
                try:
                    context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                               message_id=update.callback_query.message.message_id)
                except:
                    pass

                question, answer = apollo

                payload =context.bot.send_message(chat_id=user.id,
                                         text=emoji.emojize(f"{words.Apollo}\n\n<b>{question}</b>", use_aliases=True),reply_markup=ForceReply(),parse_mode='html')
                message_id = payload.result().message_id
                sql.update_user_messageid_answer(user.id,message_id,answer)
            else:
                context.bot.send_message(chat_id=user.id, text=words.QUE_UNVAILABLE,
                                         reply_markup=keyboards.back_key(language=language))
        elif game=="Africa":
            africa = sql.get_africa_question(level, language.capitalize())
            if africa !=False:
                question, answer, answer1, answer2, answer3, answer4 = africa
                pick = [answer1, answer2, answer3, answer4]
                answer = pick[0]

                random.shuffle(pick)
                correct = pick.index(answer)
                payload = context.bot.send_poll(chat_id=user.id, question=question, options=pick,
                                                is_anonymous=True, type=Poll.QUIZ, correct_option_id=correct,
                                                explanation=emoji.emojize(f":fire:Answer: {answer}",
                                                                          use_aliases=True))

                message_id = payload.message_id
                poll_id = payload.poll.id
                correct_id = payload.poll.correct_option_id
                sql.update_user_messageid_answer(user.id, message_id, correct_id)
                sql.update_poll_id(userid=user.id, poll_id=poll_id)
            else:
                context.bot.send_message(chat_id=user.id, text=words.QUE_UNVAILABLE,
                                         reply_markup=keyboards.back_key(language=language))

        elif game == "Gaia":
            gaia = sql.get_gaia_question(level, language.capitalize())


            if gaia !=False:
                question, answer = gaia
                try:
                    context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                               message_id=update.callback_query.message.message_id)
                except:
                    pass


                voice = utils.voice_download(url=question,user_id=user.id)
                payload = context.bot.send_audio(chat_id=user.id, audio=open(voice, 'rb'),
                                                 caption=emoji.emojize(words.GAIA, use_aliases=True), parse_mode='html',reply_markup=ForceReply())
                message_id = payload.result().message_id
                sql.update_user_messageid_answer(user.id, message_id, answer)
            else:
                context.bot.send_message(chat_id=user.id, text=words.QUE_UNVAILABLE,
                                         reply_markup=keyboards.back_key(language=language))
        elif game == 'Leizi':
            leizi = sql.get_leizi_question(level, language.capitalize())
            print(leizi)
            if leizi != False:
                try:
                    context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                               message_id=update.callback_query.message.message_id)
                except:
                    pass
                question, instruction, answer = leizi
                message = f"{words.LEIZI}\n<b>{instruction}</b>\n\n<i>{question}</i>"
                payload =context.bot.send_message(chat_id=user.id,
                                         text=emoji.emojize(message, use_aliases=True),reply_markup=ForceReply(),parse_mode='html')
                message_id = payload.result().message_id
                sql.update_user_messageid_answer(user.id,message_id,answer)
            else:
                context.bot.send_message(chat_id=user.id, text=words.QUE_UNVAILABLE,
                                         reply_markup=keyboards.back_key(language=language))

        elif game == 'Nuwa':
            nuwa = sql.get_nuwa_question(level, language.capitalize())
            print(nuwa)
            if nuwa != False:
                try:
                    context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                               message_id=update.callback_query.message.message_id)
                except:
                    pass

                message = f"<b>{words.NUWA}</b>\n\n<i>{nuwa}</i>"
                payload =context.bot.send_message(chat_id=user.id,
                                         text=emoji.emojize(message, use_aliases=True),reply_markup=ForceReply(),parse_mode='html')
                message_id = payload.result().message_id
                sql.update_user_messageid_answer(user.id,message_id,nuwa)
            else:
                context.bot.send_message(chat_id=user.id, text=words.QUE_UNVAILABLE,
                                         reply_markup=keyboards.back_key(language=language))

        elif game == 'Odin':
            odin = sql.get_odin_question(level, language.capitalize())
            print(odin)
            if odin != False:
                try:
                    context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                               message_id=update.callback_query.message.message_id)
                except:
                    pass
                queId,question,meaning = odin
                key_main = [[InlineKeyboardButton(emoji.emojize(":see_no_evil:", use_aliases=True),
                                                  callback_data=f"sodin+{queId}")]]
                main_markup = InlineKeyboardMarkup(key_main)
                message = f"<b>{words.ODIN}</b>"
                payload = context.bot.send_message(chat_id=user.id,
                                                   text=emoji.emojize(message, use_aliases=True),
                                                   reply_markup=main_markup, parse_mode='html')
                message_id = payload.result().message_id
                sql.update_user_messageid_answer(user.id, message_id, question)
            else:
                context.bot.send_message(chat_id=user.id, text=words.QUE_UNVAILABLE,
                                         reply_markup=keyboards.back_key(language=language))
        elif game == 'Seshat':
            seshat = sql.get_seshat_question(level, language.capitalize())
            print(seshat)
            if seshat != False:
                try:
                    context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                               message_id=update.callback_query.message.message_id)
                except:
                    pass

                question, answer, instruction, gif = seshat
                message = f"<b>{instruction}\n<i>{question}</i>\n\n{words.SESHAT}</b>"
                if "gif" in gif:
                    utils.mr_logger(f"posting gif: {gif}")
                    payload = context.bot.send_document(chat_id=user.id, document=gif,
                                                        caption=emoji.emojize(message, use_aliases=True),
                                                        parse_mode=ParseMode.HTML,reply_markup=ForceReply())
                else:
                    utils.mr_logger(f"posting photo: {gif}")
                    payload = context.bot.send_photo(chat_id=user.id, photo=gif,
                                                     caption=emoji.emojize(message, use_aliases=True),
                                                     parse_mode=ParseMode.HTML,reply_markup=ForceReply())
                    print(payload)
                message_id = payload.result().message_id
                sql.update_user_messageid_answer(user.id, message_id, answer)
            else:
                context.bot.send_message(chat_id=user.id, text=words.QUE_UNVAILABLE,
                                         reply_markup=keyboards.back_key(language=language))
        elif game == 'Tyche':
            tyche = sql.get_tyche_question(level, language.capitalize())
            print(tyche)
            if tyche != False:
                try:
                    context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                               message_id=update.callback_query.message.message_id)
                except:
                    pass

                question, answer = tyche
                message = f"<b>{words.TYCHE}</b>\n\n<i>{question}</i>"
                payload = context.bot.send_message(chat_id=user.id,
                                                   text=emoji.emojize(message, use_aliases=True),
                                                   reply_markup=ForceReply(), parse_mode='html')

                message_id = payload.result().message_id
                sql.update_user_messageid_answer(user.id, message_id, answer)
            else:
                context.bot.send_message(chat_id=user.id, text=words.QUE_UNVAILABLE,
                                         reply_markup=keyboards.back_key(language=language))

        elif game == "Zamo":
            zamo = sql.get_zamo_question(level, language.capitalize())


            if zamo !=False:
                question, answer = zamo
                try:
                    context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                               message_id=update.callback_query.message.message_id)
                except:
                    pass


                voice = utils.voice_download(url=question,user_id=user.id)
                payload = context.bot.send_audio(chat_id=user.id, audio=open(voice, 'rb'),
                                                 caption=emoji.emojize(words.ZAMOL, use_aliases=True), parse_mode='html',reply_markup=ForceReply())
                message_id = payload.result().message_id
                sql.update_user_messageid_answer(user.id, message_id, answer)
            else:
                context.bot.send_message(chat_id=user.id, text=words.QUE_UNVAILABLE,
                                         reply_markup=keyboards.back_key(language=language))

        elif game == "Kadlu":
            kadlu = sql.get_kadlu_main(level, language.capitalize())
            if kadlu !=False:
                try:
                    context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                               message_id=update.callback_query.message.message_id)
                except:
                    pass
                main_id, main_question = kadlu
                string = words.KADLU.split('.')
                fmt = ".\n".join(string)
                message = f"<b>{fmt}</b>"
                voice = utils.voice_download(url=main_question,user_id=user.id)
                payload = context.bot.send_audio(chat_id=user.id, audio=open(voice, 'rb'),
                                                 caption=emoji.emojize(message, use_aliases=True),
                                                 parse_mode='html')
                print(payload)
                try:
                    message_id = payload.result().message_id
                    sql.update_user_messageid_answer(user.id, message_id, 'answer')
                    if 'job' in context.user_data:
                        old_job = context.user_data['job']
                        old_job.schedule_removal()
                    new_job = context.job_queue.run_once(utils.kadlu_job_delete, 180,
                                                         context=[user.id, message_id, main_id])
                    context.user_data['job'] = new_job
                except:
                    context.bot.send_message(chat_id=user.id, text=words.ERROR_OCCURED,
                                             reply_markup=keyboards.back_key(language=language))


            else:
                context.bot.send_message(chat_id=user.id, text=words.QUE_UNVAILABLE,
                                         reply_markup=keyboards.back_key(language=language))

        elif game == "Wala":
            wala = sql.get_wala_main(level, language.capitalize())
            if wala != False:
                try:
                    context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                               message_id=update.callback_query.message.message_id)
                except:
                    pass
                main_id, main_question = wala
                string = words.WALA.split('.')
                fmt = ".\n".join(string)
                message = f"<b>{fmt}</b>\n\n{main_question}"
                payload = context.bot.send_message(chat_id=user.id,
                                                   text=emoji.emojize(message, use_aliases=True),
                                                   parse_mode='html')
                print(payload)
                try:
                    message_id = payload.result().message_id
                    sql.update_user_messageid_answer(user.id, message_id, 'answer')
                    if 'job' in context.user_data:
                        old_job = context.user_data['job']
                        old_job.schedule_removal()
                    new_job = context.job_queue.run_once(utils.wala_job_delete, 10,
                                                         context=[user.id, message_id, main_id])
                    context.user_data['job'] = new_job
                except:
                    context.bot.send_message(chat_id=user.id, text=words.ERROR_OCCURED,
                                             reply_markup=keyboards.back_key(language=language))
            else:
                context.bot.send_message(chat_id=user.id, text=words.QUE_UNVAILABLE,
                                         reply_markup=keyboards.back_key(language=language))



    elif text.startswith("sodin"):
        queId = text.split('+')[1]
        word = sql.get_answer(user.id)
        bot_type = 'Odin'
        tries = sql.check_try(userId=user.id, messageId=update.callback_query.message.message_id, bot=bot_type)
        if tries != True:
            """mark the user as tried the question"""
            sql.create_chance(userId=user.id, messageId=update.callback_query.message.message_id, bot=bot_type)

            context.bot.answer_callback_query(update.callback_query.id,
                                              text=emoji.emojize(f":fire:{word}:fire:", use_aliases=True))
        else:
            context.bot.answer_callback_query(update.callback_query.id,
                                              text=emoji.emojize(f":see_no_evil:You only peep once :see_no_evil:",
                                                                 use_aliases=True))

