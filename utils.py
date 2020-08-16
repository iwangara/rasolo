#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

import emoji
import requests
import logging
import subprocess

from telegram import Poll
import fetcher
import config
import keyboards
import os
import db
import speech_recognition as sr

logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
c_handler.setLevel(logging.ERROR)
f_handler.setLevel(logging.WARNING)
# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

sql = db.DBManager()


class Speech():

    def __init__(self, file=""):
        self.r = sr.Recognizer()
        self._file = file

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        self._file = value

    def to_text(self, lang):
        try:
            harvard = sr.AudioFile(self._file)
            # print(self.file + "******" * 100)
            with harvard as source:
                audio = self.r.record(source)
                # print(audio)
            return self.r.recognize_google(audio, language=lang)
        except sr.WaitTimeoutError:
            return 500
        except sr.UnknownValueError:
            return 401


def mr_logger(message):
    return logger.warning(message)


def convert_ogg_to_wav(ogg_file, wav_file):
    """
    :return: convert ogg file to wav file
    """
    src_filename = ogg_file
    dest_filename = wav_file
    exists = os.path.isfile(wav_file)
    if exists:
        os.remove(wav_file)

    process = subprocess.run(['ffmpeg', '-i', src_filename, dest_filename])
    print(process)
    if process.returncode != 0:
        raise Exception("Something went wrong")
    return dest_filename


def voice_download(url,user_id):
    filename = f'question_{user_id}.mp3'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
        return filename

    else:
        print("Unable to download image")


def botDesc(text):
    if text == "Apollo":
        resp = "🔏APOLLO (sentence syntax)\n" \
               "APOLLO randomizes the words of a sentence and asks the learners to provide the correct answer. Features:\n" \
               "🔹 Capital sensitive\n🔹 Double space tolerance\n🔹 Punctuation sensitive"
        return resp
    elif text == "Africa":
        resp = "👩🏾‍🦱AFRICA (grammar / vocabulary)\nAFRICA delivers multiple choice questions with ONE correct answer."
        return resp
    elif text == "Gaia":
        resp = "GAIA delivers voice based exercises. Learner has to record what she / he heard by replying to the bot. Requirements:\n" \
               "🔹 no background noise\n" \
               "🔹 mic set and good voice quality\n" \
               "🔹 leave half second empty before/ after your recording (don't start to record as soon as you pressed the button and don't release the button as soon as the voice is over)"
        return resp
    elif text == "Kadlu":
        resp = "👩🏾‍🦱KADLU (listening comprehension)\nKADLU delivers listening comprehension exercises. Learner has to listen to an audio. Once the audio is over (usually 3 minutes)," \
               " the audio is deleted and the learner has to answer to questions related to the conversation (audio)."
        return resp
    elif text == "Leizi":
        resp = "🎭LEIZI (grammar)\nLEIZI is an universal type of exercise. It may be used for translation, correct or incorrect type of questions, true or false, etc. "
        return resp
    elif text == "Nuwa":
        resp = "📖NUWA (pronunciation)\nNUWA delivers reading / pronunciation exercises. User has to read / voice record a word / sentence and reply to the bot. Requirements:\n" \
               "🔹 no background noise\n" \
               "🔹 mic set and good voice quality\n" \
               "🔹 leave half second empty before/ after your recording (don't start to record as soon as you pressed the button and don't release the button as soon as the voice is over)"
        return resp
    elif text == "Odin":
        resp = "👁ODIN (vocabulary)\nODIN delivers memory spelling exercises. A word is posted for a few seconds. User has to spell it in the given time. It only works in SOLO mode (not in the group)"
        return resp
    elif text == "Seshat":
        resp = "📸SESHAT (vocabulary)\nSESHAT is an universal type of exercise but supported by graphics. It may be used for translation, correct or incorrect type of questions, true or false, multiple choice, etc. "
        return resp
    elif text == "Tyche":
        resp = "❓TYCHE (vocabulary)\nTYCHE delivers vocabulary exercises (missing letters). A word is posted for a few seconds. User has to spell it in the given time."
        return resp
    elif text == "Wala":
        resp = "📕WALA (reading comprehension)\nWALA delivers reading comprehension exercises. Learner has to read a text. Once the time is over (usually 2 minutes), the text is deleted and the learner has to answer to questions related to the text."
        return resp
    elif text == "Zamo":
        resp = "✒️ZAMO (spelling)\nZAMO delivers voice based exercises. User has to listen and write down / reply to the bot what she / he heard."
        return resp
    elif text == "Help":
        resp = "📙all exercises are time based (answers after the given time are ignored)\n\n📙only the FIRST answer in the given time is graded (anything else is ignored)\n\n" \
               "📙exercise is graded only if the answer is provided by reply (tag) to the bot question\n\n" \
               "📙one Fortuna point is granted for one correct answer (Wala and Kadlu - 2 points)\n\n📙all correct answers (from all respondents in the given time) are graded\n\n" \
               "<a href='https://telegra.ph/Tutorials-RA-V3-08-06'>click here</a>"
        return resp


def levelDesc(level):
    if level == "Elementary":
        resp = "1️⃣ Elementary level selected, select Play to start playing."
        return resp
    elif level == "Intermediate":
        resp = "2️⃣ Intermediate level selected, select Play to start playing."
        return resp
    elif level == "Advanced":
        resp = "3️⃣ Advanced level selected, select Play to start playing."
        return resp
    elif level == "Help":
        resp = "ℹ️ Please select a level then select Play to start playing."
        return resp


# delete spaces on texts
def stripper(text):
    string = text.replace("  ", " ").strip()
    string = string.rstrip(".")
    string = string.lower()
    return string


#job delete message

def kadlu_job_delete(context):
    try:
        job = context.job
        user_id, message_id, main_id = job.context
        session, level, language = sql.get_user_session_level_language(user_id)
        print(user_id, message_id)
        context.bot.delete_message(chat_id=user_id,
                                   message_id=message_id)
        kadlu = sql.get_kadlu_questions_list(main_id)
        if len(kadlu) > 0:
            for tid in kadlu:
                kadlu_first = sql.get_kadlu_qstn_by_id(tid)

                if kadlu_first != False:
                    question, answer1, answer2, answer3, answer4 = kadlu_first
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
            context.bot.send_message(chat_id=user_id,
                                     text=emoji.emojize(":fire:Select an option below after you have finished answering the questions :backhand_index_pointing_down:",
                                                        use_aliases=True),
                                     reply_markup=keyboards.next_question(language, session, level))

    except:
        pass



def wala_job_delete(context):
    try:
        job = context.job
        user_id, message_id, main_id = job.context
        session, level, language = sql.get_user_session_level_language(user_id)
        print(user_id, message_id)
        context.bot.delete_message(chat_id=user_id,
                                   message_id=message_id)
        kadlu = sql.get_wala_questions_list(main_id)
        if len(kadlu) > 0:
            for tid in kadlu:
                kadlu_first = sql.get_wala_qstn_by_id(tid)

                if kadlu_first != False:
                    question, answer1, answer2, answer3, answer4 = kadlu_first
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
            context.bot.send_message(chat_id=user_id,
                                     text=emoji.emojize(":fire:Select an option below after you have finished answering the questions :backhand_index_pointing_down:",
                                                        use_aliases=True),
                                     reply_markup=keyboards.next_question(language, session, level))

    except:
        pass



def init():
    for language in config.LANGUAGES:
        fetcher.fetch_wala(language)
        fetcher.fetch_kadlu(language)
        fetcher.fetch_zamo(language)
        fetcher.fetch_tyche(language)
        fetcher.fetch_seshat(language)
        fetcher.fetch_odin(language)
        fetcher.fetch_nuwa(language)
        fetcher.fetch_leizi(language)
        fetcher.fetch_gaia(language)
        fetcher.fetch_africa(language)
        fetcher.fetch_apollo(language)





