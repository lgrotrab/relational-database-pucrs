import pandas as pd
import sqlalchemy as sa
import sqlalchemy.orm as orm
import ocorrencia as oc

#cria sessão e se conecta ao banco
engine = sa.create_engine("sqlite:///BD//ocorrencia.db")
Sessao = orm.sessionmaker(bind=engine)
sessao = Sessao()

#Cria metadata
metadata = sa.MetaData()
metadata.create_all(engine)

tbMunicipio = sa.Table(oc.municipio.__tablename__, metadata, autoload_with=engine)

atualizaRegiao = sa.update(tbMunicipio).values(
    {"regiao":"Rio de Janeiro"}
).where(
    tbMunicipio.c.municipio == "Rio de Janeiro"
)

try:
    sessao.execute(atualizaRegiao)
    sessao.commit()
    print("Dados atualizados")
except ValueError:
    print(ValueError)