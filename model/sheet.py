import uuid
from sqlalchemy import Column, String, Integer, Text, Float
from typing import Union

from  model import Base

class Sheet(Base):
        __tablename__ = 'sheet'

        id = Column("pk_sheet", String(150), primary_key=True)
        name = Column(String(140))
        level = Column(Float)
        life = Column(Integer)
        ac = Column(Integer)
        icon = Column(String(140))
        info = Column(Text, default='')
        type = Column(String(20), default='independent')

        def __init__(self, name:str, level: float, life: Integer, ac: Integer, icon:str, info: str, type:str = 'independent'):
            self.id =  str(uuid.uuid4()) 
            self.name = name
            self.level = level
            self.life = life
            self.icon = icon
            self.ac = ac
            self.type = type

            if (info):
                self.info = info


