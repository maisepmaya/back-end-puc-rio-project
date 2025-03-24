from sqlalchemy import Column, String, Integer, Text
from typing import Union

from  model import Base

class Sheet(Base):
        __tablename__ = 'sheet'

        id = Column("pk_sheet", String(150), primary_key=True)
        name = Column(String(140), unique=True)
        level = Column(Integer)
        life = Column(Integer)
        ac = Column(Integer)
        icon = Column(String(140))
        info = Column(Text, default='')

        def __init__(self, name:str, level: Integer, life: Integer, ac: Integer, icon:str, info: str):
            self.id = "-".join(name.split()).lower()
            self.name = name
            self.level = level
            self.life = life
            self.icon = icon
            self.ac = ac

            if (info):
                self.info = info


