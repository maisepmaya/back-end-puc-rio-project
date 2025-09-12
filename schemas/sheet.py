from pydantic import BaseModel, ConfigDict
from typing import Dict, Literal, Optional
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
    id: str = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
    level: int = 1
    life: int = 20
    ac: int = 15    
    icon: str = 'folder/img.png'
    info: str = 'Ataque: +4 // Cimitarra: 1d6 + 2 // Velocidade: 9 metros'
    type: str = 'independent'

class SheetDelSchema(BaseModel):
    id: str

class SheetSearchNameSchema(BaseModel):
    text: str = "Goblin"
    type:  Literal['id', 'name']= 'name' 

class SheetSearchSchema(BaseModel):
    type: Literal['independent', 'dependent'] 

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
        "type": sheet.type,
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
        "type": sheet.type,
        }

    return result


