
from sqlalchemy import Column, String, Integer
from datetime import date
import threading
from VegetaRobot.modules.sql import BASE, SESSION



class CoupleChats(BASE):
    __tablename__ = 'CoupleChats'
    chat_id = Column(String(14), primary_key=True)
    day = Column(Integer)
    man_id = Column(String(14))
    woman_id = Column(String(14))

    def __init__(self, chat_id, day, man_id, woman_id):
        self.chat_id = chat_id
        self.day = day
        self.man_id = man_id
        self.woman_id = woman_id

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
            couple.man_id = man_id
            couple.woman_id = woman_id
        SESSION.add(couple)
        SESSION.commit()


def get_all_chat_ids():
    try:
        chat_ids = SESSION.query(CoupleChats.chat_id).all()
        return [chat_id[0] for chat_id in chat_ids]  # Extract the first element from each tuple
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
            return {'chat_id': couple.chat_id, 'day': couple.day, 'man_id': couple.man_id, 'woman_id': couple.woman_id}
        else:
            return {}

