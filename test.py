#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from uuid import uuid4
import config
import utils
import db
import words
import emoji
import polls
import keyboards
import reply_manager
import callback
from telegram import InlineQueryResultArticle,InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackQueryHandler, PicklePersistence, \
    MessageHandler, Filters, PollHandler
from telegram.utils.helpers import mention_html
from telegram.ext.dispatcher import run_async
from telegram.utils.request import Request
from telegram.error import BadRequest
from telegram.ext import messagequeue as mq
import telegram.bot

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
sql = db.DBManager()


@run_async
def start(update, context):
    user = update.message.from_user
    chat_type = update.message.chat.type
    if chat_type == "private":
        if sql.check_user(user.id) == False:
            sql.create_user(user.id)
        context.bot.send_message(chat_id=user.id,
                                 text=words.WELCOME.format(mention_html(user.id, user.first_name)),
                                 reply_markup=keyboards.main_menu(), parse_mode="html")


@run_async
def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    user = update.inline_query.from_user
    print(query in config.EXERCISES)

    try:
        if query in config.LANGUAGES:
            sql.update_language(user.id, query)
            bots = [
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="⬆️Pull up to view available exercises⬆️",
                    thumb_url="https://telegra.ph/file/00c7a1784fd07059b0bb1.png",
                    input_message_content=InputTextMessageContent(utils.botDesc('Help'), parse_mode="HTML")),
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="APOLLO (sentence syntax)",
                    description="APOLLO randomizes the words of a sentence and asks the learners to provide the correct answer.",
                    thumb_url="https://telegra.ph/file/a54ef5be07aded5e3fe7f.jpg",
                    input_message_content=InputTextMessageContent(utils.botDesc('Apollo'), parse_mode="HTML"),
                    reply_markup=keyboards.sub_menu(bot_type="Apollo", language=query, context=context)),
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="👩🏾‍🦱AFRICA (grammar / vocabulary)",
                    description="AFRICA delivers multiple choice questions with ONE correct answer.",
                    thumb_url="https://telegra.ph/file/ec572bac09a221b1c4cef.jpg",
                    input_message_content=InputTextMessageContent(utils.botDesc('Africa'), parse_mode="HTML"),
                    reply_markup=keyboards.sub_menu(bot_type="Africa", language=query, context=context)),
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="🎙GAIA (pronunciation)",
                    description="GAIA delivers voice based exercises. Learner has to record what she / he heard by replying to the bot.",
                    thumb_url="https://telegra.ph/file/bd1fec03cc0ba37202ec2.jpg",
                    input_message_content=InputTextMessageContent(utils.botDesc('Gaia'), parse_mode="HTML"),
                    reply_markup=keyboards.sub_menu(bot_type="Gaia", language=query, context=context)),
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="👩🏾‍🦱KADLU (listening comprehension)",
                    description="KADLU delivers listening comprehension exercises. Learner has to listen to an audio. Once the audio is over (usually 3 minutes), the audio is deleted and the learner has to answer to questions related to the conversation (audio)",
                    thumb_url="https://telegra.ph/file/34696b239740a11283819.jpg",
                    input_message_content=InputTextMessageContent(utils.botDesc('Kadlu'), parse_mode="HTML"),
                    reply_markup=keyboards.sub_menu(bot_type="Kadlu", language=query, context=context)),
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="🎭LEIZI (grammar)",
                    description="LEIZI is an universal type of exercise. It may be used for translation, correct or incorrect type of questions, true or false, etc. ",
                    thumb_url="https://telegra.ph/file/ba16129c1fb623c26dec8.jpg",
                    input_message_content=InputTextMessageContent(utils.botDesc('Leizi'), parse_mode="HTML"),
                    reply_markup=keyboards.sub_menu(bot_type="Leizi", language=query, context=context)),
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="📖NUWA (pronunciation)",
                    description="NUWA delivers reading / pronunciation exercises. User has to read / voice record a word / sentence and reply to the bot.",
                    thumb_url="https://telegra.ph/file/3464381f488f63cf3f8d9.jpg",
                    input_message_content=InputTextMessageContent(utils.botDesc('Nuwa'), parse_mode="HTML"),
                    reply_markup=keyboards.sub_menu(bot_type="Nuwa", language=query, context=context)),
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="👁ODIN (vocabulary)",
                    description="ODIN delivers memory spelling exercises. A word is posted for a few seconds. User has to spell it in the given time.",
                    thumb_url="https://telegra.ph/file/eeb194693623b8e65e485.jpg",
                    input_message_content=InputTextMessageContent(utils.botDesc('Odin'), parse_mode="HTML"),
                    reply_markup=keyboards.sub_menu(bot_type="Odin", language=query, context=context)),
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="📸SESHAT (vocabulary)",
                    description="SESHAT is an universal type of exercise but supported by graphics. It may be used for translation, correct or incorrect type of questions, true or false, multiple choice, etc. ",
                    thumb_url="https://telegra.ph/file/c817da6ec09bac6e86b36.jpg",
                    input_message_content=InputTextMessageContent(utils.botDesc('Seshat'), parse_mode="HTML"),
                    reply_markup=keyboards.sub_menu(bot_type="Seshat", language=query, context=context)),
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="❓TYCHE (vocabulary)",
                    description="TYCHE delivers vocabulary exercises (missing letters). A word is posted for a few seconds. User has to spell it in the given time.",
                    thumb_url="https://telegra.ph/file/ce22e77dd6430daec1590.jpg",
                    input_message_content=InputTextMessageContent(utils.botDesc('Tyche'), parse_mode="HTML"),
                    reply_markup=keyboards.sub_menu(bot_type="Tyche", language=query, context=context)),
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="📕WALA (reading comprehension)",
                    description="WALA delivers reading comprehension exercises. Learner has to read a text. Once the time is over (usually 2 minutes), the text is deleted and the learner has to answer to questions related to the text.",
                    thumb_url="https://telegra.ph/file/ca953a4310dc97442f91d.jpg",
                    input_message_content=InputTextMessageContent(utils.botDesc('Wala'), parse_mode="HTML"),
                    reply_markup=keyboards.sub_menu(bot_type="Wala", language=query, context=context)),
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="✒️ZAMO (spelling)",
                    description="ZAMO delivers voice based exercises. User has to listen and write down / reply to the bot what she / he heard.",
                    thumb_url="https://telegra.ph/file/e7e8054fa0f012e110274.jpg",
                    input_message_content=InputTextMessageContent(utils.botDesc('Zamo'), parse_mode="HTML"),
                    reply_markup=keyboards.sub_menu(bot_type="Zamo", language=query, context=context)),

                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Help",
                    description="For more info send /help ",
                    thumb_url="https://telegra.ph/file/00c7a1784fd07059b0bb1.png",
                    input_message_content=InputTextMessageContent(utils.botDesc('Help'), parse_mode="HTML"))
            ]

            update.inline_query.answer(bots, cache_time=0)
        elif query in config.EXERCISES:
            sql.update_session(user.id, query)
            session, level, language = sql.get_user_session_level_language(user.id)
            print(session, level)
            exercises = [
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="⬆️Pull up to select questions proficiency level.⬆️",
                    thumb_url="https://telegra.ph/file/00c7a1784fd07059b0bb1.png",
                    input_message_content=InputTextMessageContent(utils.levelDesc('Help'), parse_mode="HTML")),
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Elementary",
                    description="Best questions for beginners.",
                    thumb_url="https://telegra.ph/file/0b7cd50e331d30cc4b707.png",
                    input_message_content=InputTextMessageContent(utils.levelDesc('Elementary'), parse_mode="HTML"),
                    reply_markup=keyboards.play_menu(bot_type=session, language=query, level='Elementary',
                                                     context=context)),
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Intermediate",
                    description="Best questions for intermediate students.",
                    thumb_url="https://telegra.ph/file/e2edb500a70e434977f11.png",
                    input_message_content=InputTextMessageContent(utils.levelDesc('Intermediate'), parse_mode="HTML"),
                    reply_markup=keyboards.play_menu(bot_type=session, language=query, level='Intermediate',
                                                     context=context)),
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Advanced",
                    description="Best questions for advanced students.",
                    thumb_url="https://telegra.ph/file/89fd8120a81d26cf67e82.png",
                    input_message_content=InputTextMessageContent(utils.levelDesc('Advanced'), parse_mode="HTML"),
                    reply_markup=keyboards.play_menu(bot_type=session, language=query, level='Advanced',
                                                     context=context)),
            ]
            update.inline_query.answer(exercises, cache_time=0)




    except:
        pass


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


class MQBot(telegram.bot.Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''

    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(MQBot, self).__del__()

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        logger.info("native send message method called")
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).send_message(*args, **kwargs)
        except Exception as e:
            print(e)
            logger.warning(e)
            return e

    @mq.queuedmessage
    def edit_message_text(self, *args, **kwargs):
        logger.info("native edit message method called")
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))

        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        try:
            return super(MQBot, self).edit_message_text(*args, **kwargs)
        except:
            pass

    @mq.queuedmessage
    def pin_chat_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
                OPTIONAL arguments'''
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).pin_chat_message(*args, **kwargs)
        except BadRequest:
            pass

    @mq.queuedmessage
    def answer_callback_query(self, *args, **kwargs):
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).answer_callback_query(*args, **kwargs)
        except:
            pass

    @mq.queuedmessage
    def unpin_chat_message(self, *args, **kwargs):
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).unpin_chat_message(*args, **kwargs)
        except BadRequest:
            pass

    @mq.queuedmessage
    def send_audio(self, *args, **kwargs):
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).send_audio(*args, **kwargs)
        except:
            pass

    @mq.queuedmessage
    def send_document(self, *args, **kwargs):
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).send_document(*args, **kwargs)
        except:
            pass

    @mq.queuedmessage
    def send_video(self, *args, **kwargs):
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).send_video(*args, **kwargs)
        except:
            pass

    @mq.queuedmessage
    def send_photo(self, *args, **kwargs):
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).send_photo(*args, **kwargs)
        except:
            pass

    @mq.queuedmessage
    def send_voice(self, *args, **kwargs):
        logger.info("Current Message Queue size: {}".format(
            self._msg_queue._all_delayq._queue.qsize()
        ))
        try:
            return super(MQBot, self).send_voice(*args, **kwargs)
        except:
            pass


def main():
    """Instanciate a Defaults object"""

    # Create the EventHandler and pass it your bot's token.
    q = mq.MessageQueue(all_burst_limit=29, all_time_limit_ms=1017, group_burst_limit=15, group_time_limit_ms=55000,
                        autostart=True)
    # set connection pool size for bot
    request = Request(con_pool_size=36)
    testbot = MQBot(config.TOKEN, request=request, mqueue=q)
    pp = PicklePersistence(filename='rabot', store_bot_data=True,store_chat_data=True,store_user_data=True)
    updater = telegram.ext.updater.Updater(bot=testbot, use_context=True, workers=32)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_handler(CallbackQueryHandler(callback.cbh))
    dp.add_handler(MessageHandler(Filters.reply & (Filters.text | Filters.voice), reply_manager.reply_check))
    dp.add_handler(PollHandler(polls.polls_manager))
    # dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
