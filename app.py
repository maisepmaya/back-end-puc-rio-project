from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Sheet
from logger import logger
from model.card import Card
from schemas import *
from flask_cors import CORS

from schemas.card import CardDelSchema, CardSchema, CardUpdateSchema, CardViewSchema, ObjectCardSchema, display_card, display_cards



info = Info(title="HordaMaster API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

sheet_tag = Tag(name="Ficha", description="Adição, visualização e remoção de fichas à base")
card_tag = Tag(name="Cartões", description="Adição, visualização e remoção de cartões à base")

@app.route('/')
def home():
    return redirect('/openapi/swagger')


# Fichas -------------------------------------------
@app.post('/sheet/create', tags=[sheet_tag],
          responses={"200": SheetViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_sheet(form: SheetSchema):
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
        logger.debug(f"Ficha {sheet.name} adicionada!")
        return display_sheet(sheet), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Ficha com mesmo nome já cadastrado, {sheet.name}"
        logger.warning(f"Erro ao adicionar ficha '{sheet.name}', de id '{sheet.id}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Parece que ocorreu um erro."
        logger.warning(f"Erro ao adicionar ficha '{sheet.name}', de id '{sheet.id}', {error_msg}")
        return {"message": error_msg}, 400

@app.delete('/sheet/delete', tags=[sheet_tag],
            responses={"200": SheetDelSchema, "404": ErrorSchema})
def del_sheet(query: SheetDelSchema):
    sheet_id = unquote(unquote(query.id))

    logger.debug(f"Deletando dados sobre ficha #{sheet_id}")

    session = Session()
    countSheet = session.query(Sheet).filter(Sheet.id == sheet_id).delete()
    
    session.query(Card).filter(Card.sheet_id == sheet_id).delete()
    session.commit()

    if countSheet:
        logger.debug(f"Deletado ficha #{sheet_id}")
        return {"message": "Ficha e cartões removidos", "id": sheet_id}
    else:
        error_msg = "Ficha não encontrada na base"
        logger.warning(f"Erro ao deletar ficha com id:'{sheet_id}', {error_msg}")
        return {"message": error_msg}, 404

@app.get('/sheet/getAll', tags=[sheet_tag],
         responses={"200": ObjectSheetsSchema, "404": ErrorSchema})
def get_sheets():
    logger.debug(f"Buscando fichas.")

    session = Session()
    sheets = session.query(Sheet).all()

    if not sheets:
        return {}, 200
    else:
        logger.debug(f"%d Fichas encontradas" % len(sheets))
        return display_sheets(sheets), 200


# Cartões  -------------------------------------------
@app.post('/card/create', tags=[card_tag],
          responses={"200": CardViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_card(form: CardSchema):
    sheet_id  = form.sheet_id

    session = Session()
    sheet = session.query(Sheet).filter(Sheet.id == sheet_id).first()

    if not sheet:
        error_msg = "Ficha não encontrada para criação de cartão"
        logger.warning(f"Erro ao adicionar cartão de ficha'{sheet_id}', {error_msg}")
        
        return {"mesage": error_msg}, 404
    
    card = Card( 
        index= form.index,
        currLife= sheet.life,
        sheet_id= form.sheet_id,
        info= sheet.info,
        )
    
    try:
        session = Session()
        session.add(card)
        session.commit()
        logger.debug(f"Ficha {sheet.name} adicionada!")
        return display_card(card, sheet), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Ficha com mesmo nome já cadastrado."
        logger.warning(f"Erro ao adicionar cartão de ficha'{sheet_id}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Parece que ocorreu um erro."
        logger.warning(f"Erro ao adicionar cartão de ficha'{sheet_id}', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/card/getAll', tags=[card_tag],
         responses={"200": ObjectCardSchema, "404": ErrorSchema})
def get_cards():
    logger.debug(f"Buscando fichas.")

    session = Session()

    items = session.query(Card, Sheet).filter(Card.sheet_id == Sheet.id).all()

    if not items:
        return {}, 200
    else:
        logger.debug(f"%d Cartões encontrados" % len(items))
        logger.debug(f'{items}')
        return display_cards(items), 200

@app.delete('/card/delete', tags=[card_tag],
            responses={"200": CardDelSchema, "404": ErrorSchema})
def del_card(query: CardDelSchema):
    card_id = unquote(unquote(query.id))

    logger.debug(f"Deletando dados sobre cartão #{card_id}")

    session = Session()
    count = session.query(Card).filter(Card.id == card_id).delete()
    session.commit()

    if count:
        logger.debug(f"Deletado ficha #{card_id}")
        return {"message": "Cartão removido", "id": card_id}
    else:
        error_msg = "Cartão não encontrado na base"
        logger.warning(f"Erro ao deletar ficha com id:'{card_id}', {error_msg}")
        return {"message": error_msg}, 404

@app.put('/card/update', tags=[card_tag],
            responses={"200": CardViewSchema, "404": ErrorSchema})
def update_card(query: CardUpdateSchema):
    card_id = query.id
    sheet_id = query.sheet_id


    session = Session()
    card = session.query(Card).filter(Card.id == card_id).first()


    props = {
        'index': query.index,
        'currLife': query.currLife,
        'info': query.info,
    }
    
    for key, value in props.items():
        setattr(card, key, value)

    session.commit()

    # print(card)
    sheet = session.query(Sheet).filter(Sheet.id == sheet_id).first()
    return display_card(card, sheet), 200
    # session.commit()

    # if count:
    #     logger.debug(f"Deletado ficha #{card_id}")
    #     return {"message": "Cartão removido", "id": card_id}
    # else:
    #     error_msg = "Cartão não encontrado na base"
    #     logger.warning(f"Erro ao deletar ficha com id:'{card_id}', {error_msg}")
    #     return {"message": error_msg}, 404

# @app.get('/cards/getAll', tags=[card_tag],
#          responses={"200": ObjectCardSchema, "404": ErrorSchema})
# def get_cards():
#     logger.debug(f"Buscando cartões.")

#     session = Session()
#     sheets = session.query(Card).all()

#     if not sheets:
#         return {"cartões": {}}, 200
#     else:
#         logger.debug(f"%d Cartões econtrados" % len(sheets))
#         return display_cards(sheets), 200

# @app.post('/card/create', tags=[card_tag],
#           responses={"200": CardViewSchema, "409": ErrorSchema, "400": ErrorSchema})
# def add_card(form: CardSchema):
#     sheet_id  = form.sheet_id

#     session = Session()
#     sheet = session.query(Sheet).filter(Sheet.id == sheet_id).first()

#     if not sheet:
#         error_msg = "Ficha não encontrada na base"
#         logger.warning(f"Erro ao adicionar cartão de ficha'{sheet_id}', {error_msg}")
        
#         return {"mesage": error_msg}, 404
    
#     card = Card( 
#         index= form.index,
#         currLife= form.currLife,
#         sheet_id= form.sheet_id,
#         info= form.info,
#         )
    
#     try:
#         session = Session()
#         session.add(card)
#         session.commit()
#         logger.debug(f"Ficha {sheet.name} adicionada!")
#         return display_card(card, sheet), 200

#     except IntegrityError as e:
#         # como a duplicidade do nome é a provável razão do IntegrityError
#         error_msg = "Ficha com mesmo nome já cadastrado."
#         logger.warning(f"Erro ao adicionar ficha '{sheet.name}', de id '{sheet.id}', {error_msg}")
#         return {"message": error_msg}, 409

#     except Exception as e:
#         # caso um erro fora do previsto
#         error_msg = "Parece que ocorreu um erro."
#         logger.warning(f"Erro ao adicionar ficha '{sheet.name}', de id '{sheet.id}', {error_msg}")
#         return {"message": error_msg}, 400



# @app.post('/cards/replaceAll', tags=[card_tag],
#          responses={"200": ObjectCardSchema, "404": ErrorSchema})
# def replace_cards():
    
#     try:
#         num_rows_deleted = session.query(Card).delete()
#         session.commit()
#     except:
#         session.rollback()


# @app.post('/cometario', tags=[comentario_tag],
#           responses={"200": ProdutoViewSchema, "404": ErrorSchema})
# def add_comentario(form: ComentarioSchema):
#     """Adiciona de um novo comentário à um produtos cadastrado na base identificado pelo id

#     Retorna uma representação dos produtos e comentários associados.
#     """
#     produto_id  = form.produto_id
#     logger.debug(f"Adicionando comentários ao produto #{produto_id}")
#     # criando conexão com a base
#     session = Session()
#     # fazendo a busca pelo produto
#     produto = session.query(Produto).filter(Produto.id == produto_id).first()

#     if not produto:
#         # se produto não encontrado
#         error_msg = "Produto não encontrado na base :/"
#         logger.warning(f"Erro ao adicionar comentário ao produto '{produto_id}', {error_msg}")
#         return {"mesage": error_msg}, 404

#     # criando o comentário
#     texto = form.texto
#     comentario = Comentario(texto)

#     # adicionando o comentário ao produto
#     produto.adiciona_comentario(comentario)
#     session.commit()

#     logger.debug(f"Adicionado comentário ao produto #{produto_id}")

#     # retorna a representação de produto
#     return apresenta_produto(produto), 200
