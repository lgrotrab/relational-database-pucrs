import pandas as pd #biblioteca de manipulação de dados

#variável para armazenar o endereço
#pega o caminho relativo para o arquivo
import os
dirname = os.path.dirname(__file__)
endereco = (dirname + "\\Data\\")

#variavel com o nome do arquivo
vendedor = pd.read_csv(endereco + "vendedor.csv",sep=";")

#Coleta os dados do arquivo para dentro do Python
tbVendedor = pd.DataFrame(vendedor)

#Importa o sqlalchemy para conectar ao BD Vendas
import sqlalchemy as sa
#Criando a engrenagem de conexão com o BD
engine = sa.create_engine("sqlite:///BD//vendas.db")

#iniciando um sessão com o banco de dados
import sqlalchemy.orm as orm
Sessao = orm.sessionmaker(bind=engine)
sessao = Sessao()

#importando as classes que estão no arquivo vendas.py para inserir dados
import vendas as vd

#deleta valores existentes para evitar erro
try:
    sessao.query(vd.vendedor).delete()
except ValueError:
    print(ValueError)

#Algoritmo para inserção de dados, utilizando o DataFrame tbVendedor
for i in range(len(tbVendedor)):
    dado_vendedor = vd.vendedor(
                                registro_vendedor = int(tbVendedor["registro_vendedor"][i]),
                                cpf = tbVendedor["cpf"][i],
                                nome = tbVendedor["nome"][i],
                                email = tbVendedor["email"][i],
                                genero = tbVendedor["genero"][i]
                            )
    try:
        sessao.add(dado_vendedor)
        sessao.commit()
    except ValueError:
        print(ValueError())

print ("tbVendedor criada!")

#Algoritmo para inserção de dados, utilizando o DataFrame tbProduto
#variavel com o nome do arquivo
produto = pd.read_excel(endereco + "produto.xlsx")

#Coleta os dados do arquivo para dentro do Python
tbProduto = pd.DataFrame(produto)

#Variável de definição de metadados, para identificar que estrutura será atualizada
metadata = sa.MetaData()
metadata.create_all(engine)

#Algoritmo para inserção de dados, utilizando o DataFrame tbProduto
#Transforma os dados em uma lista, correlacionando os registros/linhas/tuplas, através do método dicionário (to_dict)
DadosProduto = tbProduto.to_dict(orient='records')

#Variável que representa a tabela que se deseja inserir os dados e, um metadados.
tabela_produto = sa.Table(vd.produto.__tablename__, metadata, autoload_with=engine) #na classe que representa a tabela de ocorrências
#Inserindo dados a partir de uma conexão com a engrenagem de BD
try:
    #deleta os dados antes de conectar para evitar erros
    sessao.execute(tabela_produto.delete())
    #Adiciona os novos dados
    sessao.execute(tabela_produto.insert(), DadosProduto)
    sessao.commit()
except ValueError:
    print(ValueError())

print("tbProduto criada!")

sessao.close_all()
print("Módulo de inserção de dados finalizado!")