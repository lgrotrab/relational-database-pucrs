import sqlalchemy as sa

#cria uma engrenagem que irá criar o banco para ser utilizado para o banco de dados específico, no caso o sqlite
engine = sa.create_engine("sqlite:///BD/vendas.db")

#importa os métodos de ORM do sqlalchemy
import sqlalchemy.orm as orm

#a base é uma ponte entre o banco e a classe da linguagem
base = orm.declarative_base()

#Tabela cliente
class cliente(base):
    ##o table name precisa dos underline obrigatoriamente nesse modelo
    __tablename__ = "cliente"
    cpf = sa.Column(sa.CHAR(14),primary_key=True, index=True)
    nome = sa.Column(sa.VARCHAR(100), nullable=False)
    email = sa.Column(sa.VARCHAR(50), nullable=False)
    genero = sa.Column(sa.CHAR(1))
    salario = sa.Column(sa.DECIMAL(10,2))
    dia_mes_aniversario = sa.Column(sa.CHAR(5))
    bairro = sa.Column(sa.VARCHAR(50))
    cidade = sa.Column(sa.VARCHAR(50))
    uf = sa.Column(sa.CHAR(2))

#tabelas com chaves estrangeiras precisam ser criadas após as tabelas com a chave primária relacionada

#Tabela fornecedor
class fornecedor(base):
    __tablename__="fornecedor"
    registro_fornecedor = sa.Column(sa.INTEGER, primary_key=True, index=True)
    nome_fantasia = sa.Column(sa.VARCHAR(50), nullable=False)
    razao_social = sa.Column(sa.VARCHAR(100), nullable=False)
    cidade = sa.Column(sa.VARCHAR(50), nullable=False)
    uf = sa.Column(sa.CHAR(2), nullable=False)

#Tabela produto
class produto(base):
    __tablename__="produto"
    cod_barras = sa.Column(sa.INTEGER, primary_key=True, index=True)
    registro_fornecedor = sa.Column(sa.INTEGER, sa.ForeignKey('fornecedor.registro_fornecedor', ondelete="NO ACTION", onupdate="CASCADE"), index=True)
    dsc_produto = sa.Column(sa.VARCHAR(100), nullable=False)
    genero = sa.Column(sa.CHAR(1))

#Tabela vendedor
class vendedor(base):
    __tablename__="vendedor"
    registro_vendedor = sa.Column(sa.INTEGER, primary_key=True, index=True)
    cpf = sa.Column(sa.CHAR(14), nullable=False)
    nome = sa.Column(sa.VARCHAR(100), nullable=False)
    email = sa.Column(sa.VARCHAR(50), nullable=False)
    genero = sa.Column(sa.CHAR(1))

#Tabela vendas
class vendas(base):
    __tablename__="vendas"
    id_transacao = sa.Column(sa.INTEGER, primary_key=True, index=True)
    cpf = sa.Column(sa.CHAR(14), sa.ForeignKey('cliente.cpf', ondelete="NO ACTION", onupdate="CASCADE"),index=True)
    registro_vendedor = sa.Column(sa.INTEGER, sa.ForeignKey('vendedor.registro_vendedor', ondelete="NO ACTION", onupdate="CASCADE"), index=True)
    cod_barras = sa.Column(sa.INTEGER, sa.ForeignKey('produto.cod_barras', ondelete='NO ACTION', onupdate='CASCADE'), index=True)

#adiciona tabelas ao modelo
try:
    base.metadata.create_all(engine)
    print("Tabelas criadas!!")
except ValueError:
    print(ValueError)