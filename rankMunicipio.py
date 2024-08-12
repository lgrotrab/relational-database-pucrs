import pandas as pd
import sqlalchemy as sa
import sqlalchemy.orm as orm
import ocorrencia as oc

#cria sessão e se conecta ao banco
engine = sa.create_engine("sqlite:///BD//ocorrencia.db")
Sessao = orm.sessionmaker(bind=engine)
sessao = Sessao()

rankMunicipio = pd.DataFrame(
    sessao.query(
        oc.municipio.municipio.label("Municipio"),
        sa.func.sum(oc.ocorrencia.qtde).label("Total de roubo de veículos")
    ).join(
        oc.municipio,
        oc.municipio.cod_ibge == oc.ocorrencia.cod_ibge
    ).filter(
        oc.ocorrencia.ocorrencia == "roubo_veiculo"
    ).group_by(
        oc.municipio.municipio
    ).order_by(
        sa.func.sum(oc.ocorrencia.qtde).desc() 
    ).all()
)

print(rankMunicipio)

sessao.close_all()
print("sessão fechada")