import pandas as pd
import sqlalchemy as sa
import sqlalchemy.orm as orm
import ocorrencia as oc

#cria sessão e se conecta ao banco
engine = sa.create_engine("sqlite:///BD//ocorrencia.db")
Sessao = orm.sessionmaker(bind=engine)
sessao = Sessao()

#consulta dados no banco
rankDP = pd.DataFrame(
    sessao.query(
        oc.dp.nome.label("DP"),
        sa.func.sum(oc.ocorrencia.qtde).label("Total")  
    ).join(
        oc.ocorrencia,
        oc.ocorrencia.cod_dp == oc.dp.cod_dp
    ).join(
        oc.municipio,
        oc.ocorrencia.cod_ibge == oc.municipio.cod_ibge
    ).filter(
        oc.municipio.regiao == "Capital" 
    ).group_by(
        oc.dp.nome
    ).order_by(
        sa.func.sum(oc.ocorrencia.qtde).label("Total").desc() 
    ).all()
)

print(rankDP)

sessao.close_all()
print("sessão fechada")