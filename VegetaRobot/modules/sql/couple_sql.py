
from sqlalchemy import Column, String, Integer
from datetime import date
import threading
from VegetaRobot.modules.sql import BASE, SESSION



class CoupleChats(BASE):
    __tablename__ = 'couple_chats'
    chat_id = Column(String(14), primary_key=True)
    day = Column(Integer)
    man = Column(String(14))
    woman = Column(String(14))

    def __init__(self, chat_id, day, man, woman):
        self.chat_id = chat_id
        self.day = day
        self.man = man
        self.woman = woman

CoupleChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_couple_chat(chat_id):
    try:
        chat = SESSION.query(CoupleChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()

def rem_couple_chat(chat_id):
    with INSERTION_LOCK:
        couple = SESSION.query(CoupleChats).get(str(chat_id))
        if couple:
            SESSION.delete(couple)
        SESSION.commit()

def set_couple_chat(chat_id, man_id, woman_id):
    with INSERTION_LOCK:
        day = int(str(date.today()).split("-")[-1])
        couple = SESSION.query(CoupleChats).get(str(chat_id))
        if not couple:
            couple = CoupleChats(str(chat_id), day, man_id, woman_id)
        else:
            couple.day = day
            couple.man = man_id
            couple.woman = woman_id
        SESSION.add(couple)
        SESSION.commit()

def get_all_chat_ids():
    try:
        return SESSION.query(CoupleChats).all()
    finally:
        SESSION.close()

def get_couples_chat_day(chat_id):
    with INSERTION_LOCK:        
        couple = SESSION.query(CoupleChats).get(str(chat_id))
        if couple:
            return couple.day
        else:
            return False

def get_couple_info(chat_id):
    with INSERTION_LOCK:
        couple = SESSION.query(CoupleChats).get(str(chat_id))
        if couple:
            return {'chat_id': couple.chat_id, 'day': couple.day, 'man': couple.man, 'woman': couple.woman}
        else:
            return None

