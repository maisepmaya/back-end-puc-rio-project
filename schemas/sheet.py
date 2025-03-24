from pydantic import BaseModel, ConfigDict
from typing import Dict, Literal
from model.sheet import Sheet

class SheetSchema(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    name: str = "Goblin Verde"
    level: int = 1
    life: int = 7
    ac: int = 15
    icon: str = 'folder/img.png'
    info: str = 'Ataque: +4 // Cimitarra: 1d6 + 2 // Velocidade: 9 metros'

class SheetViewSchema(BaseModel):
    name: str = "Goblin"
    id: str = "goblin-verde"
    level: int = 1
    life: int = 20
    ac: int = 15    
    icon: str = 'folder/img.png'
    info: str = 'Ataque: +4 // Cimitarra: 1d6 + 2 // Velocidade: 9 metros'

class SheetDelSchema(BaseModel):
    id: str

class SheetSearchSchema(BaseModel):
    text: str = "Goblin"
    type:  Literal['id', 'name']= 'name' 

class ObjectSheetsSchema(BaseModel):
    sheets: Dict[str, SheetViewSchema]

def display_sheet(sheet: Sheet):
    return {
        "id": sheet.id,
        "name": sheet.name,
        "level": sheet.level,
        "life":  sheet.life,
        "ac":  sheet.ac,
        "icon":  sheet.icon,
        "info":  sheet.info,
    }

def display_sheets(sheets: Dict[str, Sheet]):
    result = {}
    for sheet in sheets:
        result[sheet.id] = {
        "id": sheet.id,
        "name": sheet.name,
        "level": sheet.level,
        "life":  sheet.life,
        "ac":  sheet.ac,
        "icon":  sheet.icon,
        "info":  sheet.info,
        }

    return result


