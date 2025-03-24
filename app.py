from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Sheet
from model.card import Card
from schemas import *
from flask_cors import CORS


info = Info(title="HordaMaster API", summary="A API HordaMaster se trata de uma API para gerenciamento de fichas de inimigos em jogos de RPG.", description="Seu propósito é permitir a criação, leitura, atualização e exclusão de registros de inimigos, além de possibilitar a manipulação em tempo real dos atributos desses registros, facilitando a organização e o controle de grandes grupos de adversários.", version="1.0.0", contact={
  "name": "Maíse Perini Maya",
  "url": "https://github.com/maisepmaya"
})
app = OpenAPI(__name__, info=info)
CORS(app)

sheet_tag = Tag(name="Ficha", description="Fornece operações para criação, consulta e remoção de fichas.")
card_tag = Tag(name="Cartões", description="Permite a criação, consulta, atualização e remoção de cartões associados às fichas.")

@app.route('/')
def home():
    return redirect('/openapi/swagger')


# Fichas -------------------------------------------
@app.post('/sheet/create', tags=[sheet_tag],
          responses={"200": SheetViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_sheet(form: SheetSchema):
    """Cria uma nova ficha e a adiciona à base de dados.

    - **200**: Retorna a ficha criada com todos os seus atributos.
    - **409**: Nome da ficha já cadastrado.
    - **400**: Erro inesperado na criação da ficha.
    """

    sheet = Sheet(
        name = form.name,
        level = form.level,
        life = form.life,
        ac = form.ac,
        info = form.info,
        icon = form.icon
        )


    try:
        session = Session()
        session.add(sheet)
        session.commit()
        return display_sheet(sheet), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Ficha com mesmo nome já cadastrado, {sheet.name}"
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Parece que ocorreu um erro."
        return {"message": error_msg}, 400
    finally:
        session.close()

@app.delete('/sheet/delete', tags=[sheet_tag],
            responses={"200": SheetDelSchema, "404": ErrorSchema, "400": ErrorSchema})
def del_sheet(query: SheetDelSchema):
    """Remove uma ficha existente da base de dados pelo seu ID e seus cartões associados.

    - **200**: Confirmação da remoção da ficha.
    - **404**: Ficha não encontrada.
    """
    try:
        sheet_id = unquote(unquote(query.id))

        session = Session()

        countSheet = session.query(Sheet).filter(Sheet.id == sheet_id).delete()
        session.query(Card).filter(Card.sheet_id == sheet_id).delete()

        session.commit()

        if countSheet:
            return {"message": "Ficha e cartões removidos", "id": sheet_id}
        else:
            error_msg = "Ficha não encontrada na base"
            return {"message": error_msg}, 404
    finally:
        session.close()

@app.get('/sheet/getAll', tags=[sheet_tag],
         responses={"200": ObjectSheetsSchema, "400": ErrorSchema})
def get_sheets():
    """Retorna todas as fichas armazenadas na base de dados.

    - **200**: Lista de fichas encontradas ou um objeto vazio caso não existam fichas.
    """
    session = Session()

    try:
        sheets = session.query(Sheet).all()
        session.close()

        if not sheets:
            return {}, 200
        else:
            return display_sheets(sheets), 200
    except Exception as e:
        error_msg = "Parece que ocorreu um erro."
        return {"message": error_msg}, 400
    finally:
            session.close()


# Cartões  -------------------------------------------
@app.post('/card/create', tags=[card_tag],
          responses={"200": CardViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_card(form: CardSchema):
    """Cria um novo cartão associado a uma ficha existente.

    - **200**: Retorna o cartão criado e os detalhes da ficha associada.
    - **404**: Ficha para cadastro não encontrada.
    - **409**: Cartão já existente.
    - **400**: Erro inesperado.
    """
    
    try:
        sheet_id  = form.sheet_id
        session = Session()

        sheet = session.query(Sheet).filter(Sheet.id == sheet_id).first()

        if not sheet:
            error_msg = "Ficha não encontrada para criação de cartão"
            return {"mesage": error_msg}, 404

        card = Card(
            index= form.index,
            currLife= sheet.life,
            sheet_id= form.sheet_id,
            info= sheet.info,
            )
    
        session.add(card)
        session.commit()
        return display_card(card, sheet), 200
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Parece que ocorreu um erro."
        return {"message": error_msg}, 400
    finally:
        session.close()

@app.get('/card/getAll', tags=[card_tag],
         responses={"200": ObjectCardSchema, "400": ErrorSchema})
def get_cards():
    """Retorna todos os cartões cadastrados, vinculados às suas respectivas fichas.

    - **200**: Lista de cartões encontrados ou um objeto vazio caso não existam cartões.
    - **400**: Erro inesperado.
    """

    try:
        session = Session()

        items = session.query(Card, Sheet).filter(Card.sheet_id == Sheet.id).all()

        if not items:
            return {}, 200
        else:
            return display_cards(items), 200
    except Exception as e:
        error_msg = "Parece que ocorreu um erro."
        return {"message": error_msg}, 400
    finally:
        session.close()

@app.delete('/card/delete', tags=[card_tag],
            responses={"200": CardDelSchema, "404": ErrorSchema, "400": ErrorSchema})
def del_card(query: CardDelSchema):
    """Remove um cartão da base de dados pelo seu ID.

    - **200**: Confirmação da remoção do cartão.
    - **404**: Cartão não encontrado.
    - **400**: Erro inesperado.
    """
    try:
        card_id = unquote(unquote(query.id))

        session = Session()
        count = session.query(Card).filter(Card.id == card_id).delete()
        session.commit()

        if count:
            return {"message": "Cartão removido", "id": card_id}
        else:
            error_msg = "Cartão não encontrado na base"
            return {"message": error_msg}, 404
    except Exception as e:
        error_msg = "Parece que ocorreu um erro."
        return {"message": error_msg}, 400
    finally:
        session.close()

@app.delete('/card/deleteAll', tags=[card_tag],
            responses={"200": CardDelSchema, "400": ErrorSchema})
def del_card_all():
    """Remove todos os cartões da base.

    - **200**: Confirmação da remoção.
    - **400**: Erro inesperado.
    """

    try:
        session = Session()
        session.query(Card).delete()
        session.commit()
        return {"message": "Cartões removidos."}
    except Exception as e:
        error_msg = "Parece que ocorreu um erro."
        return {"message": error_msg}, 400
    finally:
        session.close()

@app.put('/card/update', tags=[card_tag],
            responses={"200": CardViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_card(form: CardUpdateSchema):
    """Atualiza as informações de um cartão existente na base de dados.

    - **200**: Retorna o cartão atualizado com os novos dados e informações de sua ficha.
    - **404**: Cartão não encontrado.
    - **400**: Erro inesperado.
    """
    
    try:
        card_id = form.id

        session = Session()
        card = session.query(Card).filter(Card.id == card_id).first()

        if card:
            props = {
                'index': form.index,
                'currLife': form.currLife,
                'info': form.info,
            }

            for key, value in props.items():
                setattr(card, key, value)

            session.commit()

            sheet = session.query(Sheet).filter(Sheet.id == card.sheet_id).first()

            return display_card(card, sheet), 200
        else:
            error_msg = "Cartão não encontrado na base"
            return {"message": error_msg}, 404
    except Exception as e:
        error_msg = "Parece que ocorreu um erro."
        return {"message": error_msg}, 400
    finally:
        session.close()

