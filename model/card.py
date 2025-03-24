from sqlalchemy import Column, String, Integer, DateTime, ForeignKey,Text
from typing import  Union
from sqlalchemy.orm import relationship

from  model import Base


class Card(Base):
    __tablename__ = 'cartoes'

    id = Column("pk_card", String(150), primary_key=True)
    index = Column(Integer)
    currLife = Column(Integer)
    info = Column(String, default='')
    sheet_id = Column(
        String(150),
        ForeignKey('sheet.pk_sheet', ondelete='CASCADE'),
        nullable=False,
    )

   
    def __init__(self, index:Integer, currLife: Integer, sheet_id: str, info: Union[String, None],):
            self.id = sheet_id + '-' + str(index)
            self.index = index
            self.currLife = currLife
            self.sheet_id = sheet_id

            if (info):
                self.info = info
        
