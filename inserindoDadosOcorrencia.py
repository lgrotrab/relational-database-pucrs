import pandas as pd
import os
import sqlalchemy as sa
import sqlalchemy.orm as orm
import ocorrencia as oc

#recupera endereço de arquivos de data de forma dinâmica
dirname = os.path.dirname(__file__)
endereco = (dirname + "\\Data\\")

#cria sessão para conectar com o banco
engine = sa.create_engine("sqlite:///BD//ocorrencia.db")
Sessao = orm.sessionmaker(bind=engine)
sessao = Sessao()

#Cria metadata para utilizar na leitura do arquivo excel
metadata = sa.MetaData()
metadata.create_all(engine)

##Adiciona dados de DP ao banco

#Lê os dados do arquivo DP.csv e transforma em uma tabela.
dp = pd.read_csv(endereco + "DP.csv",sep=",")
tbDP = pd.DataFrame(dp)

try:
    #apaga dados existentes para evitar conflitos
    sessao.query(oc.dp).delete()
except ValueError:
    print(ValueError)

#insere dados no banco do arquivo csv
for i in range(len(tbDP)):
    dadoDP = oc.dp(
                                cod_dp = int(tbDP["cod_dp"][i]),
                                nome = tbDP["nome"][i],
                                endereco = tbDP["endereco"][i]
                            )
    try:
        sessao.add(dadoDP)
        sessao.commit()
    except ValueError:
        print(ValueError())

print ("tbDP criada!")

##Adiciona dados de Municipio ao banco

#Lê os dados do arquivo Municipio.csv e transforma em uma tabela.
municipio = pd.read_csv(endereco + "Municipio.csv",sep=",")
tbMunicipio = pd.DataFrame(municipio)

try:
    #apaga dados existentes para evitar conflitos
    sessao.query(oc.municipio).delete()
except ValueError:
    print(ValueError)

for i in range(len(tbMunicipio)):
    dadoMunicipio = oc.municipio(
                                cod_ibge = int(tbMunicipio["cod_ibge"][i]),
                                municipio = tbMunicipio["municipio"][i],
                                regiao = tbMunicipio["regiao"][i]
                            )
    try:
        sessao.add(dadoMunicipio)
        sessao.commit()
    except ValueError:
        print(ValueError())

print ("tbMunicipio criada!")

##Adiciona dados de responsavelDP ao banco

#lê arquivo excel com dados de dpResponsavel e coleta os dados pro python
responsavelDP = pd.read_excel(endereco + "ResponsavelDP.xlsx")
tbResponsavelDP = pd.DataFrame(responsavelDP)

#Transforma os dados em uma lista, correlacionando os registros/linhas/tuplas, através do método dicionário (to_dict)
dadosResponsavelDP = tbResponsavelDP.to_dict(orient='records')

#Variável que representa a tabela que se deseja inserir os dados e, um metadados.
tabelaResponsavelDP = sa.Table(oc.responsavelDP.__tablename__, metadata, autoload_with=engine)

#Inserindo dados a partir de uma sessao com a engrenagem de BD
try:
    #deleta os dados antes de conectar para evitar erros
    sessao.execute(tabelaResponsavelDP.delete())
    #Adiciona os novos dados
    sessao.execute(tabelaResponsavelDP.insert(), dadosResponsavelDP)
    sessao.commit()
except ValueError:
    print(ValueError())

print("tbResponsavelProduto criada!")

##Adiciona dados de ocorrencia ao banco

#lê arquivo excel com dados de ocorrencia e coleta os dados pro python
ocorrencia = pd.read_excel(endereco + "ocorrencias.xlsx")
tbOcorrencia = pd.DataFrame(ocorrencia)

#Transforma os dados em uma lista, correlacionando os registros/linhas/tuplas, através do método dicionário (to_dict)
dadosOcorrencia = tbOcorrencia.to_dict(orient='records')

#Variável que representa a tabela que se deseja inserir os dados e, um metadados.
tabelaOcorrencia= sa.Table(oc.ocorrencia.__tablename__, metadata, autoload_with=engine)

#Inserindo dados a partir de uma sessao com a engrenagem de BD
try:
    #deleta os dados antes de conectar para evitar erros
    sessao.execute(tabelaOcorrencia.delete())
    #Adiciona os novos dados
    sessao.execute(tabelaOcorrencia.insert(), dadosOcorrencia)
    sessao.commit()
except ValueError:
    print(ValueError())

print("tbOcorrencia criada!")

#encerra todas as sessões
sessao.close_all()
print("Módulo de inserção de dados finalizado!")