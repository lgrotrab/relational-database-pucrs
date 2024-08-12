import sqlalchemy as sa
import sqlalchemy.orm as orm


engine = sa.create_engine("sqlite:///BD/ocorrencia.db")
base = orm.declarative_base()

class dp(base):
    __tablename__ = "dp"
    cod_dp = sa.Column(sa.INTEGER ,primary_key=True, index=True)
    nome = sa.Column(sa.VARCHAR(100), nullable=False)
    endereco = sa.Column(sa.VARCHAR(255), nullable=False)

class responsavelDP(base):
    __tablename__ = "responsavel_dp"
    cod_dp = sa.Column(sa.INTEGER, sa.ForeignKey("dp.cod_dp", ondelete="NO ACTION", onupdate="CASCADE") , primary_key=True, index=True, )
    delegado = sa.Column(sa.VARCHAR(100), nullable=False)

class municipio(base):
    __tablename__ = "municipio"
    cod_ibge = sa.Column(sa.INTEGER, primary_key=True, index=True)
    municipio = sa.Column(sa.VARCHAR(100), nullable=False)
    regiao = sa.Column(sa.VARCHAR(25), nullable=False)

class ocorrencia(base):
    __tablename__ = "ocorrencia"
    id_registro = sa.Column(sa.INTEGER, primary_key=True, index=True)
    cod_dp = sa.Column(sa.INTEGER, sa.ForeignKey("dp.cod_dp", ondelete="NO ACTION", onupdate="CASCADE"), index=True, )
    cod_ibge = sa.Column(sa.INTEGER, sa.ForeignKey("municipio.cod_ibge", ondelete="NO ACTION", onupdate="CASCADE"), index=True)
    ano = sa.Column(sa.CHAR(4), nullable=False)
    mes = sa.Column(sa.VARCHAR(2), nullable=False)
    ocorrencia = sa.Column(sa.VARCHAR(100), nullable=False)
    qtde = sa.Column(sa.INTEGER, nullable=False)

try:
    base.metadata.create_all(engine)
    print("Tabelas criadas!!")
except ValueError:
    print(ValueError)