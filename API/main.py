import fastapi
from model import Puffles
from typing import Optional
from sqlmodel import create_engine, SQLModel, Session, select



app = fastapi.FastAPI()
engine = create_engine('sqlite:///database.db')

def db_connect():
    try:
        SQLModel.metadata.create_all(engine)
    
    except Exception as e:
        
        print('Ocorreu um erro ao tentar conectar ao banco: ', e)
        
    finally:
        print('Banco conectado com sucesso')
        
    


@app.on_event('startup')
async def criar_banco():
    
    db_connect() 
    

@app.get('/mostrar')
async def mostrar_puffles():
    
    puffles = []
        
    with Session(engine) as session:
        
        statement = select(Puffles)
        result = session.exec(statement)
        for i in result:
            puffles.append(i)
            
    return{'Puffles': puffles}


@app.get('/mostrar/{id}')
async def mostrar_puffles(id: int):
    
    with Session(engine) as session:
        
        statement = select(Puffles).where(Puffles.id == id)
        puffle = session.exec(statement).first()
        
    return puffle
    
    
    
    
@app.post('/adicionar', status_code=fastapi.status.HTTP_201_CREATED)
async def adicionar_puffle(puffle: Optional[Puffles] = None):
    try:
        
        with Session(engine) as session:
            
            session.add(puffle)
            session.commit()
        
        return {'status': 'Adicionado com sucesso'}
            
    except KeyError:
        
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_204_NO_CONTENT, detail=f'Não foi possivel adicionar o Puffle {puffle.nome}')


    
@app.delete('/remover/{id}')
async def remover_puffle(id):
    
    with Session(engine) as session:
        statement = select(Puffles).where(Puffles.id == id)
        puffle = session.exec(statement).first()

        session.delete(puffle)
        session.commit()
        
    return {'status': f'Puffle com id {id} deletado com sucesso'}


@app.put('/atualizar/{id}')
async def atualizar_puffle(id: int, novo_puffle: Optional[Puffles] = None):
    
    try:
        
        with Session(engine) as session:
            
            statement = select(Puffles).where(Puffles.id == id)
            puffle = session.exec(statement).first()
            
            puffle.nome = novo_puffle.nome
            puffle.descricao = novo_puffle.descricao
            puffle.custo = novo_puffle.custo
            puffle.data_lancamento = novo_puffle.data_lancamento
            puffle.imagem = novo_puffle.imagem
            
            session.add(puffle)
            session.commit()
            session.refresh(puffle)
        
        return {'status': 'Atualizado com sucesso'}
            
    except KeyError:
        
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_204_NO_CONTENT, detail=f'Não foi possivel adicionar o Puffle {puffle.nome}')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, log_level='info', reload=True)