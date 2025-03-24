from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Union, Tuple
from model.card import Card
from model.sheet import Sheet

class CardSchema(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    index: int = 1
    sheet_id: str = 'goblin-verde'

class CardViewSchema(BaseModel):
    id: str = 'goblin-verde-0'
    index: int = 0
    currLife: int = 7
    sheetId: str = "goblin-verde"
    info: str = 'Ataque: +4 // Cimitarra: 1d6 + 2 // Velocidade: 9 metros',
    name: str = "Goblin"
    level: int = 1
    maxLife: int = 7
    ac: int = 15    
    icon: str = 'folder/img.png'

class ObjectCardSchema(BaseModel):
    sheets: Dict[str, CardViewSchema]

class CardDelSchema(BaseModel):
    id: str = 'goblin-verde-1'

class CardUpdateSchema(BaseModel):
    id: str = 'goblin-verde-1'
    index: int = 0
    currLife: int = 7
    info: str = "Ataque: +4 // Cimitarra: 1d6 + 2 // Velocidade: 9 metros"

def display_card(card: Card, sheet: Sheet):
    return {
        'id': card.id,
        'index': card.index,
        'currLife': card.currLife,
        'sheet_id': card.sheet_id,
        'info': card.info,
        "name": sheet.name,
        "level": sheet.level,
        "life":  sheet.life,
        "ac":  sheet.ac,
        "icon":  sheet.icon,
    }

def display_cards(items:List[Tuple[Card, Sheet]]):
    result = {}
    for item in items:
        card = item[0]
        sheet = item[1]

        result[card.id] = {
        'id': card.id,
        'index': card.index,
        'currLife': card.currLife,
        'sheet_id': card.sheet_id,
        'info': card.info,
        "name": sheet.name,
        "level": sheet.level,
        "life":  sheet.life,
        "ac":  sheet.ac,
        "icon":  sheet.icon,
    }
    return  result


