#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from threading import Lock

lock = Lock()


class DBManager:

    def __init__(self, dbname="solo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False, timeout=20)
        self.c = self.conn.cursor()

    def setup(self):
        tbl_seshat = """CREATE TABLE IF NOT EXISTS seshat(id INTEGER PRIMARY KEY,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,instruction VARCHAR DEFAULT NULL,gif VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,bot VARCHAR DEFAULT NULL)"""
        tbl_odin = """CREATE TABLE IF NOT EXISTS odin(id INTEGER PRIMARY KEY,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,meaning VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,bot VARCHAR DEFAULT NULL)"""
        tbl_leizi = """CREATE TABLE IF NOT EXISTS leizi(id INTEGER PRIMARY KEY,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,answer1 VARCHAR DEFAULT NULL,answer2 VARCHAR DEFAULT NULL,instruction VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,bot VARCHAR DEFAULT NULL)"""
        tbl_gaia = """CREATE TABLE IF NOT EXISTS gaia(id INTEGER PRIMARY KEY,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,bot VARCHAR DEFAULT NULL)"""
        tbl_africa = """CREATE TABLE IF NOT EXISTS africa(id INTEGER PRIMARY KEY,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,answer1 VARCHAR DEFAULT NULL,answer2 VARCHAR DEFAULT NULL,answer3 VARCHAR DEFAULT NULL,answer4 VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,bot VARCHAR DEFAULT NULL)"""
        tbl_apollo = """CREATE TABLE IF NOT EXISTS apollo(id INTEGER PRIMARY KEY,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,bot VARCHAR DEFAULT NULL)"""
        tbl_users = """CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,userid INTEGER DEFAULT NULL,answer VARCHAR DEFAULT NULL,message_id INTEGER DEFAULT NULL,poll_id INTEGER DEFAULT NULL,session VARCHAR DEFAULT NULL,language VARCHAR DEFAULT NULL,correct INTEGER DEFAULT 0,level VARCHAR DEFAULT 0)"""
        tbl_nuwa = """CREATE TABLE IF NOT EXISTS nuwa(id INTEGER PRIMARY KEY,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,bot VARCHAR DEFAULT NULL)"""
        tbl_chances = """CREATE TABLE IF NOT EXISTS chances(id INTEGER PRIMARY KEY,userId INTEGER DEFAULT NULL ,tries INTEGER DEFAULT 0,bot DEFAULT NULL,messageId INTEGER DEFAULT NULL )"""
        tbl_tyche = """CREATE TABLE IF NOT EXISTS tyche(id INTEGER PRIMARY KEY,quesId INTEGER DEFAULT NULL ,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,bot VARCHAR DEFAULT NULL)"""
        tbl_zamo = """CREATE TABLE IF NOT EXISTS zamo(id INTEGER PRIMARY KEY,quesId INTEGER DEFAULT NULL ,answer VARCHAR DEFAULT NULL,question VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,bot VARCHAR DEFAULT NULL)"""
        tbl_kadlu = """CREATE TABLE IF NOT EXISTS kadlu (id INTEGER PRIMARY KEY,quesId INTEGER DEFAULT NULL ,main_id INTEGER DEFAULT NULL ,main_question VARCHAR DEFAULT NULL,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,answer1 VARCHAR DEFAULT NULL,answer2 VARCHAR DEFAULT NULL,answer3 VARCHAR DEFAULT NULL,answer4 VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,bot VARCHAR DEFAULT NULL)"""
        tbl_wala = """CREATE TABLE IF NOT EXISTS wala (id INTEGER PRIMARY KEY,quesId INTEGER DEFAULT NULL ,main_id INTEGER DEFAULT NULL ,main_question VARCHAR DEFAULT NULL,question VARCHAR DEFAULT NULL,answer VARCHAR DEFAULT NULL,answer1 VARCHAR DEFAULT NULL,answer2 VARCHAR DEFAULT NULL,answer3 VARCHAR DEFAULT NULL,answer4 VARCHAR DEFAULT NULL,qlevel VARCHAR DEFAULT NULL,qlanguage VARCHAR DEFAULT NULL,bot VARCHAR DEFAULT NULL)"""
        self.c.execute(tbl_wala)
        self.c.execute(tbl_kadlu)
        self.c.execute(tbl_zamo)
        self.c.execute(tbl_tyche)
        self.c.execute(tbl_chances)
        self.c.execute(tbl_seshat)
        self.c.execute(tbl_odin)
        self.c.execute(tbl_leizi)
        self.c.execute(tbl_nuwa)
        self.c.execute(tbl_gaia)
        self.c.execute(tbl_africa)
        self.c.execute(tbl_apollo)
        self.c.execute(tbl_users)
        self.conn.commit()


#################WALA###################
    def check_wala(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM wala WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_wala(self, quesId, main_id, main_question, question, answer, answer1, answer2, answer3, answer4, qlevel,
                  qlanguage,
                  bot='wala'):
        if self.check_wala(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO wala(quesId,main_id,main_question,question, answer, answer1, answer2, answer3, answer4,  qlevel, qlanguage,bot) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    quesId, main_id, main_question, question, answer, answer1, answer2, answer3, answer4, qlevel,
                    qlanguage,
                    bot))
            lock.release()
            self.conn.commit()

    def get_wala_main(self,level,language):
        self.c.execute("SELECT main_id,main_question FROM wala WHERE qlevel=? AND qlanguage=? ORDER BY RANDOM() LIMIT 1",(level,language))
        que = self.c.fetchone()
        if que is not None:
            return que
        else:
            return False

    def get_wala_questions_list(self,main_id):
        wala =[]
        for que in self.c.execute("SELECT quesId FROM wala WHERE main_id=?",(main_id, )):
            wala.append(que[0])
        return wala

    def get_wala_qstn_by_id(self, tid):
        self.c.execute("SELECT question, answer1, answer2, answer3, answer4 FROM wala WHERE quesId=?", (tid,))
        min_id = self.c.fetchone()
        if min_id is not None:
            return min_id
        else:
            return False


################KADLU###############
    def check_kadlu(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM kadlu WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_kadlu(self, quesId, main_id, main_question, question, answer, answer1, answer2, answer3, answer4, qlevel,
                   qlanguage,
                   bot='kadlu'):
        if self.check_kadlu(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO kadlu(quesId,main_id,main_question,question, answer, answer1, answer2, answer3, answer4,  qlevel, qlanguage,bot) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    quesId, main_id, main_question, question, answer, answer1, answer2, answer3, answer4, qlevel,
                    qlanguage,
                    bot))
            lock.release()
            self.conn.commit()

    def get_kadlu_main(self,level,language):
        self.c.execute("SELECT main_id,main_question FROM kadlu WHERE qlevel=? AND qlanguage=? ORDER BY RANDOM() LIMIT 1",(level,language))
        que = self.c.fetchone()
        if que is not None:
            return que
        else:
            return False

    def get_kadlu_questions_list(self,main_id):
        kadlu =[]
        for que in self.c.execute("SELECT quesId FROM kadlu WHERE main_id=?",(main_id, )):
            kadlu.append(que[0])
        return kadlu

    def get_kadlu_qstn_by_id(self, tid):
        self.c.execute("SELECT question, answer1, answer2, answer3, answer4 FROM kadlu WHERE quesId=?", (tid,))
        min_id = self.c.fetchone()
        if min_id is not None:
            return min_id
        else:
            return False


#######################ZAMO##################
    def check_zamo(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM zamo WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_zamo(self, quesId, question, answer, qlevel, qlanguage, bot='zamo'):
        if self.check_zamo(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO zamo(quesId ,question,answer,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?)",
                (quesId, question, answer, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def get_zamo_question(self,level,language):
        self.c.execute("SELECT question,answer FROM zamo WHERE qlevel=? AND qlanguage=? ORDER BY RANDOM() LIMIT 1",(level,language))
        que = self.c.fetchone()
        if que is not None:
            return que
        else:
            return False



##############TYCHE######################
    def check_tyche(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM tyche WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_tyche(self, quesId, question, answer, qlevel, qlanguage, bot='tyche'):
        if self.check_tyche(quesId) == False:
            lock.acquire(True)
            self.c.execute("INSERT INTO tyche(quesId, question,answer,qlevel, qlanguage,bot) VALUES (?,?,?,?,?,?)",
                           (quesId, question, answer, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def get_tyche_question(self,level,language):
        self.c.execute("SELECT question,answer FROM tyche WHERE qlevel=? AND qlanguage=? ORDER BY RANDOM() LIMIT 1",(level,language))
        que = self.c.fetchone()
        if que is not None:
            return que
        else:
            return False


##############SESHAT############################
    def check_seshat(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM seshat WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_seshat(self, quesId, question, answer, instruction, gif, qlevel, qlanguage, bot='seshat'):
        if self.check_seshat(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO seshat(quesId, question,answer,instruction,gif,qlevel, qlanguage,bot) VALUES (?,?,?,?,?,?,?,?)",
                (quesId, question, answer, instruction, gif, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def get_seshat_question(self,level,language):
        self.c.execute("SELECT question,answer,instruction,gif FROM seshat WHERE qlevel=? AND qlanguage=? ORDER BY RANDOM() LIMIT 1",(level,language))
        que = self.c.fetchone()
        if que is not None:
            return que
        else:
            return False

##############ODIN########################################
    def check_try(self, userId, messageId, bot):
        lock.acquire(True)
        self.c.execute("SELECT tries FROM chances WHERE userId=? and messageId=? and bot=?", (userId, messageId, bot))
        lock.release()
        tries = self.c.fetchone()
        if tries is not None:
            return tries[0]
        else:
            return False

    def create_chance(self, userId, messageId, bot, chance=1):
        lock.acquire(True)
        self.c.execute("INSERT INTO chances(userId,messageId,bot,tries) VALUES (?,?,?,?)",
                       (userId, messageId, bot, chance))
        lock.release()
        self.conn.commit()

    def delete_chance(self, messageId):
        lock.acquire(True)
        self.c.execute("DELETE FROM chances WHERE messageId=?", (messageId,))
        lock.release()
        self.conn.commit()

    def check_odin(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM odin WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_odin(self, quesId, question, meaning, qlevel, qlanguage, bot='odin'):
        if self.check_odin(quesId) == False:
            lock.acquire(True)
            self.c.execute("INSERT INTO odin(quesId, question,meaning,qlevel, qlanguage,bot) VALUES (?,?,?,?,?,?)",
                           (quesId, question, meaning, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def get_odin_question(self,level,language):
        self.c.execute("SELECT id,question,meaning FROM odin WHERE qlevel=? AND qlanguage=? ORDER BY RANDOM() LIMIT 1",(level,language))
        que = self.c.fetchone()
        if que is not None:
            return que
        else:
            return False

######################NUWA##################################
    def check_nuwa(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM nuwa WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_nuwa(self, quesId, question, qlevel, qlanguage, bot='nuwa'):
        if self.check_nuwa(quesId) == False:
            lock.acquire(True)
            self.c.execute("INSERT INTO nuwa(quesId, question,qlevel, qlanguage,bot) VALUES (?,?,?,?,?)",
                           (quesId, question, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def get_nuwa_question(self,level,language):
        self.c.execute("SELECT question FROM nuwa WHERE qlevel=? AND qlanguage=? ORDER BY RANDOM() LIMIT 1",(level,language))
        que = self.c.fetchone()
        if que is not None:
            return que[0]
        else:
            return False

####################LEIZI###################################
    def check_leizi(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM leizi WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_leizi(self, quesId, question, answer1, answer2, instruction, qlevel, qlanguage, bot='leizi'):
        if self.check_leizi(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO leizi(quesId, question, answer1, answer2,instruction,qlevel, qlanguage,bot) VALUES (?,?,?,?,?,?,?,?)",
                (quesId, question, answer1, answer2, instruction, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def get_leizi_question(self,level,language):
        self.c.execute("SELECT question,instruction,answer1 FROM leizi WHERE qlevel=? AND qlanguage=? ORDER BY RANDOM() LIMIT 1",(level,language))
        que = self.c.fetchone()
        if que is not None:
            return que
        else:
            return False


####################GAIA##################################
    def check_gaia(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM gaia WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_gaia(self, quesId, question, answer, qlevel, qlanguage, bot='gaia'):
        if self.check_gaia(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO gaia(quesId ,question,answer,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?)",
                (quesId, question, answer, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def get_gaia_question(self,level,language):
        self.c.execute("SELECT question,answer FROM gaia WHERE qlevel=? AND qlanguage=? ORDER BY RANDOM() LIMIT 1",(level,language))
        que = self.c.fetchone()
        if que is not None:
            return que
        else:
            return False

####################AFRICA############################
    def check_africa(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM africa WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_africa(self, quesId, answer, answer1, answer2, answer3, answer4, question, qlevel, qlanguage,
                    bot='africa'):
        if self.check_africa(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO africa(quesId ,answer,answer1,answer2,answer3,answer4,question ,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (quesId, answer, answer1, answer2, answer3, answer4, question, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def get_africa_question(self,level,language):
        self.c.execute(
            "SELECT question,answer, answer1, answer2, answer3, answer4 FROM africa WHERE qlevel=? AND qlanguage=? ORDER BY RANDOM() LIMIT 1",(level,language))
        que = self.c.fetchone()
        if que is not None:
            return que
        else:
            return False

    def get_africa_message_id(self, pollid):
        self.c.execute("SELECT userid,message_id,session FROM users WHERE poll_id=?", (pollid,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot
        else:
            return False

    def get_userid_poll_id(self,poll_id):
        self.c.execute("SELECT userid FROM users WHERE poll_id=?", (poll_id,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

################SAVE APOLLO#######################
    def check_apollo(self, queId):
        lock.acquire(True)
        self.c.execute("SELECT quesId FROM apollo WHERE quesId=?", (queId,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def save_apollo(self, quesId, question, answer, qlevel, qlanguage, bot='apollo'):
        if self.check_apollo(quesId) == False:
            lock.acquire(True)
            self.c.execute(
                "INSERT INTO apollo(quesId ,question,answer,qlevel ,qlanguage,bot) VALUES (?,?,?,?,?,?)",
                (quesId, question, answer, qlevel, qlanguage, bot))
            lock.release()
            self.conn.commit()

    def get_apollo_question(self,level,language):
        self.c.execute("SELECT question,answer FROM apollo WHERE qlevel=? AND qlanguage=? ORDER BY RANDOM() LIMIT 1",(level,language))
        que = self.c.fetchone()
        if que is not None:
            return que
        else:
            return False
################################MANAGE USERS ##########################
    def check_user(self, userid):
        lock.acquire(True)
        self.c.execute("SELECT userid FROM users WHERE userid=?", (userid,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return True
        else:
            return False

    def create_user(self, userid):
        if self.check_user(userid) == False:
            lock.acquire(True)
            self.c.execute("INSERT INTO users(userid) VALUES (?)", (userid,))
            lock.release()
            self.conn.commit()

    def update_language(self,userid,language):
        self.create_user(userid)
        lock.acquire(True)
        self.c.execute("UPDATE users set language=? WHERE userid=?",(language,userid))
        lock.release()
        self.conn.commit()

    def update_level(self,userid,level):
        self.create_user(userid)
        lock.acquire(True)
        self.c.execute("UPDATE users set level=? WHERE userid=?",(level,userid))
        lock.release()
        self.conn.commit()

    def update_session(self,userid,session):
        self.create_user(userid)
        lock.acquire(True)
        self.c.execute("UPDATE users set session=? WHERE userid=?",(session,userid))
        lock.release()
        self.conn.commit()

    def update_poll_id(self,userid,poll_id):
        self.create_user(userid)
        lock.acquire(True)
        self.c.execute("UPDATE users set poll_id=? WHERE userid=?",(poll_id,userid))
        lock.release()
        self.conn.commit()

    def get_user_session_level_language(self,userid):
        lock.acquire(True)
        self.c.execute("SELECT session,level,language FROM users WHERE userid=?", (userid,))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot
        else:
            return False

    def update_user_messageid_answer(self,userid,messageid,answer):
        lock.acquire(True)
        self.c.execute("UPDATE users SET message_id=?,answer=? WHERE userid=?",(messageid,answer,userid))
        lock.release()
        self.conn.commit()

    def get_session_type(self, userid, msgid):
        lock.acquire(True)
        self.c.execute("SELECT session FROM users WHERE userid=? AND message_id=?", (userid, msgid))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def get_answer_msgid(self, userid, msgid):
        lock.acquire(True)
        self.c.execute("SELECT answer FROM users WHERE userid=? AND message_id=?", (userid, msgid))
        lock.release()
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False

    def get_answer(self, userid):
        self.c.execute("SELECT answer FROM users WHERE userid=?", (userid,))
        bot = self.c.fetchone()
        if bot is not None:
            return bot[0]
        else:
            return False
